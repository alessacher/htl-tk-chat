#! /usr/bin/python3
"""
Chat Client backend
"""

import socket
import client_functions
import ssl
import configparser
import os
import os
import getpass
import sys

dir = os.path.dirname(__file__)
os.chdir(dir)

my_client = None
cconfig = None
host = "ehw12.ddns.net"
port = "9999"
user = getpass.getuser()
en_ssl = False

ssl._create_default_https_context = ssl._create_unverified_context

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

        if sys.platform == "linux":
            self.tmpfile = "/tmp/cert.pem"
        else:
            self.tmpfile = "cert.pem.tmp"

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

                with open(self.tmpfile, "wb") as fp:
                    fp.write(cert)

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = ssl.wrap_socket(
                self.sock,
                ca_certs = self.tmpfile,
                ssl_version=self.__ssl_version,
            )

            self.sock.connect((ip, port+1))
        
        else:
            raise ssl.SSL_ERROR_SSL

def read_config():
    global cconfig, host, port, user, en_ssl
    os.chdir(dir)
    config_file = "client.conf"
    cconfig = configparser.ConfigParser()


    if os.path.exists(config_file):
        cconfig.read(config_file)
    else:
        # setup default configuration file 
        cconfig["SSL"] = {
            "enable_ssl" : False
        }
        cconfig["frontend"] = {
            "host" : "ehw12.ddns.net",
            "port" : 9999,
            "user" : getpass.getuser()
        }
        with open(config_file,'w') as fp:
            cconfig.write(fp)

    try:
        host = cconfig.get("frontend","host")
        port = int(cconfig.get("frontend","port"))
        user = cconfig.get("frontend","user")
        en_ssl = cconfig.getboolean("SSL", "enable_ssl")
    except Exception:
        host = input("Server address: ")
        port = int(input("Server port: "))
        user = input("Username: ")
        en_ssl = False


def init_backend(ip = host, port = port, username = user, en_ssl = en_ssl):
    global shutdown, user, my_client

    user = username
    if not en_ssl:
        my_client = Client(ip, port)
    else:
        my_client = SSL_Client(
            ip,
            port,
            ssl.PROTOCOL_TLS
        )
    my_client.connect(ip, port)
    print(f"authenticating on {my_client.sock} as {user}")
    client_functions.authenticate(my_client.sock, username)