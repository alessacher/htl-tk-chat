#! /usr/bin/python3

import socket
import msgpack
import argh

def send_message(ip : str, port : int, message : str):
    """
    sends a message to the server and awaits a response
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        packer = msgpack.Packer()
        unpacker = msgpack.Unpacker()
        port = int(port)
        s.connect((ip, port))
        s.sendall(packer.pack(message))
        buf = s.recv(1024)
        unpacker.feed(buf)
        for o in unpacker:
            print('Received', o)

if __name__ == "__main__":
    argh.dispatch_command(send_message) # makes the command accessible over the commandline
    
