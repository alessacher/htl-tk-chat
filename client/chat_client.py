#! /usr/bin/python3
"""
CLI bassed Chat Client
"""

import socket
import client_functions
import threading
class Client:
    """Intializes the Socket which is available as self.sock"""
    def __init__(self, ip : str, port : int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    host = input("Server address: ")
    port = int(input("Server port: "))

    shutdown = False

    try:
        my_client = Client(host, port)
        user = input("username: ")

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
    