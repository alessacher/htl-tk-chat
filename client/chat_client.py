#! /usr/bin/python3
"""
Chat client for testing purposes
"""

import socket
import client_functions

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.3.191", 9999))
    client_functions.authenticate(sock, "alessacher")
    sock.close()