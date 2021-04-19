from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtGui import QColor

# python doesn't accept tuples as input,
# it can't do lambda (a,b): a
def fst(x):
  (a,_) = x
  return a

test_users = [ ("Hans","10.0.0.1")
             , ("Klaus","10.0.0.2")
             , ("Peter","192.168.1.3")
             ]

def test_connection(ip):
  #ping ip stub
  return ip[1] == '0'

# setup ChatList :: QTableWidget on the left side of the window
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
      status_color = QColor('#80005500')
    else:
      status_color = QColor('#80ff3737')
    item_status.setBackground(status_color)

    table.setItem(i, 0, item_name)
    table.setItem(i, 1, item_ip)
    table.setItem(i, 2, item_status)

# setup userSelect :: QComboBox on the left of the InputBar :: QLineEdit
def test_combo_box(window):
  users = list(map(fst,test_users))
  window.userSelect.addItems(users)
