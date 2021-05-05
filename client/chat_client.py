#! /usr/bin/python3
"""
CLI bassed Chat Client
"""

import socket
import client_functions
import threading
import ssl
import configparser
import os
class Client:
    """Intializes the Socket which is available as self.sock"""
    def __init__(self, ip : str, port : int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip,port))
        self.sock.setblocking(True)

class SSL_Client:
    """The same Client but with SSL support"""
    def __init__(
        self,
        ip : str,
        port : int,
        certfile : str,
        ssl_version):

        dir = os.path.dirname(__file__)
        self.__certfile = os.path.join(dir, certfile)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = ssl.wrap_socket(
            self.sock,
            ca_certs=self.__certfile,
            cert_reqs=ssl.CERT_REQUIRED,
            ssl_version=ssl_version
        )

        self.sock.connect((ip,port))
        self.sock.setblocking(True)

def main_read_loop(sock):
    """Reads the socket in a loop"""
    global shutdown
    while not shutdown:
        message = client_functions.get_message(sock)
        if message == None:
            shutdown = True
        elif message["type"] == "text":
            if message["author"] != user:
                if message["recipient"] == "all":
                    print(f"{message['author']}: {message['content']}")
                else:
                    print(f"{message['author']} -> {message['recipient']}: {message['content']}")
    return

def main_write_loop(sock, user):
    """Sends messages in a loop"""
    global shutdown
    while not shutdown:
        buffer = input()
        if buffer == "!exit":
            client_functions.close_connection(sock)
            shutdown = True
        elif buffer.startswith("!msg"):
            client_functions.text_message(
                sock,
                " ".join(buffer.split(" ")[2:]),
                user,
                buffer.split(" ")[1])
        else:
            client_functions.text_message(sock, buffer, user)
            
    return


if __name__ == "__main__":

    shutdown = False

    dir = os.path.dirname(__file__)
    config_file = os.path.join(dir, "client.conf")
    config = configparser.ConfigParser()

    if os.path.exists(config_file):
        config.read(config_file)

    else:
        config["SSL"] = {
            "enable_ssl" : False
        }

    if config.has_section("frontend")
        host = config.getstring("frontend","host")
        port = config.getstring("frontend","port")
        user = config.getstring("frontend","user")
    else: # standalone, cli client
        host = input("Server address: ")
        port = int(input("Server port: "))
        user = input("username: ")

    try:
        if config["SSL"].getboolean("enable_ssl"):
            my_client = SSL_Client(
                host,
                port,
                config["SSL"]["certfile"],
                eval("".join(("ssl.PROTOCOL_",config["SSL"]["ssl_version"])))
                )
        else:
            my_client = Client(host, port)



        client_functions.authenticate(my_client.sock, user)

        read_thread = threading.Thread(
            target=main_read_loop,
            args=(my_client.sock,))
        write_thread = threading.Thread(
            target=main_write_loop,
            args=(my_client.sock, user,))

        read_thread.start()
        write_thread.start()

        read_thread.join()
        write_thread.join()

    except KeyboardInterrupt:
        shutdown = True
        client_functions.close_connection(my_client.sock)
        exit()
