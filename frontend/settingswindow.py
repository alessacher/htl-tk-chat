# Form implementation generated from reading ui file 'ui_files/settingswindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(700, 350)
        self.centralWidget = QtWidgets.QWidget(SettingsWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.MainButtonsLayout = QtWidgets.QHBoxLayout()
        self.MainButtonsLayout.setObjectName("MainButtonsLayout")
        self.ButtonSaveProfile = QtWidgets.QPushButton(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonSaveProfile.sizePolicy().hasHeightForWidth())
        self.ButtonSaveProfile.setSizePolicy(sizePolicy)
        self.ButtonSaveProfile.setObjectName("ButtonSaveProfile")
        self.MainButtonsLayout.addWidget(self.ButtonSaveProfile)
        self.ButtonLoadProfile = QtWidgets.QPushButton(self.centralWidget)
        self.ButtonLoadProfile.setObjectName("ButtonLoadProfile")
        self.MainButtonsLayout.addWidget(self.ButtonLoadProfile)
        self.ButtonDeleteProfile = QtWidgets.QPushButton(self.centralWidget)
        self.ButtonDeleteProfile.setObjectName("ButtonDeleteProfile")
        self.MainButtonsLayout.addWidget(self.ButtonDeleteProfile)
        self.gridLayout.addLayout(self.MainButtonsLayout, 6, 0, 1, 5)
        self.MainTabBar = QtWidgets.QTabWidget(self.centralWidget)
        self.MainTabBar.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.MainTabBar.setIconSize(QtCore.QSize(20, 20))
        self.MainTabBar.setObjectName("MainTabBar")
        self.TabInformation = QtWidgets.QWidget()
        self.TabInformation.setObjectName("TabInformation")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.TabInformation)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_2 = QtWidgets.QCheckBox(self.TabInformation)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout.addWidget(self.checkBox_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.AuthLayout = QtWidgets.QHBoxLayout()
        self.AuthLayout.setObjectName("AuthLayout")
        self.ConncetionLabel = QtWidgets.QLabel(self.TabInformation)
        self.ConncetionLabel.setAlignment(QtCore.Qt.Alignment.AlignRight|QtCore.Qt.Alignment.AlignTrailing|QtCore.Qt.Alignment.AlignVCenter)
        self.ConncetionLabel.setObjectName("ConncetionLabel")
        self.AuthLayout.addWidget(self.ConncetionLabel)
        self.InputServerAddress = QtWidgets.QLineEdit(self.TabInformation)
        self.InputServerAddress.setStatusTip("")
        self.InputServerAddress.setWhatsThis("")
        self.InputServerAddress.setInputMask("")
        self.InputServerAddress.setText("")
        self.InputServerAddress.setReadOnly(False)
        self.InputServerAddress.setObjectName("InputServerAddress")
        self.AuthLayout.addWidget(self.InputServerAddress)
        self.InputPort = QtWidgets.QLineEdit(self.TabInformation)
        self.InputPort.setText("")
        self.InputPort.setObjectName("InputPort")
        self.AuthLayout.addWidget(self.InputPort)
        self.InputUsername = QtWidgets.QLineEdit(self.TabInformation)
        self.InputUsername.setText("")
        self.InputUsername.setObjectName("InputUsername")
        self.AuthLayout.addWidget(self.InputUsername)
        self.InputPassword = QtWidgets.QLineEdit(self.TabInformation)
        self.InputPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.InputPassword.setObjectName("InputPassword")
        self.AuthLayout.addWidget(self.InputPassword)
        self.ButtonStartConnection = QtWidgets.QPushButton(self.TabInformation)
        self.ButtonStartConnection.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.ButtonStartConnection.setObjectName("ButtonStartConnection")
        self.AuthLayout.addWidget(self.ButtonStartConnection)
        self.ButtonEndConnection = QtWidgets.QPushButton(self.TabInformation)
        self.ButtonEndConnection.setObjectName("ButtonEndConnection")
        self.AuthLayout.addWidget(self.ButtonEndConnection)
        self.gridLayout_2.addLayout(self.AuthLayout, 5, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.MainTabBar.addTab(self.TabInformation, "")
        self.TabSettings = QtWidgets.QWidget()
        self.TabSettings.setObjectName("TabSettings")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.TabSettings)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.SettingsTabBar = QtWidgets.QToolBox(self.TabSettings)
        self.SettingsTabBar.setObjectName("SettingsTabBar")
        self.gridLayout_4.addWidget(self.SettingsTabBar, 0, 0, 1, 1)
        self.MainTabBar.addTab(self.TabSettings, "")
        self.gridLayout.addWidget(self.MainTabBar, 2, 0, 1, 5)
        SettingsWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(SettingsWindow)
        self.MainTabBar.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings"))
        self.ButtonSaveProfile.setText(_translate("SettingsWindow", "Save Profile"))
        self.ButtonLoadProfile.setText(_translate("SettingsWindow", "Load Profile"))
        self.ButtonDeleteProfile.setText(_translate("SettingsWindow", "Delete Profile"))
        self.checkBox_2.setText(_translate("SettingsWindow", "CheckBox"))
        self.ConncetionLabel.setText(_translate("SettingsWindow", "Connect to server"))
        self.InputServerAddress.setToolTip(_translate("SettingsWindow", "IP-Address of the server in dotted decimal, Port is optional"))
        self.InputServerAddress.setPlaceholderText(_translate("SettingsWindow", "ip:port"))
        self.InputPort.setPlaceholderText(_translate("SettingsWindow", "Port"))
        self.InputUsername.setToolTip(_translate("SettingsWindow", "Your Username to connect to the chat-server"))
        self.InputUsername.setPlaceholderText(_translate("SettingsWindow", "Username"))
        self.InputPassword.setToolTip(_translate("SettingsWindow", "Your Password for your User"))
        self.InputPassword.setPlaceholderText(_translate("SettingsWindow", "Password"))
        self.ButtonStartConnection.setToolTip(_translate("SettingsWindow", "Establish a Connection to the Server with the provided informaiton"))
        self.ButtonStartConnection.setText(_translate("SettingsWindow", "Connect"))
        self.ButtonEndConnection.setToolTip(_translate("SettingsWindow", "Disconnect from the Serve, abort connection"))
        self.ButtonEndConnection.setText(_translate("SettingsWindow", "Disconnect"))
        self.MainTabBar.setTabText(self.MainTabBar.indexOf(self.TabInformation), _translate("SettingsWindow", "Information"))
        self.MainTabBar.setTabText(self.MainTabBar.indexOf(self.TabSettings), _translate("SettingsWindow", "Settings"))