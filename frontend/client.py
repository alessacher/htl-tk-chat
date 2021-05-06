#! /usr/bin/python3

"""The Chat Client

This is the chat client with Qt6 frontend.
"""

import sys
import os.path
import logging
import logging.config
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6 import uic # .ui files and their content
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import * # cursor shapes
from PyQt6.QtWidgets import *

from userstub import *
from settingsstub import *

sys.path.append('../client')
import chat_client
import client_functions

@Slot()
def send_msg():
  """Send message function

  This function is called when the user presses Enter,
  to send the message."""
  r = window.userSelect.currentText()
  t = window.InputBar.text()
  if r == "all":
    logging.info(f"frontend broadcasting message '{t}'")
  else:
    logging.info(f"frontend sending message '{t}' to '{r}'")
  display_message(chat_client.user,r,t)
  client_functions.text_message(chat_client.my_client.sock, t, chat_client.user, r)
  logging.info(f"frontend calling textmessage with {chat_client.my_client.sock},{t},{chat_client.user}->{r}")
  window.InputBar.clear()


def display_message(sender : str, recipient : str, message : str):
  """Displays a message on the msgList :: QListWidget """
  window.msgList.addItem(f"{sender} -> {recipient}: {message}")


def load_ui_file(filename):
  """UI File Loader

  Path independent loader function for QTCreators .ui files
  """
  script_path = os.path.realpath(__file__)
  script_path_list = script_path.split("/")
  script_path_list[-1] = filename
  ui_path = "/".join(script_path_list)
  if os.path.exists(ui_path):
    return uic.loadUi(ui_path)
  else:
    logging.error(f"Cannot open {ui_path} to load {filename}")
    sys.exit(1)

def main_read_loop(sock):
    """Reads the socket in a loop"""
    while not chat_client.shutdown:
        message = client_functions.get_message(sock)
        print(f"message={message}")
        if message == None:
            chat_client.shutdown = True
            return
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

  window = load_ui_file("mainwindow.ui")
  window.InputBar.returnPressed.connect(send_msg)
  test_user_table(window)
  test_combo_box(window)
  window.actionExit.triggered.connect(app.quit)
  window.show()

  settings = load_ui_file("settingswindow.ui")
  window.actionServer.triggered.connect(settings.show)
  init_settings_window(settings)

  display_thread = threading.Thread(target=main_read_loop, args=(chat_client.my_client.sock,))
  display_thread.start()

  sys.exit(app.exec())

