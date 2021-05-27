#! /usr/bin/python3

"""The Chat Server

This is the Chat server, it is the backbone of the communication between
the clients.
"""

import msgpack
import threading
import socketserver
import time
import logging
import logging.config
import ssl
import os
import configparser
import struct
import signal
import sys

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    Handles the request in a thread
    """
    def handle(self):
        """
        function gets a request offer from the socket and prints the
        message and the Thread it is in. It handles the authentication
        and the messages. At the moment it just broadcasts the messages
        """
        logging.info(f"Started new Thread")
        logging.debug(f"New Thread is {threading.current_thread}")
        logging.info(f"Got new connection from {self.client_address}.")

        while True:
            try:
                buffer = recv_msg(self.request)
            except ConnectionResetError:
                logging.error("Connection reset by peer, client disconnected")
                self.remove_user()
                for client in self.server.connected_clients:
                    send_connected_users(
                        client["socket"],
                        connected_users
                    )
                return
            message = unpack_message(buffer)

            if type(message) == int:
                logging.error("fGot Integer from socket : {message}")
                continue

            if message == None:
                logging.error("Client disconnected forcefully")
                self.remove_user()
                for client in self.server.connected_clients:
                    send_connected_users(
                        client["socket"],
                        connected_users
                    )
                return

            if message["type"] == "sslcheck":
                response = config["SSL"].getboolean("enable_ssl")
                send_encoded(self.request, response)
                return

            elif message["type"] == "sslcert":
                certfile = config["SSL"]["certfile"]

                with open(certfile, "rb") as cert:
                    cert_buffer = cert.read()
                
                send_encoded(self.request, cert_buffer)

            elif message["type"] == "auth":
                logging.debug(f"Got auth request from {self.client_address}")
                logging.info(f"New client with username: {message['user']}")
                for client in self.server.connected_clients:
                    if client["user"] == message["user"]:
                        if client["uuid"] != message["uuid"]:
                            text_message(
                                self.request,
                                f"Username : {message['user']} already taken",
                                "SERVER"
                                )
                            self.request.close()
                            return
                        else:
                            text_message(
                                self.request,
                                f"{message['user']} reconnected",
                                "SERVER"
                                )
                            client["socket"] = self.request
                            connected_users = [x["user"] for x in self.server.connected_clients]
                            for client in self.server.connected_clients:
                                send_connected_users(
                                    client["socket"],
                                    connected_users
                                )
                            return

                self.server.connected_clients.append(
                    {
                    "socket" : self.request,
                    "user"   : message["user"],
                    "uuid"   : message["uuid"]
                    }
                    )
                self.user = message["user"]
                connected_users = [x["user"] for x in self.server.connected_clients]
                logging.info(f"created new user {self.user} on socket {self.request}")
                for client in self.server.connected_clients:
                    text_message(
                        client["socket"],
                        f"{message['user']} logged in",
                        "SERVER"
                        )
                    send_connected_users(
                        client["socket"],
                        connected_users
                    )
            

            elif message["type"] == "text":
                logging.debug(f"Got text message request from {self.client_address}")
                if message["recipient"] == "all":
                    for client in self.server.connected_clients:
                        text_message(
                            client["socket"],
                            message["content"],
                            message["author"],
                            message["recipient"]
                            )
                else:
                    logging.debug(f"""New private message to {message['recipient']}""")
                    for client in self.server.connected_clients:
                        if client["user"] == message["recipient"]:
                            text_message(
                                client["socket"],
                                message["content"],
                                message["author"],
                                message["recipient"]
                                )
                            break
                    else:
                        logging.warning(f"{message['recipient']} unavailable")
                        text_message(
                            self.request,
                            "Private Message was not delivered. Reason: user unavailable",
                            "SERVER",
                            self.user
                            )
            
            elif message["type"] == "image":
                logging.debug(f"Got image message request from {self.client_address}")
                if message["recipient"] == "all":
                    for client in self.server.connected_clients:
                        image_message(
                            client["socket"],
                            message["content"],
                            message["author"],
                            message["recipient"]
                            )
                else:
                    logging.debug(f"New private message to {message['recipient']}")
                    for client in self.server.connected_clients:
                        if client["user"] == message["recipient"]:
                            image_message(
                                client["socket"],
                                message["content"],
                                message["author"],
                                message["recipient"]
                                )
                            break
                    else:
                        logging.warning(f"{message['recipient']} unavailable")
                        text_message(
                            self.request,
                            "Private Message was not delivered. Reason: user unavailable",
                            "SERVER",
                            self.user
                            )

            elif message["type"] == "close":
                self.remove_user()
                logging.info(f"Closing connection from {self.client_address}")
                for client in self.server.connected_clients:
                    send_connected_users(
                        client["socket"],
                        connected_users
                    )
                return


    def remove_user(self):
        for client in self.server.connected_clients:
            if client["user"] == self.user:
                self.server.connected_clients.remove(client)

class SSL_TCPServer(socketserver.TCPServer):
    """A TCP Server with SSL support"""
    def __init__(
        self,
        certfile : str,
        keyfile : str,
        server_address : tuple,
        RequestHandlerClass,
        ssl_version,
        bind_and_activate=True
        ):

        socketserver.TCPServer.__init__(
            self,
            server_address,
            RequestHandlerClass,
            bind_and_activate
            )

        dir = os.path.dirname(__file__)
        self.__certfile = os.path.join(dir, certfile)
        self.__keyfile = os.path.join(dir, keyfile)

        self.socket = ssl.wrap_socket(
            self.socket,
            keyfile=self.__keyfile,
            certfile=self.__certfile,
            ssl_version=ssl_version
            )

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    TCPServer with threading support.
    Spawns a new Thread for every response.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected_clients = []
class SSL_ThreadedTCPServer(socketserver.ThreadingMixIn, SSL_TCPServer):
    """
    SSL_TCPServer with threading support.
    Spawns a new Thread for every response.
    Has SSL support
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected_clients = []

