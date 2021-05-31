#! /usr/bin/python3

"""The Chat Client

This is the chat client with Qt6 frontend.
"""

import sys
import os.path
from os import chdir
import logging
import logging.config
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication

import user_functions
import settings_functions
from mainwindow import Ui_MainWindow
from settingswindow import Ui_SettingsWindow

dir = os.path.dirname(__file__)
os.chdir(dir)

sys.path.append('../client')
import chat_client
import client_functions

display_thread = None
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        logging.info("Application closing")
        if settings_functions.connected == True:
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
    if settings_functions.connected == True:
        r = mainwindowui.userSelect.currentText()
        t = mainwindowui.InputBar.text()
        if r == "all":
            logging.info(f"frontend broadcasting message '{t}'")
        else:
            logging.info(f"frontend sending message '{t}' to '{r}'")

        user_functions.display_message(mainwindowui, chat_client.user, r, t)
        client_functions.text_message(chat_client.my_client.sock, t, chat_client.user, r)
        logging.info(f"frontend calling textmessage with {chat_client.my_client.sock},{t},{chat_client.user}->{r}")
        mainwindowui.InputBar.clear()
    else:
        logging.info("User not connected to a server {settings_functions.connected}, skipping")

@Slot()
def send_image_file():
    if settings_functions.connected == True:
        logging.debug("Sending new image")
        
        image_file = user_functions.get_image_file()
        
        if image_file is None:
            logging.error("File not found, not sending image")
            return
        recipient = mainwindowui.userSelect.currentText()
        user_functions.display_message(
            mainwindowui,
            chat_client.user,
            recipient,
            "")

        user_functions.add_image(mainwindowui, image_file)
        logging.debug("displaying image")
        client_functions.image_message(
            chat_client.my_client.sock,
            image_file,
            chat_client.user,
            recipient
        )
        logging.debug("Image sent")
    else:
        logging.info("User not connected to a server, skipping")


@Slot()
def start_read_loop():
    """starts the read loop in a new thread"""

    global display_thread

    logging.debug("Starting read loop thread")
    if settings_functions.connected == True and display_thread == None:
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
    while settings_functions.connected:
        message = client_functions.get_message(sock)

        if( type(message) == int):
          logging.error(f"Got Integer from socket : {message}")
          continue

        if message == None:
            settings_functions.connected = False
            logging.debug("read loop stopped because of disconnect")
            return

        elif message["type"] == "text":
            if message["author"] != chat_client.user:
              user_functions.display_message(
                  mainwindowui,
                  message['author'],
                  message['recipient'],
                  message['content'])

        elif message["type"] == "users":
            user_functions.set_user_table(mainwindowui, message["users"])
            user_functions.set_combo_box(mainwindowui, message["users"])

        elif message["type"] == "image":
            if message["author"] != chat_client.user:
                user_functions.display_message(
                    mainwindowui,
                    message["author"],
                    message["recipient"],
                    "")
                user_functions.add_image(mainwindowui, message["content"])



    logging.debug("read loop stopped")
    return

if __name__ == "__main__":
    log_conf = "logger.conf"
    logging.config.fileConfig(log_conf)
    logging.info("Client Logging ready")

    app = QApplication(sys.argv)
    app.setStyle("Breeze") # only Windows or Fusion

    mainwindow = MainWindow()
    mainwindowui = Ui_MainWindow()
    mainwindowui.setupUi(mainwindow)
    mainwindowui.InputBar.returnPressed.connect(send_msg)
    mainwindow.show()

    settingswindow = QMainWindow()
    settingswindowui = Ui_SettingsWindow()
    settingswindowui.setupUi(settingswindow)
    mainwindowui.actionServer.triggered.connect(settingswindow.show)
    settings_functions.init_settings_window(settingswindowui)

    settingswindowui.ButtonStartConnection.pressed.connect(start_read_loop)
    settingswindowui.ButtonEndConnection.pressed.connect(stop_read_loop)

    mainwindowui.addFileButton.pressed.connect(send_image_file)

    sys.exit(app.exec())
