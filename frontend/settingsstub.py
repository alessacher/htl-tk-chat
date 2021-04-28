from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication
import os.path
from PyQt6 import QtWidgets, uic # .ui files and their content
import re # regex
from PyQt6.QtCore import Qt
from PyQt6 import QtGui # cursor shapes
import time

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
  if not re.match('(?:[0-9]{1,3}\.){3}[0-9]{1,3}',ip):
    # checks for dotted-decimal compliance (Syntax)
    # no range (0-255) checking (Semantics)

    # should we include checks for semantics in this stage
    #  or postpone it to the backend and forward the error it will cause ?
    print("ip adress Syntax is incorrect !")
  else :
    print(f"stub connecting to server '{ip}'")
    settings.InputServerAddress.setReadOnly(True)
    # setting cursor does not take effect immediately but on function exit ?!
    # unusable in current form as cursor effectively gets not changed ...
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


