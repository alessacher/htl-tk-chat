#! /usr/bin/python3
"""
CLI Chat Client
"""

import backend
import client_functions
import threading
import configparser
import os
from os import chdir
import sys
import getpass

dir = os.path.dirname(__file__)
chdir(dir)

shutdown = False

def main_read_loop(sock):
    """Reads the socket in a loop"""
    global shutdown
    while not shutdown:
        message = client_functions.get_message(sock)
        if message == None:
            shutdown = True
            return
        if( type(message) == int):
            print("got a hinig message from socket:",message)
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

if __name__ == '__main__':
    print("client starting standalone")
    config_file = "client.conf"
    cconfig = configparser.ConfigParser()


    if os.path.exists(config_file):
        cconfig.read(config_file)
    else:
        # setup default configuration file 
        cconfig["SSL"] = {
            "enable_ssl" : False,
            "ssl_version" : "TLSv1"
        }
        cconfig["frontend"] = {
            "host" : "ehw12.ddns.net",
            "port" : 9999,
            "user" : getpass.getuser()
        }
        cconfig.write(open(config_file,'w'))

    if len(sys.argv) == 4 :
        host = sys.argv[1]
        port = int(sys.argv[2])
        user = sys.argv[3]
    else:
        try:
            host = cconfig.get("frontend","host")
            port = int(cconfig.get("frontend","port"))
            user = cconfig.get("frontend","user")
        except Exception:
            host = input("Server address: ")
            port = int(input("Server port: "))
            user = input("Username: ")

    backend.init_backend(host, port, user)

    read_thread = threading.Thread(
        target=main_read_loop,
        args=(backend.my_client.sock,))
    write_thread = threading.Thread(
        target=main_write_loop,
        args=(backend.my_client.sock, user,))

    read_thread.start()
    write_thread.start()
