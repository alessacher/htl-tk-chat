"""
This is just a stub for users since other functionalities
are not implemented at the moment.
"""
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtGui import QColor

test_users = [ ("Hans","10.0.0.1")
             , ("Klaus","10.0.0.2")
             , ("Peter","192.168.1.3")
             ]

def test_connection(ip):
  """Test the Connection

  pings the ip to get the connction status.
  Not implemented at the moment.
  """
  return ip[1] == '0'

# setup ChatList :: QTableWidget on the left side of the window
def test_user_table(window):
  """
  Adds test users to the table

  This function adds test users to the QTableWidget
  on the left side of the window.
  """
  table = window.chatList
  table.setRowCount(len(test_users))
  table.setColumnCount(len(test_users[0]) + 1)
  table.setHorizontalHeaderLabels(["Name", "ip", "connected"])

  for i, (name, ip) in enumerate(test_users):
    item_name = QTableWidgetItem(name)
    item_ip = QTableWidgetItem(ip)
    user_online = test_connection(ip)
    item_status = QTableWidgetItem(str(user_online))
    if user_online:
      status_color = QColor('#80005500')
    else:
      status_color = QColor('#80ff3737')
    item_status.setBackground(status_color)

    table.setItem(i, 0, item_name)
    table.setItem(i, 1, item_ip)
    table.setItem(i, 2, item_status)

# setup userSelect :: QComboBox on the left of the InputBar :: QLineEdit
def test_combo_box(window):
  """Adds test users to the Combo Box

  This function adds test users to the QComboBox
  on the left side of the InputBar.
  """
  users = [x[0] for x in test_users]
  window.userSelect.addItems(users)
