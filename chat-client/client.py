#! /usr/bin/python3

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtCore import Slot
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
  ui_file_name = "mainwindow.ui"

  script_path = os.path.realpath(__file__)
  script_path_list = script_path.split("/")
  script_path_list[-1] = ui_file_name
  ui_path = "/".join(script_path_list)
  if os.path.exists(ui_path):
    ui_file = QFile(ui_path)
  else:
    print(f"Cannot open {ui_path}: No such file or directory")
    sys.exit(1)

  loader = QUiLoader()
  window = loader.load(ui_file)
  ui_file.close()
  if not window:
      print(loader.errorString())
      sys.exit(-1)
  window.InputBar.returnPressed.connect(send_msg)
  test_user_table(window)
  test_combo_box(window)
  window.show()

  sys.exit(app.exec_())
