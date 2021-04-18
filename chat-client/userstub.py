from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt

# python doesn't accept tuples as input,
# it can't do lambda (a,b): a
def fst(pair):
  (a,b) = pair
  return a


test_users = [ ("Hans","10.0.0.1")
             , ("Klaus","10.0.0.2")
             , ("Peter","192.168.1.3")
             ]

def test_connection(ip):
  #ping ip stub
  return ip[1] == '0'

# setup user table on the left
def test_user_table(window):
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
      status_color = Qt.darkGreen
    else:
      status_color = Qt.darkRed
    item_status.setBackground(status_color)

    table.setItem(i, 0, item_name)
    table.setItem(i, 1, item_ip)
    table.setItem(i, 2, item_status)

def test_combo_box(window):
  users = list(map(fst,test_users))
  window.userSelect.addItems(users)
