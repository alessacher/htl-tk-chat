#! /usr/bin/python3

"""The Chat Server

This is the Chat server, it is the backbone of the communication
between the clients.
"""

import msgpack
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    Handles the request in a thread
    """
    def handle(self):
        """
        function gets a request offer from the socket and prints the message and
        the Thread it is in. Then it sends the message back as a response.
        """
        cur_thread = threading.current_thread()
        packer = msgpack.Packer()
        unpacker = msgpack.Unpacker()
        buffer = self.request.recv(1024)
        unpacker.feed(buffer)
        for o in unpacker:
            print("{} wrote:".format(self.client_address[0]))
            print(o,"on Thread:",cur_thread.name)
            self.request.sendall(packer.pack(o))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    TCPServer with threading support. Spawns a new Thread for every response.
    """
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999 # Listening on the arbitrary port 9999

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        server_thread = threading.Thread(target=server.serve_forever) # creating main server thread

        server_thread.daemon = True # telling the thread to run in the background
        server_thread.start()

        while True:
            pass