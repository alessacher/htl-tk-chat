"""Settings stub
Stub for settings window since server is not yet implemented.
"""
import logging
import logging.config
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot # ui elements communication
import os.path
from PyQt6 import QtWidgets, uic # .ui files and their content
import re # regex
from PyQt6.QtCore import Qt
from PyQt6 import QtGui # cursor shapes
import time
import hashlib
import configparser
import sys

sys.path.append('../client')
import chat_client 
import client_functions 

dir = os.path.dirname(__file__)
config_file = os.path.join(dir, "../client/client.conf")
config = configparser.ConfigParser() # client config file
config.read(config_file)

@Slot()
def save_frontend_config(settings):
  """Save the settings values to a .config file"""
  logging.info(f"Saving current settings to {config_file}...")
  user = settings.InputUsername.text()
  (ip,port) = re.split("\:",settings.InputServerAddress.text(),1)
  config.read(config_file)
  if(not config.has_section("frontend")):
    logging.info("No Config section found, creating one")
    config.add_section("frontend")
  config.set("frontend", "host", ip)
  config.set("frontend", "port", port)
  config.set("frontend", "user", user)
  config.write(open(config_file,'w'))
  
@Slot()
def delete_frontend_config(settings):
  """Delete the settings values in the .config file."""
  logging.info(f"Clearing frontend section in {config_file}...")
  if(config.has_section("frontend")):
    config["frontend"].clear()
  else: logging.warning("No frontend section found do delete, skipping")
  config.write(open(config_file,'w'))

@Slot()
def load_frontend_config(settings):
  """Load the values stored in the .config file for frontend settings"""
  logging.info(f"Loading .config Profile")
  try:
    host = config.get("frontend", "host") + ':' + config.get("frontend", "port")
    user = config.get("frontend", "user")
  except: 
    logging.error("No or empty frontend section found !")
    return
  settings.InputServerAddress.setText(host)
  settings.InputUsername.setText(user)
  logging.info(f"frontend loaded user {user}, host {host}")



@Slot()
def connect_server(settings):
  """Connect to a chat server

  Connect to a chat server via the settings window and the
  information provided through the same window.
  This function is called when the user presses the 'Connect'
  button in the settings window.
  The function is a stub.
  """
  ip = settings.InputServerAddress.text()
  if (not re.match('((?:\d{1,3}\.){3}\d{1,3})((?:\:\d{1,5})|())',ip)):
    # checks for dotted-decimal : port (optional) compliance -> (Syntax)
    # no range (0-255) checking -> (Semantics)
    # should we include checks for semantics in this stage or postpone it to the backend and forward the error it will cause ?
    logging.error("ip adress Syntax is incorrect !")
  else:
    logging.info(f"stub connecting to server '{ip}'")
    settings.InputServerAddress.setReadOnly(True)
    # setting cursor does not take effect immediately but on function exit ?!
    # unusable in current form as cursor starts showing when connection is finished
    #settings.setCursor(QtGui.QCursor(Qt.CursorShape.BusyCursor))
    time.sleep(0.5)
    settings.ConnectionProgressBar.setValue(50)
    #client_functions.authenticate(chat_client.my_client.sock, chat_client.user)
    chat_client.init_backend()
    time.sleep(0.5)
    settings.ConnectionProgressBar.setValue(100)
    #settings.setCursor(QtGui.QCursor(Qt.CursorShape.ArrowCursor))

@Slot()
def disconnect_server(settings):
  """Disconnect from a chat server

  Disconnect from a chat server via the settings window.
  This function is called when the user presses the 'Disconnect'
  button for server connection in the settings window.
  The function is a stub.
  """
  ip = settings.InputServerAddress.text()
  print(f"stub disconnecting from server '{ip}'")
  settings.ConnectionProgressBar.setValue(0)
  settings.InputServerAddress.setReadOnly(False)
  settings.InputUsername.setReadOnly(False)
  settings.InputPassword.setReadOnly(False)
  logging.info(f"frontend disconnecting from server '{ip}'")
  client_functions.close_connection(chat_client.my_client.sock)


def init_settings_window(settings):
  """Initialize settings-window
  Initialize functionality of settings-window elements
  Mainly, actions and signals are being connected to their Slots
  """
  settings.ConnectionProgressBar.setValue(0)
  settings.ButtonStartConnection.pressed.connect(lambda: connect_server(settings))
  settings.ButtonEndConnection.pressed.connect(lambda: disconnect_server(settings))
  settings.ButtonSaveProfile.pressed.connect(lambda: save_frontend_config(settings))
  settings.ButtonDeleteProfile.pressed.connect(lambda: delete_frontend_config(settings))
  settings.ButtonLoadProfile.pressed.connect(lambda: load_frontend_config(settings))


