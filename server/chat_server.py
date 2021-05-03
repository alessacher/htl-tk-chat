#! /usr/bin/python3

"""The Chat Server

This is the Chat server, it is the backbone of the communication
between the clients.
"""

import msgpack
import threading
import socketserver
import time
import logging
import logging.config

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    Handles the request in a thread
    """
    def handle(self):
        """
        function gets a request offer from the socket and prints the message and
        the Thread it is in. It handles the authentication and the messages.
        At the moment it just broadcasts the messages
        """
        logging.info(f"Started new Thread")
        logging.debug(f"New Thread is {threading.current_thread}")
        logging.info(f"Got new connection from {self.client_address}.")
        while True:
            buffer = self.request.recv(4096)
            message = unpack_message(buffer)
            if message == None:
                logging.error("Client disconnected forcefully")
                self.server.connected_clients.remove(self.request)
                return
            elif message["type"] == "auth":
                logging.debug(f"Got auth request from {self.client_address}")
                logging.info(f"New client with username: {message['user']}")
                self.server.connected_clients.append(self.request)
                for client in self.server.connected_clients:
                    text_message(client, f"{message['user']} logged in", "SERVER")
            elif message["type"] == "text":
                logging.debug(f"Got text message request from {self.client_address}")
                for client in self.server.connected_clients:
                    text_message(client, message["content"], message["author"], message["recipient"])
            elif message["type"] == "close":
                self.server.connected_clients.remove(self.request)
                logging.info(f"Closing connection from {self.client_address}")
                return


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    TCPServer with threading support. Spawns a new Thread for every response.
    """
    def __init__(self, *args):
        super().__init__(*args)
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
    logging.debug(f"Send message to client : {sock.getpeername()}")

if __name__ == "__main__":
    logging.config.fileConfig("logger.conf")
    logging.info("Logging Ready")

    HOST, PORT = "0.0.0.0", 9999 # Listening on the arbitrary port 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever) # creating main server thread

        server_thread.setDaemon(True) # telling the thread to run in the background
        server_thread.start()
        logging.info("Started Server Thread")

        while True:
            pass