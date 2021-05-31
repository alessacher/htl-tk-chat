#! /usr/bin/python3
"""
Chat Client backend
"""

import socket
import client_functions
import threading
import ssl
import configparser
import os
from os import chdir
import sys
import getpass

dir = os.path.dirname(__file__)
os.chdir(dir)

class Client:
    """Intializes the Socket which is available as self.sock"""
    def __init__(self, ip : str, port : int):
        self.__ip = ip
        self.__port = port

    def connect(self, ip = None, port = None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip == None and port == None:
            self.sock.connect((self.__ip, self.__port))
        else:
            self.sock.connect((ip, port))

class SSL_Client:
    """The same Client but with SSL support"""
    def __init__(
        self,
        ip : str,
        port : int,
        ssl_version):

        self.__ssl_version = ssl_version
        self.__ip = ip
        self.__port = port

    def connect(self, ip = None, port = None):
        if ip == None and port == None:
            ip = self.__ip
            port = self.__port


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))

            ssl_status = client_functions.check_ssl(sock)
            
        if ssl_status:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((ip, port))
                cert = client_functions.get_ssl_cert(sock)

                with open("cert.pem.tmp", "wb") as fp:
                    fp.write(cert)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = ssl.wrap_socket(
                self.sock,
                ca_certs="cert.pem.tmp",
                cert_reqs=ssl.CERT_REQUIRED,
                ssl_version=self.__ssl_version
            )

            self.sock.connect((ip, port+1))
        
        else:
            raise ssl.SSL_ERROR_SSL

def main_read_loop(sock):
    """Reads the socket in a loop"""
    global shutdown
    while not shutdown:
        message = client_functions.get_message(sock)
        print(f"message={message}")
        if message == None:
            shutdown = True
            return
        if( type(message) == int):
            print("got a hinig message from socket:",message)
        elif message["type"] == "text":
            if message["author"] != user:
                if message["recipient"] == "all":
                    print(f"{message['author']}: {message['content']}")
                    #display_message(message['author'],message['content'])
                else:
                    print(f"{message['author']} -> {message['recipient']}: {message['content']}")
                    #display_message(message['author'],message['recipient'],message['content'])
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


shutdown = False

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


print(f"backend got {user}@{host}:{port}")

if cconfig.has_section("SSL"):
    if cconfig["SSL"].getboolean("enable_ssl"):
        my_client = SSL_Client(
            host,
            port,
            eval("".join(("ssl.PROTOCOL_",cconfig["SSL"]["ssl_version"])))
            )
    else:
        my_client = Client(host, port)
else:
    print(f"No SSL Section found in {config_file}!")

def init_backend(ip = None, port = None, username = user):
    global shutdown, user
    try:
        user = username
        my_client.connect(ip, port)
        print(f"authenticating on {my_client.sock} as {user}")
        client_functions.authenticate(my_client.sock, username)

        read_thread = threading.Thread(
            target=main_read_loop,
            args=(my_client.sock,))
        write_thread = threading.Thread(
            target=main_write_loop,
            args=(my_client.sock, user,))

        if __name__ == "__main__":
            read_thread.start()
            write_thread.start()

    except KeyboardInterrupt:
        shutdown = True
        client_functions.close_connection(my_client.sock)
        exit()

if __name__ == '__main__':
    print("client starting standalone")
    init_backend()
