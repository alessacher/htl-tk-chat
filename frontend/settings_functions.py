"""Settings Module
functions behind the settings window ui-elements
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

import client
sys.path.append('../client')
import chat_client
import client_functions

dir = os.path.dirname(__file__)
config_file = os.path.join(dir, "../client/client.conf")
config = configparser.ConfigParser() # client config file
config.read(config_file)

connected = False

@Slot()
def save_frontend_config(settings):
  """Save the settings values to a .config file"""
  logging.info(f"Saving current settings to {config_file}...")
  user = settings.InputUsername.text()
  addr = settings.InputServerAddress.text() # ip or hostname
  port = settings.InputPort.text()
  if re.match("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$",addr):
    logging.info(f"Got dotted decimal addr from settings-panel {addr}")
  elif re.match("^\w*\.(\w*|\.)*$",addr):
    logging.info(f"Got hostname from settings-panel: {addr}")
  config.read(config_file)
  if(not config.has_section("frontend")):
    logging.info(f"No 'frontend' section found in {config_file}, creating one")
    config.add_section("frontend")
  config.set("frontend", "host", addr)
  config.set("frontend", "port", port)
  config.set("frontend", "user", user)
  config.write(open(config_file,'w'))

@Slot()
def delete_frontend_config(settings):
  """Delete the settings values in the .config file."""
  logging.info(f"Clearing frontend section in {config_file}...")
  if(config.has_section("frontend")):
    config["frontend"].clear()
  else: logging.warning("No 'frontend' section found to delete, skipping")
  config.write(open(config_file,'w'))

@Slot()
def load_frontend_config(settings):
  """Load the values stored in the .config file for frontend settings"""
  logging.info(f"Loading .config Profile")
  try:
    host = config.get("frontend", "host")
    user = config.get("frontend", "user")
  except:
    logging.error("No or empty 'frontend' section found in {config_file} !")
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

  global connected

  if connected == False:
    addr = settings.InputServerAddress.text()
    port = int(settings.InputPort.text())
    username = settings.InputUsername.text()

    logging.info(f"stub connecting to server '{addr}:{port}'")
    settings.InputServerAddress.setReadOnly(True)
    settings.InputPort.setReadOnly(True)
    settings.InputUsername.setReadOnly(True)
    settings.InputPassword.setReadOnly(True)
    chat_client.init_backend(addr, port, username)
    connected = True


@Slot()
def disconnect_server(settings):
  """Disconnect from a chat server

  Disconnect from a chat server via the settings window.
  This function is called when the user presses the 'Disconnect'
  button for server connection in the settings window.
  The function is a stub.
  """

  global connected

  if connected == True:
    connected = False
    addr = settings.InputServerAddress.text()
    print(f"stub disconnecting from server '{addr}'")
    settings.InputServerAddress.setReadOnly(False)
    settings.InputPort.setReadOnly(False)
    settings.InputUsername.setReadOnly(False)
    settings.InputPassword.setReadOnly(False)
    logging.info(f"frontend disconnecting from server '{addr}'")
    client_functions.close_connection(chat_client.my_client.sock)


def init_settings_window(settings):
  """Initialize settings-window
  Actions and signals are being connected to their Slots
  """
  settings.ButtonStartConnection.pressed.connect(lambda: connect_server(settings))
  settings.ButtonEndConnection.pressed.connect(lambda: disconnect_server(settings))
  settings.ButtonSaveProfile.pressed.connect(lambda: save_frontend_config(settings))
  settings.ButtonDeleteProfile.pressed.connect(lambda: delete_frontend_config(settings))
  settings.ButtonLoadProfile.pressed.connect(lambda: load_frontend_config(settings))

  settings.InputServerAddress.setText(chat_client.host)
  settings.InputPort.setText(str(chat_client.port))
  settings.InputUsername.setText(chat_client.user)



