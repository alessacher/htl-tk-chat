"""client_functions
Adds functions for the client to use

This module serves as some kind of API for the chat client. The client
should never send messages to the server directly, but rather through
this api. This makes it easier to programm the GUI later.
"""

import msgpack
import time
import uuid
import socket
import base64
import struct
import logging

too_large_message = msgpack.packb(
    {
    "type" : "toolarge"
    }
)

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
        "uuid" : str(uuid.uuid3(uuid.NAMESPACE_DNS, socket.gethostname())),
        "time" : time.time()
    }
    
    send_encoded(sock, message)

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
    
    send_encoded(sock, message)

def image_message(
    sock,
    image : str,
    author : str,
    recipient : str = "all"):
    """Image Message function

    Takes a socket, image, author and recipient as arguments and
    sends it to the server. The image will be base64 encoded.
    """

    with open(image, "rb") as fp:
        encoded_image = base64.b64encode(fp.read())

    message = {
        "type" : "image",
        "content" : encoded_image,
        "author" : author,
        "recipient" : recipient,
        "time" : time.time()
    }

    send_encoded(sock, message)

def get_message(sock):
    """Get Message function

    Takes a socket argument and returns the message in the pipe.
    """

    buffer = recv_msg(sock)
    if buffer == None:
        return None
    message = unpack_message(buffer)
    if message:
        return message
    else:
        return None

def unpack_message(message):
    """helper function to unpack a message"""
    object = msgpack.unpackb(message)
    return object

def close_connection(sock):
    """Close function

    Closes the server connection and notifies the server about it.
    """
    message = {
        "type" : "close",
        "time" : time.time()
    }
    
    send_encoded(sock, message)

def recv_msg(sock):
    """helper function to receive a whole message"""
    bmessage_length = recv_all(sock, 4)
    if not bmessage_length:
        return None
    
    message_length = struct.unpack('>I', bmessage_length)[0]

    if message_length > 2**17:
        logging.warning("Not receiving messages above 128MiB")
        return too_large_message
    logging.debug(f"receiving message of size {message_length} bytes")

    return recv_all(sock, message_length)

def recv_all(sock, msglen):
    """helper function which receives all up to msglen"""
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
    message = msgpack.packb(message)
    message_length = len(message)
    message = struct.pack('>I', message_length) + message
    sock.sendall(message)

def check_ssl(sock):
    """Check if the server supports ssl"""

    message = {
        "type" : "sslcheck",
        "time" : time.time()
    }

    send_encoded(sock, message)

    response = get_message(sock)
    return response

def get_ssl_cert(sock):
    """Check if the server supports ssl"""

    message = {
        "type" : "sslcert",
        "time" : time.time()
    }

    send_encoded(sock, message)

    response = get_message(sock)
    return response

def file_message(sock,
    filename : str,
    file_data : bytes,
    fileid : str,
    author : str,
    recipient : str = "all"):

    """Sends File to server"""

    message = {
        "type" : "file",
        "content" : filename,
        "filename" : filename,
        "file" : file_data,
        "fileid" : fileid,
        "author" : author,
        "recipient" : recipient, 
        "time" : time.time()
    }

    send_encoded(sock, message)

def get_file(sock, fileid : str):
    """gets a file from the server"""

    message = {
        "type" : "getfile",
        "fileid" : fileid,
        "time" : time.time()
    }

    send_encoded(sock, message)
