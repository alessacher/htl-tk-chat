"""
This file provides functions for the mainwindow to use
"""
import base64
import logging
import logging.config
import os.path
import sys
from PIL import Image
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, pyqtSlot as Slot

dir = os.path.dirname(__file__)
os.chdir(dir)

sys.path.append('../client')
import backend
import client_functions

def set_user_table(window, users):
    """function to uptade the user table on the right side"""
    table = window.chatList
    table.clear()
    table.setRowCount(len(users))
    table.setColumnCount(1)
    table.setHorizontalHeaderLabels(["Users"])

    logging.debug(f"Users: {users}")

    for index, user in enumerate(users):
        userwidget = QTableWidgetItem(str(user))
        logging.debug(f"Made user widget from user {user}")
        table.setItem(index, 0, userwidget)

def set_combo_box(window, users):
    """function to uptade the user select combo box"""
    window.userSelect.clear()
    users.insert(0, "all")
    window.userSelect.addItems(users)

def display_message(window, sender : str, recipient : str, message : str):
    """Displays a message on the msgList :: QListWidget """
    item = QListWidgetItem(f"{sender} -> {recipient}: {message}")
    window.msgList.addItem(item)
    window.msgList.scrollToItem(item)

def display_file(window, sender, recipient, filename, fileid):
    """Diplays the file message"""
    item = QListWidgetItem(f"{sender} -> {recipient}: file: {filename}")
    item.setStatusTip(f"{fileid}")
    window.msgList.addItem(item)
    window.msgList.scrollToItem(item)

def add_image(window, image):
    """Adds an image to the Chat

    add_image(window, image) -> None

    The window parameter is a QObject
    The image parameter can be a path to an image
    or a base64 encoded image string.
    """
    IMAGE_MAX_SIZE = 300
    listwidget = window.msgList
    listitem = QListWidgetItem()
    if os.path.exists(image):
        im = Image.open(image)
        w, h = im.size
        w, h = min(w, IMAGE_MAX_SIZE), min(h, IMAGE_MAX_SIZE)
        icon = QIcon(image)
        size = QSize(w, h)
    else:
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(image))
        icon = QIcon(pixmap)
        size = pixmap.size()
        w, h = size.width(), size.height()
        w, h = min(w, IMAGE_MAX_SIZE), min(h, IMAGE_MAX_SIZE)
        size = QSize(w, h)

    listitem.setSizeHint(size)
    listitem.setIcon(icon)
    listwidget.setIconSize(size)
    listwidget.addItem(listitem)

def get_file():
    """Opens a File Dialog to get a file and returns its to the file"""
    file, _ = QFileDialog.getOpenFileName(None,
        filter = (
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff *gif);; All Files (*)"
            )
    )
    if not file:
        return None
    return file

def get_save_file():
    """Opens a File Dialog to save a file and returns its to the file"""
    file, _ = QFileDialog.getSaveFileName(None,
        filter = ("All Files (*)")
    )
    if not file:
        return None
    return file
