# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\core\rf_maya\nuTools\util\dynamicFk\ui\bake.ui'
#
# Created: Wed Jul 24 19:05:09 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_bake_dialog(object):
    def setupUi(self, bake_dialog):
        bake_dialog.setObjectName("bake_dialog")
        bake_dialog.setWindowModality(QtCore.Qt.WindowModal)
        bake_dialog.resize(187, 127)
        self.verticalLayout = QtWidgets.QVBoxLayout(bake_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.startEnd_gridLayout = QtWidgets.QGridLayout()
        self.startEnd_gridLayout.setSpacing(10)
        self.startEnd_gridLayout.setObjectName("startEnd_gridLayout")
        self.startFrame_lineEdit = QtWidgets.QLineEdit(bake_dialog)
        self.startFrame_lineEdit.setObjectName("startFrame_lineEdit")
        self.startEnd_gridLayout.addWidget(self.startFrame_lineEdit, 0, 1, 1, 1)
        self.endFrame_lineEdit = QtWidgets.QLineEdit(bake_dialog)
        self.endFrame_lineEdit.setObjectName("endFrame_lineEdit")
        self.startEnd_gridLayout.addWidget(self.endFrame_lineEdit, 1, 1, 1, 1)
        self.endFrame_label = QtWidgets.QLabel(bake_dialog)
        self.endFrame_label.setObjectName("endFrame_label")
        self.startEnd_gridLayout.addWidget(self.endFrame_label, 0, 0, 1, 1)
        self.startFrame_label = QtWidgets.QLabel(bake_dialog)
        self.startFrame_label.setObjectName("startFrame_label")
        self.startEnd_gridLayout.addWidget(self.startFrame_label, 1, 0, 1, 1)
        self.startEnd_gridLayout.setColumnStretch(0, 1)
        self.verticalLayout.addLayout(self.startEnd_gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.simplifyCurve_checkBox = QtWidgets.QCheckBox(bake_dialog)
        self.simplifyCurve_checkBox.setObjectName("simplifyCurve_checkBox")
        self.horizontalLayout.addWidget(self.simplifyCurve_checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.bake_buttonBox = QtWidgets.QDialogButtonBox(bake_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bake_buttonBox.sizePolicy().hasHeightForWidth())
        self.bake_buttonBox.setSizePolicy(sizePolicy)
        self.bake_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.bake_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bake_buttonBox.setCenterButtons(False)
        self.bake_buttonBox.setObjectName("bake_buttonBox")
        self.verticalLayout.addWidget(self.bake_buttonBox)

        self.retranslateUi(bake_dialog)
        QtCore.QObject.connect(self.bake_buttonBox, QtCore.SIGNAL("accepted()"), bake_dialog.accept)
        QtCore.QObject.connect(self.bake_buttonBox, QtCore.SIGNAL("rejected()"), bake_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(bake_dialog)

    def retranslateUi(self, bake_dialog):
        bake_dialog.setWindowTitle(QtWidgets.QApplication.translate("bake_dialog", "Bake", None, -1))
        self.endFrame_label.setText(QtWidgets.QApplication.translate("bake_dialog", "Start frame", None, -1))
        self.startFrame_label.setText(QtWidgets.QApplication.translate("bake_dialog", "End frame", None, -1))
        self.simplifyCurve_checkBox.setText(QtWidgets.QApplication.translate("bake_dialog", "Simplify curve", None, -1))