def unpack_message(message):
    unpacker = msgpack.Unpacker()
    unpacker.feed(message)
    for object in unpacker:
        return object

def text_message(sock, text : str, author : str, recipient : str = "all"):
    """Text Message function

    Takes a socket, text, author and recipient as arguments and
    sends it to the client.
    """
    message = {
        "type" : "text",
        "content" : text,
        "author" : author,
        "recipient" : recipient,
        "time" : time.time()
    }
    send_encoded(sock, message)
    logging.debug(f"Send message '{text}' to client : {sock.getpeername()}")

def send_connected_users(sock, usernames):
    """Text Message function

    Takes a socket and a iterable usernames as arguments and
    sends it to the client.
    """
    message = {
        "type" : "users",
        "users" : usernames,
        "time" : time.time()
    }
    send_encoded(sock, message)
    logging.debug(f"Send connected users to client")

def image_message(
    sock,
    image : str,
    author : str,
    recipient : str = "all"):
    """Image Message function

    Takes a socket, image, author and recipient as arguments and
    sends it to the server. The image will be base64 encoded.
    """

    message = {
        "type" : "image",
        "content" : image,
        "author" : author,
        "recipient" : recipient,
        "time" : time.time()
    }
    send_encoded(sock, message)
    logging.debug(f"Send image to client : {sock.getpeername()}")

def recv_msg(sock):
    bmessage_length = recvall(sock, 4)
    if not bmessage_length:
        return None
    
    message_length = struct.unpack('>I', bmessage_length)[0]
    logging.debug(f"receiving message of size {message_length} bytes")

    return recvall(sock, message_length)

def recvall(sock, msglen):
    data = bytearray()
    while len(data) < msglen:
        buffer = sock.recv(msglen - len(data))
        if not buffer:
            return None
        data.extend(buffer)
        logging.debug(f"extend data about {len(buffer)} bytes. data now at {len(data)} bytes")
    return data

def send_encoded(sock, message):
    """Helper function to send encoded the message"""
    packer = msgpack.Packer()
    message = packer.pack(message)
    message_length = len(message)
    message = struct.pack('>I', message_length) + message
    sock.sendall(message)

def setup_server(server):
    """function that setups the server"""
    # creating main server thread
    server_thread = threading.Thread(target=server.serve_forever)

    # telling the thread to run in the background
    server_thread.setDaemon(True)
    server_thread.start()
    logging.info("Started Server Thread")

if __name__ == "__main__":
    dir = os.path.dirname(__file__)

    log_conf = os.path.join(dir, "logger.conf")
    logging.config.fileConfig(log_conf)
    logging.info("Logging Ready")

    config_file = os.path.join(dir, "server.conf")
    config = configparser.ConfigParser()

    if os.path.exists(config_file):
        logging.info("Loading \"server.conf\" file")
        config.read(config_file)
    else:
        logging.warning("Using default config")
        config["SERVER"] = {
            "listen_address" : "0.0.0.0",
            "listen_port" : 9999
        }

        config["SSL"] = {
            "enable_ssl" : False
        }

    HOST = config["SERVER"]["listen_address"]
    PORT = int(config["SERVER"]["listen_port"])

    logging.info(f"Server serving at {HOST} on port {PORT}")

    if config["SSL"].getboolean("enable_ssl"):
        logging.info("SSL ENABLED")
        ssl_server = SSL_ThreadedTCPServer(
            config["SSL"]["certfile"],
            config["SSL"]["keyfile"],
            (HOST, PORT+1),
            ThreadedTCPRequestHandler,
            eval("".join(("ssl.PROTOCOL_",config["SSL"]["ssl_version"])))
            )

    else:
        logging.info("SSL DISABLED")

    server = ThreadedTCPServer(
        (HOST,PORT),
        ThreadedTCPRequestHandler
    )

    if config["SSL"].getboolean("enable_ssl"):
        setup_server(ssl_server)
    
    setup_server(server)

    if sys.platform == "linux":
        signal.pause()
    
    else:
        while True:
            pass