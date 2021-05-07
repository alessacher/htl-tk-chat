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
import sys
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
        print(f"message={message}")
        if message == None:
            shutdown = True
            return
        if( type(message) == int):
            print("got a hinig message from socket:")
            print(message)
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

dir = os.path.dirname(__file__)
config_file = os.path.join(dir, "client.conf")
cconfig = configparser.ConfigParser()

if os.path.exists(config_file):
    cconfig.read(config_file)

else:
    cconfig["SSL"] = {
        "enable_ssl" : False
    }

if len(sys.argv) == 4 :
    host = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
else:
  try:
      host = cconfig.get("frontend","host")
      port = int(cconfig.get("frontend","port"))
      user = cconfig.get("frontend","user")
  except:
    host = input("Server address: ")
    port = int(input("Server port: "))
    user = input("username: ")
    
print(f"backend got {user}@{host}:{port}")

if cconfig["SSL"].getboolean("enable_ssl"):
    my_client = SSL_Client(
        host,
        port,
        cconfig["SSL"]["certfile"],
        eval("".join(("ssl.PROTOCOL_",cconfig["SSL"]["ssl_version"])))
        )
else:
    my_client = Client(host, port)

def init_backend():
        try:
            print(f"authenticating on {my_client.sock} as {user}")
            client_functions.authenticate(my_client.sock, user)

            read_thread = threading.Thread(
                target=main_read_loop,
                args=(my_client.sock,))
            write_thread = threading.Thread(
                target=main_write_loop,
                args=(my_client.sock, user,))

            if __name__ == "__main__":
                read_thread.start()

            write_thread.start()

            #read_thread.join()
            #write_thread.join()

        except KeyboardInterrupt:
            shutdown = True
            client_functions.close_connection(my_client.sock)
            exit()

if __name__ == '__main__':
    print("client starting standalone")
    init_backend()
