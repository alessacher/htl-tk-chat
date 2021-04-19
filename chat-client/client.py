import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
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
  window = uic.loadUi("mainwindow.ui")
  if not window:
      print("Cannot find mainwindow.ui")
      sys.exit(-1)
  window.InputBar.returnPressed.connect(send_msg)
  test_user_table(window)
  test_combo_box(window)
  window.show()

  sys.exit(app.exec())
