"""
This is just a stub for users since other functionalities
are not implemented at the moment.
"""
import base64
from genericpath import exists
import logging
import logging.config
import os.path
from sys import path_importer_cache
from PIL import Image
from PyQt6.QtWidgets import QTableWidgetItem, QListWidgetItem, QFileDialog
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot


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
    window.msgList.addItem(f"{sender} -> {recipient}: {message}")

def add_image(window, image):
  listwidget = window.msgList
  listitem = QListWidgetItem()
  if os.path.exists(image):
    im = Image.open(image)
    w, h = im.size
    w, h = min(w, 1000), min(h, 1000)
    icon = QIcon(image)
    size = QSize(w, h)
  else:
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(image))
    icon = QIcon(pixmap)
    size = pixmap.size()
    w, h = size.width(), size.height()
    w, h = min(w, 1000), min(h, 1000)
    size = QSize(w, h)

  listitem.setSizeHint(size)
  listitem.setIcon(icon)
  listwidget.setIconSize(size)
  listwidget.addItem(listitem)

def get_image_file():
  try:
    file = QFileDialog.getOpenFileName(
      filter = ("Images (*.png *.jpg *.jpeg *.bmp *.svg *.tiff);; All Files (*)")
    )
  except Exception:
    pass
  return file[0]

