"""client_functions
Adds functions for the client to use

This module serves as some kind of API for the chat client.
The client should never send messages to the server directly,
but rather through this api. This makes it easier to programm
the GUI later.
"""

import msgpack
import time

def authenticate(sock, username : str):
    """Authentication function

    Takes a socket and a username as arguments and sends it
    to the server as an auth type message. The auth message 
    has the values user for the username identification and
    time, to know when the user logs in. A value for the ip
    address is not necessary, since the socket already knows
    this.
    """
    message = {
        "type" : "auth",
        "user" : username,
        "time" : time.time()
    }
    packer = msgpack.Packer()
    sock.sendall(packer.pack(message)) 