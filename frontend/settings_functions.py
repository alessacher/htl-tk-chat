"""Settings Module
functions behind the settings window ui-elements
"""
import logging
import logging.config
from PyQt5.QtCore import pyqtSlot as Slot # ui elements communication
import os.path
from os import chdir
import configparser
import sys

import client
sys.path.append('../client')
import backend
import client_functions

dir = os.path.dirname(__file__)
chdir(dir)
config_file = "../client/client.conf"
config = configparser.ConfigParser() # client config file
config.read(config_file)

connected = False

@Slot()
def save_frontend_config(settings):
  """Save the settings values to a .config file"""
  logging.info(f"Saving current settings to {config_file}...")
  user = settings.InputUsername.text()
  addr = settings.InputServerAddress.text()
  port = settings.InputPort.text()
  config.read(config_file)
  if(not config.has_section("frontend")):
    logging.info(f"No 'frontend' section found in {config_file}, creating one")
    config.add_section("frontend")
  config.set("frontend", "host", addr)
  config.set("frontend", "port", port)
  config.set("frontend", "user", user)

  en_ssl = str(settings.SSLCheckBox.isChecked())
  config.set("SSL", "enable_ssl", en_ssl)

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
    port = config.get("frontend", "port")
    en_ssl = config.getboolean("SSL", "enable_ssl")
  except:
    logging.error("No or empty 'frontend' section found in {config_file} !")
    return

  settings.InputServerAddress.setText(host)
  settings.InputUsername.setText(user)
  settings.InputPort.setText(port)
  settings.SSLCheckBox.setChecked(en_ssl)
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
    en_ssl = settings.SSLCheckBox.isChecked()

    settings.InputServerAddress.setReadOnly(True)
    settings.InputPort.setReadOnly(True)
    settings.InputUsername.setReadOnly(True)

    backend.init_backend(addr, port, username, en_ssl)
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

    settings.InputServerAddress.setReadOnly(False)
    settings.InputPort.setReadOnly(False)
    settings.InputUsername.setReadOnly(False)

    logging.info(f"frontend disconnecting from server '{addr}'")
    client_functions.close_connection(backend.my_client.sock)


def init_settings_window(settings):
  """Initialize settings-window
  Actions and signals are being connected to their Slots
  """
  settings.ButtonStartConnection.pressed.connect(lambda: connect_server(settings))
  settings.ButtonEndConnection.pressed.connect(lambda: disconnect_server(settings))
  settings.ButtonSaveProfile.pressed.connect(lambda: save_frontend_config(settings))
  settings.ButtonDeleteProfile.pressed.connect(lambda: delete_frontend_config(settings))
  settings.ButtonLoadProfile.pressed.connect(lambda: load_frontend_config(settings))

  settings.InputServerAddress.setText(backend.host)
  settings.InputPort.setText(str(backend.port))
  settings.InputUsername.setText(backend.user)



