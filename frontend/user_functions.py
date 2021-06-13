"""
This file provides functions for the mainwindow to use
"""
import base64
import logging
import logging.config
import os.path
from PIL import Image
from PyQt5.QtWidgets import QTableWidgetItem, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize


def set_user_table(window, users):
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
    item = QListWidgetItem()
    item.setText(f"{sender} -> {recipient}: file: {filename}\nFileID: {fileid}")
    window.msgList.addItem(item)
    window.msgList.scrollToItem(item)

def add_image(window, image):
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
    file, _ = QFileDialog.getOpenFileName(None,
        filter = (
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff *gif);; All Files (*)"
            )
    )
    if not file:
        return None
    return file

def get_save_file():
    file, _ = QFileDialog.getSaveFileName(None,
        filter = ("All Files (*)")
    )
    if not file:
        return None
    return file
