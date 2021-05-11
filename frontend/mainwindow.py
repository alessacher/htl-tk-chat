# Form implementation generated from reading ui file 'ui_files/mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModality.NonModal)
        MainWindow.resize(707, 606)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui_files/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.userSelect = QtWidgets.QComboBox(self.centralwidget)
        self.userSelect.setObjectName("userSelect")
        self.horizontalLayout.addWidget(self.userSelect)
        self.InputBar = QtWidgets.QLineEdit(self.centralwidget)
        self.InputBar.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.InputBar.setStatusTip("")
        self.InputBar.setAutoFillBackground(False)
        self.InputBar.setStyleSheet("")
        self.InputBar.setInputMethodHints(QtCore.Qt.InputMethodHints.ImhNone)
        self.InputBar.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.InputBar.setCursorPosition(0)
        self.InputBar.setReadOnly(False)
        self.InputBar.setClearButtonEnabled(True)
        self.InputBar.setObjectName("InputBar")
        self.horizontalLayout.addWidget(self.InputBar)
        self.addFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.addFileButton.setCheckable(False)
        self.addFileButton.setChecked(False)
        self.addFileButton.setObjectName("addFileButton")
        self.horizontalLayout.addWidget(self.addFileButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.msgList = QtWidgets.QListWidget(self.centralwidget)
        self.msgList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.msgList.setAutoScrollMargin(0)
        self.msgList.setEditTriggers(QtWidgets.QAbstractItemView.EditTriggers.NoEditTriggers)
        self.msgList.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.NoDragDrop)
        self.msgList.setDefaultDropAction(QtCore.Qt.DropActions.CopyAction)
        self.msgList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.msgList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.msgList.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.msgList.setProperty("isWrapping", False)
        self.msgList.setResizeMode(QtWidgets.QListView.ResizeMode.Adjust)
        self.msgList.setWordWrap(True)
        self.msgList.setObjectName("msgList")
        self.gridLayout.addWidget(self.msgList, 0, 1, 1, 1)
        self.chatList = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chatList.sizePolicy().hasHeightForWidth())
        self.chatList.setSizePolicy(sizePolicy)
        self.chatList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.chatList.setEditTriggers(QtWidgets.QAbstractItemView.EditTriggers.NoEditTriggers)
        self.chatList.setTextElideMode(QtCore.Qt.TextElideMode.ElideNone)
        self.chatList.setObjectName("chatList")
        self.chatList.setColumnCount(0)
        self.chatList.setRowCount(0)
        self.chatList.horizontalHeader().setCascadingSectionResizes(True)
        self.gridLayout.addWidget(self.chatList, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 707, 35))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionServer = QtGui.QAction(MainWindow)
        self.actionServer.setObjectName("actionServer")
        self.menuFile.addAction(self.actionExport)
        self.menuSettings.addAction(self.actionServer)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.InputBar.setToolTip(_translate("MainWindow", "Enter Text here to send"))
        self.InputBar.setPlaceholderText(_translate("MainWindow", "Enter message to send"))
        self.addFileButton.setText(_translate("MainWindow", "attach"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuSettings.setTitle(_translate("MainWindow", "&Settings"))
        self.actionExit.setText(_translate("MainWindow", "E&xit"))
        self.actionExport.setText(_translate("MainWindow", "&Export"))
        self.actionServer.setText(_translate("MainWindow", "Server"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
