#! /usr/bin/python3

"""The Chat Client

This is the chat client with Qt5 frontend.
"""

import sys
import os.path
import os
import logging
import logging.config
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication

import user_functions
import settings_functions
from mainwindow import Ui_MainWindow
from settingswindow import Ui_SettingsWindow

dir = os.path.dirname(__file__)
os.chdir(dir)

sys.path.append('../client')
import backend
import client_functions

display_thread = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        logging.info("Application closing")
        if settings_functions.connected == True:
            client_functions.close_connection(backend.my_client.sock)
        event.accept()
        if display_thread != None:
            display_thread.join()
        app.quit()

@Slot()
def send_msg():
    """Send message function

    This function is called when the user presses Enter,
    to send the message."""
    if settings_functions.connected:
        r = mainwindowui.userSelect.currentText()
        t = mainwindowui.InputBar.text()
        if r == "all":
            logging.info(f"frontend broadcasting message '{t}'")
        else:
            logging.info(f"frontend sending message '{t}' to '{r}'")

        user_functions.display_message(mainwindowui, backend.user, r, t)
        client_functions.text_message(backend.my_client.sock, t, backend.user, r)
        logging.info(f"frontend calling textmessage with {backend.my_client.sock},{t},{backend.user}->{r}")
        mainwindowui.InputBar.clear()
    else:
        logging.info(f"User not connected to a server {settings_functions.connected}, skipping")

@Slot()
def send_file():
    if settings_functions.connected:
        logging.debug("Sending new File")
        filename = user_functions.get_file()

        if filename.endswith(("png", "jpg", "jpeg", "bmp", "tiff", "gif")):
            send_image_file(filename)
        
        else:
            with open(filename, "rb") as fp:
                file_data = fp.read()

            logging.debug("read file into memory")

            filename = os.path.basename(filename)
            fileid = "-".join((filename, str(time.time())))

            recipient = mainwindowui.userSelect.currentText()
            user_functions.display_file(
                mainwindowui,
                backend.user,
                recipient,
                os.path.basename(filename),
                fileid
            )

            logging.debug("displaying file")

            client_functions.file_message(
                backend.my_client.sock,
                filename,
                file_data,
                fileid,
                backend.user,
                recipient
            )

            logging.debug("file sent")

def send_image_file(image_file):
    if settings_functions.connected:
        logging.debug("Sending new image")

        if image_file is None:
            logging.error("File not found, not sending image")
            return
        recipient = mainwindowui.userSelect.currentText()
        user_functions.display_message(
            mainwindowui,
            backend.user,
            recipient,
            "")

        user_functions.add_image(mainwindowui, image_file)
        logging.debug("displaying image")
        client_functions.image_message(
            backend.my_client.sock,
            image_file,
            backend.user,
            recipient
        )
        logging.debug("Image sent")
    else:
        logging.info("User not connected to a server, skipping")

@Slot()
def get_file_from_server(listwidgetitem):
    text = listwidgetitem.data()

    if not text:
        return

    elif "file:" in text and "FileID:" in text:
        logging.debug("Try to get file from server")
        startindex = text.find("FileID: ")
        fileid = text[startindex+8:]

        file_data = client_functions.get_file(
            backend.my_client.sock,
            fileid
        )

        if file_data == "ERROR":
            logging.error("File not found")
            return

        elif file_data:
            logging.debug("Got file from server")

            save_file = user_functions.get_save_file()

            if save_file:
                with open(save_file, "wb") as fp:
                    fp.write(file_data)

            logging.info("File saved")
        
        else:
            logging.error("File is None")

@Slot()
def start_read_loop():
    """starts the read loop in a new thread"""

    global display_thread

    logging.debug("Starting read loop thread")
    if settings_functions.connected == True and display_thread == None:
        display_thread = threading.Thread(
            target=main_read_loop,
            args=(backend.my_client.sock,))
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
            if message["author"] != backend.user:
              user_functions.display_message(
                  mainwindowui,
                  message['author'],
                  message['recipient'],
                  message['content'])

        elif message["type"] == "users":
            user_functions.set_user_table(mainwindowui, message["users"])
            user_functions.set_combo_box(mainwindowui, message["users"])

        elif message["type"] == "image":
            if message["author"] != backend.user:
                user_functions.display_message(
                    mainwindowui,
                    message["author"],
                    message["recipient"],
                    "")
                user_functions.add_image(mainwindowui, message["content"])
        
        elif message["type"] == "filetext":
            if message["author"] != backend.user:
              user_functions.display_file(
                  mainwindowui,
                  message['author'],
                  message['recipient'],
                  message['content'],
                  message['fileid'])



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
    mainwindowui.SettingButton.pressed.connect(settingswindow.show)
    mainwindowui.ConnectButton.pressed.connect(
        lambda : settings_functions.quickConnect(mainwindowui ,settingswindowui)
        )

    if not os.path.exists("../client/client.conf"):
        settingswindow.show()
    else:
        backend.read_config()
        
    settings_functions.init_settings_window(settingswindowui)

    settingswindowui.ButtonStartConnection.pressed.connect(start_read_loop)
    settingswindowui.ButtonEndConnection.pressed.connect(stop_read_loop)

    mainwindowui.addFileButton.pressed.connect(send_file)
    mainwindowui.msgList.pressed.connect(get_file_from_server)


    sys.exit(app.exec())
