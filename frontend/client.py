#! /usr/bin/python3

"""The Chat Client

This is the chat client with Qt6 frontend.
"""

import sys
import os.path
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, uic # .ui files and their content
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication
from PyQt6.QtCore import Qt
from PyQt6 import QtGui # cursor shapes

from userstub import *
from settingsstub import *

import time
import re # regex



@Slot()
def connect_server():
  """Connect to a chat server

  Connect to a chat server via the settings window and the
  information provided through the same window.
  This function is called when the user presses the 'Connect'
  button in the settings window.
  The function is a stub.
  """
  ip = settings.InputServerAddress.text()
  if not re.match('((?:\d{1,3}\.){3}\d{1,3})((?:\:\d{1,5})|())',ip):
    # checks for dotted-decimal : port (optional) compliance -> (Syntax)
    # no range (0-255) checking -> (Semantics)

    # should we include checks for semantics in this stage
    #  or postpone it to the backend and forward the error it will cause ?
    print("ip adress Syntax is incorrect !")
  else :
    print(f"stub connecting to server '{ip}'")
    settings.InputServerAddress.setReadOnly(True)
    # setting cursor does not take effect immediately but on function exit ?!
    # unusable in current form as cursor starts showing when connection is finished
    settings.setCursor(QtGui.QCursor(Qt.CursorShape.BusyCursor))
    time.sleep(0.5)
    settings.ConnectionProgressBar.setValue(50)
    time.sleep(0.5)
    settings.ConnectionProgressBar.setValue(100)
    #settings.setCursor(QtGui.QCursor(Qt.CursorShape.ArrowCursor))


@Slot()
def disconnect_server():
  """Disconnect to a chat server

  Disconnect from a chat server via the settings window.
  This function is called when the user presses the 'Cancel'
  button for server connection in the settings window.
  The function is a stub.
  """
  ip = settings.InputServerAddress.text()
  print(f"stub disconnecting from server '{ip}'")
  settings.ConnectionProgressBar.setValue(0)
  settings.InputServerAddress.setReadOnly(False)


@Slot()
def send_msg():
  """Send message function

  This function is called when the user presses Enter,
  to send the message. The function isn't fully implemented
  at the moment.
  """
  r = window.userSelect.currentText()
  t = window.InputBar.text()
  if r == "All":
    print(f"stub broadcasting message '{t}'")
  else:
    print(f"stub sending message '{t}' to '{r}'")
  window.msgList.addItem(f"<you> -> {r}: "+t)
  window.InputBar.clear()


def load_ui_file(filename):
  """UI File Loader

  Path independent loader function for QTCreators .ui files
  """
  ui_file_name = filename
  script_path = os.path.realpath(__file__)
  script_path_list = script_path.split("/")
  script_path_list[-1] = ui_file_name
  ui_path = "/".join(script_path_list)
  if os.path.exists(ui_path):
    return uic.loadUi(ui_path)
  else:
    print(f"Cannot open {ui_path}: No such file or directory")
    sys.exit(1)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  #app.setStyle('Fusion') # only Windows or Fusion

  window = load_ui_file("mainwindow.ui")
  window.InputBar.returnPressed.connect(send_msg)
  test_user_table(window)
  test_combo_box(window)
  window.show()

  settings = load_ui_file("settingswindow.ui")
  window.actionServer.triggered.connect(settings.show)
  init_settings_window(settings)

  sys.exit(app.exec())
