#! /usr/bin/python3

"""The Chat Client

This is the chat client with Qt6 frontend.
"""

import sys
import os.path
import logging
import logging.config
import threading
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic # .ui files and their content
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import * # cursor shapes
from PyQt6.QtWidgets import *

import userstub
import settingsstub
from mainwindow import Ui_MainWindow
from settingswindow import Ui_SettingsWindow

sys.path.append('../client')
import chat_client
import client_functions

display_thread = None
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        logging.info("Application closing")
        if settingsstub.connected == True:
            client_functions.close_connection(chat_client.my_client.sock)
        event.accept()
        if display_thread != None:
            display_thread.join()
        app.quit()

@Slot()
def send_msg():
    """Send message function

    This function is called when the user presses Enter,
    to send the message."""
    r = mainwindowui.userSelect.currentText()
    t = mainwindowui.InputBar.text()
    if r == "all":
        logging.info(f"frontend broadcasting message '{t}'")
    else:
        logging.info(f"frontend sending message '{t}' to '{r}'")
    display_message(chat_client.user,r,t)
    client_functions.text_message(chat_client.my_client.sock, t, chat_client.user, r)
    logging.info(f"frontend calling textmessage with {chat_client.my_client.sock},{t},{chat_client.user}->{r}")
    mainwindowui.InputBar.clear()


def display_message(sender : str, recipient : str, message : str):
    """Displays a message on the msgList :: QListWidget """
    mainwindowui.msgList.addItem(f"{sender} -> {recipient}: {message}")

@Slot()
def start_read_loop():
    """starts the read loop in a new thread"""

    global display_thread

    logging.debug("Starting read loop thread")
    if settingsstub.connected == True and display_thread == None:
        display_thread = threading.Thread(target=main_read_loop, args=(chat_client.my_client.sock,))
        display_thread.start()

@Slot()
def stop_read_loop():
    """stops the read loop thread"""

    global display_thread

    if display_thread != None:
        logging.debug("stopping read loop thread")
        display_thread.join()
        logging.debug("display_thread stopped")
        display_thread = None
    else:
        logging.warning("display thread already stopped")

def main_read_loop(sock):
    """Reads the socket in a loop"""
    logging.debug("read loop started")
    while settingsstub.connected:
        message = client_functions.get_message(sock)
        print(f"message={message}")
        if message == None:
            settingsstub.connected = False
            logging.debug("read loop stopped because of disconnect")
            return
        if( type(message) == int):
          logging.error(f"Got Integer from socket : {message}")
        elif message["type"] == "text":
            if message["author"] != chat_client.user:
              display_message(message['author'],message['recipient'],message['content'])
        elif message["type"] == "users":
            userstub.set_user_table(mainwindowui, message["users"])
            userstub.set_combo_box(mainwindowui, message["users"])

    logging.debug("read loop stopped")
    return

if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    log_conf = os.path.join(dir, "logger.conf")
    logging.config.fileConfig(log_conf)
    logging.info("Client Logging ready")

    app = QApplication(sys.argv)
    app.setStyle('Breeze') # only Windows or Fusion

    mainwindow = MainWindow()
    mainwindowui = Ui_MainWindow()
    mainwindowui.setupUi(mainwindow)
    mainwindowui.InputBar.returnPressed.connect(send_msg)
    mainwindow.show()

    settingswindow = QMainWindow()
    settingswindowui = Ui_SettingsWindow()
    settingswindowui.setupUi(settingswindow)
    mainwindowui.actionServer.triggered.connect(settingswindow.show)
    settingsstub.init_settings_window(settingswindowui)

    settingswindowui.ButtonStartConnection.pressed.connect(start_read_loop)
    settingswindowui.ButtonEndConnection.pressed.connect(stop_read_loop)

    sys.exit(app.exec())
