#/usr/bin/python3

import unittest
from unittest.loader import makeSuite
import msgpack
import sys
import os.path
import struct
import time
import uuid
import socket

dir = os.path.dirname(__file__)
os.chdir(dir)

sys.path.append('../client')
import client_functions


class DummySocket():

    def __init__(self):
        self.__sent_output : bytes
        self.__out_queue : bytes

    def sendall(self, buffer):
        self.__sent_output = buffer
        self.__out_queue = buffer

    def recv(self, length):
        output = self.__out_queue[:length]
        self.__out_queue = self.__out_queue[length:]
        return output

    def get_last_sent(self):
        return self.__sent_output

class TestSendEncoded(unittest.TestCase):
    
    def setUp(self):
        self.sock = DummySocket()
        self.message = "Lorem Ipsum"
        self.packed_message = msgpack.packb(self.message)
        self.message_len = len(self.packed_message)

        client_functions.send_encoded(self.sock, self.message)

    def test_struct_packing(self):
        message_len = struct.unpack(">I", self.sock.get_last_sent()[:4])[0]

        self.assertEqual(message_len, self.message_len)

    def test_decode(self):
        message = msgpack.unpackb(self.sock.get_last_sent()[4:])

        self.assertEqual(message, self.message)

class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        self.sock = DummySocket()
        self.message = "Lorem Ipsum"
        self.packed_message = msgpack.packb(self.message)

    def test_unpacking(self):
        message = client_functions.unpack_message(self.packed_message)

        self.assertEqual(self.message, message)

    def test_recv_all(self):

        numbers = "01234"
        self.sock.sendall(numbers.encode("UTF-8"))

        for i in range(5):
            number = client_functions.recv_all(self.sock, 1)
            self.assertEqual(number.decode("UTF-8"), numbers[i])

class TestAuthenticate(unittest.TestCase):

    def setUp(self):
        self.sock = DummySocket()
        self.user = "test_user"
        self.uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, socket.gethostname()))
        self.message = {
            "type" : "auth",
            "user" : self.user,
            "uuid" : self.uuid,
            "time" : time.time()
        }
        self.packed_message = msgpack.packb(self.message)
        self.message_len = len(self.packed_message)

        client_functions.authenticate(self.sock, self.user)

    def test_message_len(self):
        message_len = struct.unpack('>I', self.sock.get_last_sent()[:4])[0]

        self.assertEqual(message_len, self.message_len)

    def test_authenticate_message(self):
        packed_message = self.sock.get_last_sent()
        message = msgpack.unpackb(packed_message[4:])

        self.assertEqual(message["type"], "auth")
        self.assertEqual(message["user"], self.user)
        self.assertEqual(message["uuid"], self.uuid)
        
class TestTextMessage(unittest.TestCase):

    def setUp(self):
        self.sock = DummySocket()
        self.user = "test_user"
        self.recipient = "test_user2"
        self.content = "Lorem ipsum"
        self.message = {
            "type" : "text",
            "content" : self.content,
            "author" : self.user,
            "recipient" : self.recipient,
            "time" : time.time()
        }
        self.packed_message = msgpack.packb(self.message)
        self.message_len = len(self.packed_message)

        client_functions.text_message(
            self.sock,
            self.content,
            self.user,
            self.recipient
        )
    
    def test_message_len(self):
        message_len = struct.unpack('>I', self.sock.get_last_sent()[:4])[0]

        self.assertEqual(message_len, self.message_len)
    
    def test_text_message(self):
        packed_message = self.sock.get_last_sent()
        message = msgpack.unpackb(packed_message[4:])

        self.assertEqual(message["type"], "text")
        self.assertEqual(message["content"], self.content)
        self.assertEqual(message["author"], self.user)
        self.assertEqual(message["recipient"], self.recipient)

class TestCloseConnection(unittest.TestCase):

    def setUp(self):
        self.sock = DummySocket()

        self.message = {
            "type" : "close",
            "time" : time.time()
        }
        self.packed_message = msgpack.packb(self.message)
        self.message_len = len(self.packed_message)

        client_functions.close_connection(self.sock)

    def test_message_len(self):
        message_len = struct.unpack('>I', self.sock.get_last_sent()[:4])[0]

        self.assertEqual(message_len, self.message_len)

    def test_close_messaege(self):
        packed_message = self.sock.get_last_sent()
        message = msgpack.unpackb(packed_message[4:])

        self.assertEqual(message["type"], self.message["type"])

class TestGetMessage(unittest.TestCase):

    def setUp(self):
        self.sock = DummySocket()

        self.message = "Lorem Ipsum"
        self.packed_message = msgpack.packb(self.message)
        self.message_len = len(self.packed_message)

        client_functions.send_encoded(self.sock, self.message)
    
    def test_message(self):
        message = client_functions.get_message(self.sock)

        self.assertEqual(message, self.message)


if __name__ == "__main__":
    unittest.main()