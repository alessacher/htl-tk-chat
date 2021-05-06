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
            buffer = self.request.recv(4096)
            message = unpack_message(buffer)

            if message == None:
                logging.error("Client disconnected forcefully")
                self.server.connected_clients.remove(
                    {
                    "socket" : self.request,
                    "user"   : self.user
                    }
                    )
                return

            elif message["type"] == "auth":
                logging.debug(f"Got auth request from {self.client_address}")
                logging.info(f"New client with username: {message['user']}")
                for client in self.server.connected_clients:
                    if client["user"] == message["user"]:
                        text_message(
                            self.request,
                            f"Username : {message['user']} already taken",
                            "SERVER"
                            )
                        self.request.close()
                        return

                self.server.connected_clients.append(
                    {
                    "socket" : self.request,
                    "user"   : message["user"]
                    }
                    )
                self.user = message["user"]
                logging.info(f"created new user {self.user} on socket {self.request}")
                for client in self.server.connected_clients:
                    text_message(
                        client["socket"],
                        f"{message['user']} logged in",
                        "SERVER"
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

            elif message["type"] == "close":
                self.server.connected_clients.remove(
                    {
                    "socket" : self.request,
                    "user"   : self.user
                    })
                logging.info(f"Closing connection from {self.client_address}")
                return

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
    sends it to the server.
    """
    message = {
        "type" : "text",
        "content" : text,
        "author" : author,
        "recipient" : recipient,
        "time" : time.time()
    }
    packer = msgpack.Packer()
    sock.sendall(packer.pack(message))
    logging.debug(f"Send message '{text}' to client : {sock.getpeername()}")

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
        server = SSL_ThreadedTCPServer(
            config["SSL"]["certfile"],
            config["SSL"]["keyfile"],
            (HOST, PORT),
            ThreadedTCPRequestHandler,
            eval("".join(("ssl.PROTOCOL_",config["SSL"]["ssl_version"])))
            )

    else:
        logging.info("SSL DISABLED")
        server = ThreadedTCPServer(
            (HOST,PORT),
            ThreadedTCPRequestHandler
        )

    with server:
        # creating main server thread
        server_thread = threading.Thread(target=server.serve_forever)

        # telling the thread to run in the background
        server_thread.setDaemon(True)
        server_thread.start()
        logging.info("Started Server Thread")

        while True:
            pass
