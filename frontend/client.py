#! /usr/bin/python3

"""The Chat Client

This is the chat client with Qt6 frontend.
"""

import sys
import os.path
import logging
import logging.config
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic # .ui files and their content
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import * # cursor shapes
from PyQt6.QtWidgets import *

from userstub import *
from settingsstub import *
from mainwindow import Ui_MainWindow
from settingswindow import Ui_SettingsWindow

sys.path.append('../client')
import chat_client
import client_functions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        logging.info("Application closing")
        client_functions.close_connection(chat_client.my_client.sock)
        event.accept()

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

def main_read_loop(sock):
    """Reads the socket in a loop"""
    while not chat_client.shutdown:
        message = client_functions.get_message(sock)
        print(f"message={message}")
        if message == None:
            chat_client.shutdown = True
            return
        if( type(message) == int):
          logging.error(f"Got Integer from socket : {message}")
        elif message["type"] == "text":
            if message["author"] != chat_client.user:
              display_message(message['author'],message['recipient'],message['content'])
    return

if __name__ == "__main__":
  log_conf = os.path.join(dir, "logger.conf")
  logging.config.fileConfig(log_conf)
  logging.info("Client Logging ready")

  app = QApplication(sys.argv)
  #app.setStyle('Fusion') # only Windows or Fusion

  mainwindow = MainWindow()
  mainwindowui = Ui_MainWindow()
  mainwindowui.setupUi(mainwindow)
  mainwindowui.InputBar.returnPressed.connect(send_msg)
  test_user_table(mainwindowui)
  test_combo_box(mainwindowui)
  mainwindow.show()

  settingswindow = QMainWindow()
  settingswindowui = Ui_SettingsWindow()
  settingswindowui.setupUi(settingswindow)
  mainwindowui.actionServer.triggered.connect(settingswindow.show)
  init_settings_window(settingswindowui)

  display_thread = threading.Thread(target=main_read_loop, args=(chat_client.my_client.sock,))
  display_thread.start()

  sys.exit(app.exec())

