"""client_functions
Adds functions for the client to use

This module serves as some kind of API for the chat client. The client
should never send messages to the server directly, but rather through
this api. This makes it easier to programm the GUI later.
"""

import msgpack
import time

def authenticate(sock, username : str):
    """Authentication function

    Takes a socket and a username as arguments and sends it to the 
    server as an auth type message. The auth message has the values user
    for the username identification and time, to know when the user logs
    in. A value for the ip address is not necessary, since the socket
    already knows this.
    """
    message = {
        "type" : "auth",
        "user" : username,
        "time" : time.time()
    }
    packer = msgpack.Packer()
    sock.sendall(packer.pack(message)) 

def text_message(
    sock,
    text : str,
    author : str,
    recipient : str = "all"):
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

def get_message(sock):
    """Get Message function

    Takes a socket argument and returns the message in the pipe.
    """
    unpacker = msgpack.Unpacker()
    buffer = sock.recv(4096)
    unpacker.feed(buffer)
    for object in unpacker:
        return object


def close_connection(sock):
    """Close function

    Closes the server connection and notifies the server about it.
    """
    message = {
        "type" : "close",
        "time" : time.time()
    }
    packer = msgpack.Packer()
    sock.sendall(packer.pack(message))
    sock.close()