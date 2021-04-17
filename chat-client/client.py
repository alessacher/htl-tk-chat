import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtCore import Slot

@Slot()
def send_msg():
  t = window.InputBar.text()
  print(f"stub sending message '{t}'")
  window.InputBar.clear()

if __name__ == "__main__":
  app = QApplication(sys.argv)

  ui_file = QFile("mainwindow.ui")
  if not ui_file.open(QIODevice.ReadOnly):
      print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
      sys.exit(-1)
  loader = QUiLoader()
  window = loader.load(ui_file)
  ui_file.close()
  if not window:
      print(loader.errorString())
      sys.exit(-1)
  window.InputBar.returnPressed.connect(send_msg)
  window.show()


  sys.exit(app.exec_())