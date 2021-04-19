#! /usr/bin/python3

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
import os.path
from userstub import *

@Slot()
def send_msg():
  u = window.userSelect.currentText()
  t = window.InputBar.text()
  print(f"stub sending message '{t}' to '{u}'")
  window.msgList.addItem(f"<you> -> {u}: "+t)
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
    window = uic.loadUi("mainwindow.ui")
  else:
    print(f"Cannot open {ui_path}: No such file or directory")
    sys.exit(1)

  window.InputBar.returnPressed.connect(send_msg)
  test_user_table(window)
  test_combo_box(window)
  window.show()

  sys.exit(app.exec())
