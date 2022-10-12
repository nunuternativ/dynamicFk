# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\core\rf_maya\nuTools\util\dynamicFk\ui\newSystem.ui'
#
# Created: Fri Jan 04 11:57:42 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_newSystem_Dialog(object):
    def setupUi(self, newSystem_Dialog):
        newSystem_Dialog.setObjectName("newSystem_Dialog")
        newSystem_Dialog.resize(260, 91)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(newSystem_Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.newSystem_gridLayout = QtWidgets.QGridLayout()
        self.newSystem_gridLayout.setSpacing(1)
        self.newSystem_gridLayout.setObjectName("newSystem_gridLayout")
        self.startFrame_label = QtWidgets.QLabel(newSystem_Dialog)
        self.startFrame_label.setObjectName("startFrame_label")
        self.newSystem_gridLayout.addWidget(self.startFrame_label, 1, 0, 1, 1)
        self.sysName_lineEdit = QtWidgets.QLineEdit(newSystem_Dialog)
        self.sysName_lineEdit.setObjectName("sysName_lineEdit")
        self.newSystem_gridLayout.addWidget(self.sysName_lineEdit, 0, 1, 1, 1)
        self.sysName_label = QtWidgets.QLabel(newSystem_Dialog)
        self.sysName_label.setObjectName("sysName_label")
        self.newSystem_gridLayout.addWidget(self.sysName_label, 0, 0, 1, 1)
        self.startFrame_lineEdit = QtWidgets.QLineEdit(newSystem_Dialog)
        self.startFrame_lineEdit.setObjectName("startFrame_lineEdit")
        self.newSystem_gridLayout.addWidget(self.startFrame_lineEdit, 1, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.newSystem_gridLayout)
        self.buttons_verticalLayout = QtWidgets.QVBoxLayout()
        self.buttons_verticalLayout.setObjectName("buttons_verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.buttons_verticalLayout.addItem(spacerItem)
        self.ok_pushButton = QtWidgets.QPushButton(newSystem_Dialog)
        self.ok_pushButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.buttons_verticalLayout.addWidget(self.ok_pushButton)
        self.cancel_pushButton = QtWidgets.QPushButton(newSystem_Dialog)
        self.cancel_pushButton.setFocusPolicy(QtCore.Qt.TabFocus)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.buttons_verticalLayout.addWidget(self.cancel_pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.buttons_verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.buttons_verticalLayout)

        self.retranslateUi(newSystem_Dialog)
        QtCore.QObject.connect(self.ok_pushButton, QtCore.SIGNAL("clicked()"), newSystem_Dialog.accept)
        QtCore.QObject.connect(self.cancel_pushButton, QtCore.SIGNAL("clicked()"), newSystem_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(newSystem_Dialog)

    def retranslateUi(self, newSystem_Dialog):
        newSystem_Dialog.setWindowTitle(QtWidgets.QApplication.translate("newSystem_Dialog", "New System", None, -1))
        self.startFrame_label.setText(QtWidgets.QApplication.translate("newSystem_Dialog", "Start Frame", None, -1))
        self.sysName_lineEdit.setText(QtWidgets.QApplication.translate("newSystem_Dialog", "name", None, -1))
        self.sysName_label.setText(QtWidgets.QApplication.translate("newSystem_Dialog", "System Name", None, -1))
        self.startFrame_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("newSystem_Dialog", "1.00", None, -1))
        self.ok_pushButton.setText(QtWidgets.QApplication.translate("newSystem_Dialog", "OK", None, -1))
        self.cancel_pushButton.setText(QtWidgets.QApplication.translate("newSystem_Dialog", "Cancel", None, -1))

