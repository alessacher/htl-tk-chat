#! /usr/bin/python3

"""The Chat Client

This is the chat client with Qt6 frontend.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
import os.path
from userstub import * #beware bad code style

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

if __name__ == "__main__":
  app = QApplication(sys.argv)
  #app.setStyle('Fusion') # only Windows or Fusion

  ui_file_name = "mainwindow.ui"

  script_path = os.path.realpath(__file__)
  script_path_list = script_path.split("/")
  script_path_list[-1] = ui_file_name
  ui_path = "/".join(script_path_list)
  if os.path.exists(ui_path):
    window = uic.loadUi(ui_path)
  else:
    print(f"Cannot open {ui_path}: No such file or directory")
    sys.exit(1)

  window.InputBar.returnPressed.connect(send_msg)
  test_user_table(window)
  test_combo_box(window)
  window.show()

  sys.exit(app.exec())
