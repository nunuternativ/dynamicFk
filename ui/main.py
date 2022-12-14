# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\dev\core\rf_maya\nuTools\util\dynamicFk\ui\main.ui'
#
# Created: Mon Jan 28 17:20:44 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DynamicFk_mainWindow(object):
    def setupUi(self, DynamicFk_mainWindow):
        DynamicFk_mainWindow.setObjectName("DynamicFk_mainWindow")
        DynamicFk_mainWindow.setWindowModality(QtCore.Qt.NonModal)
        DynamicFk_mainWindow.resize(364, 535)
        self.centralwidget = QtWidgets.QWidget(DynamicFk_mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.system_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.system_groupBox.setFlat(True)
        self.system_groupBox.setObjectName("system_groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.system_groupBox)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.system_horizontalLayout = QtWidgets.QHBoxLayout()
        self.system_horizontalLayout.setSpacing(5)
        self.system_horizontalLayout.setObjectName("system_horizontalLayout")
        self.system_listWidget = QtWidgets.QListWidget(self.system_groupBox)
        self.system_listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.system_listWidget.setObjectName("system_listWidget")
        self.system_horizontalLayout.addWidget(self.system_listWidget)
        self.systemButtons_verticalLayout = QtWidgets.QVBoxLayout()
        self.systemButtons_verticalLayout.setSpacing(2)
        self.systemButtons_verticalLayout.setObjectName("systemButtons_verticalLayout")
        self.preset_groupBox = QtWidgets.QGroupBox(self.system_groupBox)
        self.preset_groupBox.setObjectName("preset_groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.preset_groupBox)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.savePreset_pushButton = QtWidgets.QPushButton(self.preset_groupBox)
        self.savePreset_pushButton.setObjectName("savePreset_pushButton")
        self.horizontalLayout_3.addWidget(self.savePreset_pushButton)
        self.loadPreset_pushButton = QtWidgets.QPushButton(self.preset_groupBox)
        self.loadPreset_pushButton.setObjectName("loadPreset_pushButton")
        self.horizontalLayout_3.addWidget(self.loadPreset_pushButton)
        self.systemButtons_verticalLayout.addWidget(self.preset_groupBox)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.systemAdd_pushButton = QtWidgets.QPushButton(self.system_groupBox)
        self.systemAdd_pushButton.setObjectName("systemAdd_pushButton")
        self.horizontalLayout_5.addWidget(self.systemAdd_pushButton)
        self.systemRemove_pushButton = QtWidgets.QPushButton(self.system_groupBox)
        self.systemRemove_pushButton.setObjectName("systemRemove_pushButton")
        self.horizontalLayout_5.addWidget(self.systemRemove_pushButton)
        self.systemButtons_verticalLayout.addLayout(self.horizontalLayout_5)
        self.refresh_pushButton = QtWidgets.QPushButton(self.system_groupBox)
        self.refresh_pushButton.setObjectName("refresh_pushButton")
        self.systemButtons_verticalLayout.addWidget(self.refresh_pushButton)
        self.system_horizontalLayout.addLayout(self.systemButtons_verticalLayout)
        self.system_horizontalLayout.setStretch(0, 5)
        self.system_horizontalLayout.setStretch(1, 1)
        self.verticalLayout_4.addLayout(self.system_horizontalLayout)
        self.settings_groupBox = QtWidgets.QGroupBox(self.system_groupBox)
        self.settings_groupBox.setTitle("")
        self.settings_groupBox.setFlat(False)
        self.settings_groupBox.setObjectName("settings_groupBox")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.settings_groupBox)
        self.verticalLayout_9.setSpacing(3)
        self.verticalLayout_9.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.settings_horizontalLayout = QtWidgets.QHBoxLayout()
        self.settings_horizontalLayout.setSpacing(2)
        self.settings_horizontalLayout.setObjectName("settings_horizontalLayout")
        self.slider_verticalLayout = QtWidgets.QVBoxLayout()
        self.slider_verticalLayout.setSpacing(2)
        self.slider_verticalLayout.setObjectName("slider_verticalLayout")
        self.stiffness_groupBox = QtWidgets.QGroupBox(self.settings_groupBox)
        self.stiffness_groupBox.setEnabled(True)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.stiffness_groupBox.setFont(font)
        self.stiffness_groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stiffness_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.stiffness_groupBox.setFlat(True)
        self.stiffness_groupBox.setObjectName("stiffness_groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.stiffness_groupBox)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stiffness_lineEdit = QtWidgets.QLineEdit(self.stiffness_groupBox)
        self.stiffness_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stiffness_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.stiffness_lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.stiffness_lineEdit.setInputMask("")
        self.stiffness_lineEdit.setText("")
        self.stiffness_lineEdit.setMaxLength(32)
        self.stiffness_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stiffness_lineEdit.setDragEnabled(True)
        self.stiffness_lineEdit.setObjectName("stiffness_lineEdit")
        self.verticalLayout.addWidget(self.stiffness_lineEdit)
        self.sitffnessSlider_horizontalLayout = QtWidgets.QHBoxLayout()
        self.sitffnessSlider_horizontalLayout.setObjectName("sitffnessSlider_horizontalLayout")
        self.stiffness1_verticalSlider = QtWidgets.QSlider(self.stiffness_groupBox)
        self.stiffness1_verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stiffness1_verticalSlider.setMaximum(1000)
        self.stiffness1_verticalSlider.setProperty("value", 1000)
        self.stiffness1_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.stiffness1_verticalSlider.setObjectName("stiffness1_verticalSlider")
        self.sitffnessSlider_horizontalLayout.addWidget(self.stiffness1_verticalSlider)
        self.stiffness2_verticalSlider = QtWidgets.QSlider(self.stiffness_groupBox)
        self.stiffness2_verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stiffness2_verticalSlider.setMaximum(1000)
        self.stiffness2_verticalSlider.setProperty("value", 1000)
        self.stiffness2_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.stiffness2_verticalSlider.setObjectName("stiffness2_verticalSlider")
        self.sitffnessSlider_horizontalLayout.addWidget(self.stiffness2_verticalSlider)
        self.stiffness3_verticalSlider = QtWidgets.QSlider(self.stiffness_groupBox)
        self.stiffness3_verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stiffness3_verticalSlider.setMaximum(1000)
        self.stiffness3_verticalSlider.setProperty("value", 1000)
        self.stiffness3_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.stiffness3_verticalSlider.setObjectName("stiffness3_verticalSlider")
        self.sitffnessSlider_horizontalLayout.addWidget(self.stiffness3_verticalSlider)
        self.stiffness4_verticalSlider = QtWidgets.QSlider(self.stiffness_groupBox)
        self.stiffness4_verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stiffness4_verticalSlider.setMaximum(1000)
        self.stiffness4_verticalSlider.setProperty("value", 1000)
        self.stiffness4_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.stiffness4_verticalSlider.setObjectName("stiffness4_verticalSlider")
        self.sitffnessSlider_horizontalLayout.addWidget(self.stiffness4_verticalSlider)
        self.stiffness5_verticalSlider = QtWidgets.QSlider(self.stiffness_groupBox)
        self.stiffness5_verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.stiffness5_verticalSlider.setMaximum(1000)
        self.stiffness5_verticalSlider.setProperty("value", 1000)
        self.stiffness5_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.stiffness5_verticalSlider.setObjectName("stiffness5_verticalSlider")
        self.sitffnessSlider_horizontalLayout.addWidget(self.stiffness5_verticalSlider)
        self.verticalLayout.addLayout(self.sitffnessSlider_horizontalLayout)
        self.slider_verticalLayout.addWidget(self.stiffness_groupBox)
        self.attract_groupBox = QtWidgets.QGroupBox(self.settings_groupBox)
        self.attract_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.attract_groupBox.setFlat(True)
        self.attract_groupBox.setObjectName("attract_groupBox")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.attract_groupBox)
        self.verticalLayout_10.setSpacing(3)
        self.verticalLayout_10.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.attract_lineEdit = QtWidgets.QLineEdit(self.attract_groupBox)
        self.attract_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.attract_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.attract_lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.attract_lineEdit.setInputMask("")
        self.attract_lineEdit.setText("")
        self.attract_lineEdit.setMaxLength(32)
        self.attract_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.attract_lineEdit.setDragEnabled(True)
        self.attract_lineEdit.setObjectName("attract_lineEdit")
        self.verticalLayout_10.addWidget(self.attract_lineEdit)
        self.attract_horizontalLayout = QtWidgets.QHBoxLayout()
        self.attract_horizontalLayout.setObjectName("attract_horizontalLayout")
        self.attract1_verticalSlider = QtWidgets.QSlider(self.attract_groupBox)
        self.attract1_verticalSlider.setMaximum(1000)
        self.attract1_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.attract1_verticalSlider.setObjectName("attract1_verticalSlider")
        self.attract_horizontalLayout.addWidget(self.attract1_verticalSlider)
        self.attract2_verticalSlider = QtWidgets.QSlider(self.attract_groupBox)
        self.attract2_verticalSlider.setMaximum(1000)
        self.attract2_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.attract2_verticalSlider.setObjectName("attract2_verticalSlider")
        self.attract_horizontalLayout.addWidget(self.attract2_verticalSlider)
        self.attract3_verticalSlider = QtWidgets.QSlider(self.attract_groupBox)
        self.attract3_verticalSlider.setMaximum(1000)
        self.attract3_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.attract3_verticalSlider.setObjectName("attract3_verticalSlider")
        self.attract_horizontalLayout.addWidget(self.attract3_verticalSlider)
        self.attract4_verticalSlider = QtWidgets.QSlider(self.attract_groupBox)
        self.attract4_verticalSlider.setMaximum(1000)
        self.attract4_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.attract4_verticalSlider.setObjectName("attract4_verticalSlider")
        self.attract_horizontalLayout.addWidget(self.attract4_verticalSlider)
        self.attract5_verticalSlider = QtWidgets.QSlider(self.attract_groupBox)
        self.attract5_verticalSlider.setMaximum(1000)
        self.attract5_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.attract5_verticalSlider.setObjectName("attract5_verticalSlider")
        self.attract_horizontalLayout.addWidget(self.attract5_verticalSlider)
        self.verticalLayout_10.addLayout(self.attract_horizontalLayout)
        self.slider_verticalLayout.addWidget(self.attract_groupBox)
        self.settings_horizontalLayout.addLayout(self.slider_verticalLayout)
        self.damp_groupBox = QtWidgets.QGroupBox(self.settings_groupBox)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.damp_groupBox.setFont(font)
        self.damp_groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.damp_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.damp_groupBox.setFlat(True)
        self.damp_groupBox.setCheckable(False)
        self.damp_groupBox.setObjectName("damp_groupBox")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.damp_groupBox)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.damp_lineEdit = QtWidgets.QLineEdit(self.damp_groupBox)
        self.damp_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.damp_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.damp_lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.damp_lineEdit.setInputMask("")
        self.damp_lineEdit.setText("")
        self.damp_lineEdit.setMaxLength(32)
        self.damp_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.damp_lineEdit.setDragEnabled(True)
        self.damp_lineEdit.setObjectName("damp_lineEdit")
        self.verticalLayout_7.addWidget(self.damp_lineEdit)
        self.dampSlider_horizontalLayout = QtWidgets.QHBoxLayout()
        self.dampSlider_horizontalLayout.setObjectName("dampSlider_horizontalLayout")
        self.damp_verticalSlider = QtWidgets.QSlider(self.damp_groupBox)
        self.damp_verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.damp_verticalSlider.setMaximum(10000)
        self.damp_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.damp_verticalSlider.setObjectName("damp_verticalSlider")
        self.dampSlider_horizontalLayout.addWidget(self.damp_verticalSlider)
        self.verticalLayout_7.addLayout(self.dampSlider_horizontalLayout)
        self.settings_horizontalLayout.addWidget(self.damp_groupBox)
        self.drag_groupBox = QtWidgets.QGroupBox(self.settings_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drag_groupBox.sizePolicy().hasHeightForWidth())
        self.drag_groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.drag_groupBox.setFont(font)
        self.drag_groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.drag_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.drag_groupBox.setFlat(True)
        self.drag_groupBox.setObjectName("drag_groupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.drag_groupBox)
        self.verticalLayout_8.setSpacing(5)
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_8.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.drag_lineEdit = QtWidgets.QLineEdit(self.drag_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drag_lineEdit.sizePolicy().hasHeightForWidth())
        self.drag_lineEdit.setSizePolicy(sizePolicy)
        self.drag_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.drag_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.drag_lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.drag_lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.drag_lineEdit.setInputMask("")
        self.drag_lineEdit.setText("")
        self.drag_lineEdit.setMaxLength(32)
        self.drag_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.drag_lineEdit.setDragEnabled(True)
        self.drag_lineEdit.setObjectName("drag_lineEdit")
        self.verticalLayout_8.addWidget(self.drag_lineEdit)
        self.dragSlider_horizontalLayout = QtWidgets.QHBoxLayout()
        self.dragSlider_horizontalLayout.setObjectName("dragSlider_horizontalLayout")
        self.drag_verticalSlider = QtWidgets.QSlider(self.drag_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drag_verticalSlider.sizePolicy().hasHeightForWidth())
        self.drag_verticalSlider.setSizePolicy(sizePolicy)
        self.drag_verticalSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.drag_verticalSlider.setMaximum(10000)
        self.drag_verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.drag_verticalSlider.setObjectName("drag_verticalSlider")
        self.dragSlider_horizontalLayout.addWidget(self.drag_verticalSlider)
        self.verticalLayout_8.addLayout(self.dragSlider_horizontalLayout)
        self.settings_horizontalLayout.addWidget(self.drag_groupBox)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.startFrame_groupBox = QtWidgets.QGroupBox(self.settings_groupBox)
        self.startFrame_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.startFrame_groupBox.setFlat(True)
        self.startFrame_groupBox.setObjectName("startFrame_groupBox")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.startFrame_groupBox)
        self.verticalLayout_11.setSpacing(3)
        self.verticalLayout_11.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.startFrame_lineEdit = QtWidgets.QLineEdit(self.startFrame_groupBox)
        self.startFrame_lineEdit.setMaxLength(32)
        self.startFrame_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.startFrame_lineEdit.setDragEnabled(True)
        self.startFrame_lineEdit.setObjectName("startFrame_lineEdit")
        self.verticalLayout_11.addWidget(self.startFrame_lineEdit)
        self.verticalLayout_6.addWidget(self.startFrame_groupBox)
        self.wind_groupBox = QtWidgets.QGroupBox(self.settings_groupBox)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.wind_groupBox.setFont(font)
        self.wind_groupBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.wind_groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.wind_groupBox.setFlat(True)
        self.wind_groupBox.setObjectName("wind_groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.wind_groupBox)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.strength_label = QtWidgets.QLabel(self.wind_groupBox)
        self.strength_label.setAlignment(QtCore.Qt.AlignCenter)
        self.strength_label.setObjectName("strength_label")
        self.verticalLayout_3.addWidget(self.strength_label)
        self.strength_lineEdit = QtWidgets.QLineEdit(self.wind_groupBox)
        self.strength_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.strength_lineEdit.setInputMask("")
        self.strength_lineEdit.setText("")
        self.strength_lineEdit.setMaxLength(32)
        self.strength_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.strength_lineEdit.setDragEnabled(True)
        self.strength_lineEdit.setObjectName("strength_lineEdit")
        self.verticalLayout_3.addWidget(self.strength_lineEdit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.speed_label = QtWidgets.QLabel(self.wind_groupBox)
        self.speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.speed_label.setObjectName("speed_label")
        self.verticalLayout_3.addWidget(self.speed_label)
        self.speed_lineEdit = QtWidgets.QLineEdit(self.wind_groupBox)
        self.speed_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.speed_lineEdit.setInputMask("")
        self.speed_lineEdit.setText("")
        self.speed_lineEdit.setMaxLength(32)
        self.speed_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.speed_lineEdit.setDragEnabled(True)
        self.speed_lineEdit.setObjectName("speed_lineEdit")
        self.verticalLayout_3.addWidget(self.speed_lineEdit)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.frequency_label = QtWidgets.QLabel(self.wind_groupBox)
        self.frequency_label.setAlignment(QtCore.Qt.AlignCenter)
        self.frequency_label.setObjectName("frequency_label")
        self.verticalLayout_3.addWidget(self.frequency_label)
        self.frequency_lineEdit = QtWidgets.QLineEdit(self.wind_groupBox)
        self.frequency_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.frequency_lineEdit.setInputMask("")
        self.frequency_lineEdit.setText("")
        self.frequency_lineEdit.setMaxLength(32)
        self.frequency_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.frequency_lineEdit.setDragEnabled(True)
        self.frequency_lineEdit.setObjectName("frequency_lineEdit")
        self.verticalLayout_3.addWidget(self.frequency_lineEdit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.verticalLayout_6.addWidget(self.wind_groupBox)
        self.settings_horizontalLayout.addLayout(self.verticalLayout_6)
        self.settings_horizontalLayout.setStretch(0, 7)
        self.settings_horizontalLayout.setStretch(1, 1)
        self.settings_horizontalLayout.setStretch(2, 1)
        self.settings_horizontalLayout.setStretch(3, 1)
        self.verticalLayout_9.addLayout(self.settings_horizontalLayout)
        self.verticalLayout_9.setStretch(0, 5)
        self.verticalLayout_4.addWidget(self.settings_groupBox)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 5)
        self.verticalLayout_2.addWidget(self.system_groupBox)
        self.chain_groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.chain_groupBox.setFlat(True)
        self.chain_groupBox.setObjectName("chain_groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.chain_groupBox)
        self.verticalLayout_5.setSpacing(3)
        self.verticalLayout_5.setContentsMargins(3, 0, 3, 3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.parent_groupBox = QtWidgets.QGroupBox(self.chain_groupBox)
        self.parent_groupBox.setAutoFillBackground(True)
        self.parent_groupBox.setTitle("")
        self.parent_groupBox.setFlat(False)
        self.parent_groupBox.setObjectName("parent_groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.parent_groupBox)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setContentsMargins(5, 1, 1, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.parent_groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.parent_label = QtWidgets.QLabel(self.parent_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parent_label.sizePolicy().hasHeightForWidth())
        self.parent_label.setSizePolicy(sizePolicy)
        self.parent_label.setText("")
        self.parent_label.setObjectName("parent_label")
        self.horizontalLayout_2.addWidget(self.parent_label)
        self.setParent_pushButton = QtWidgets.QPushButton(self.parent_groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setParent_pushButton.sizePolicy().hasHeightForWidth())
        self.setParent_pushButton.setSizePolicy(sizePolicy)
        self.setParent_pushButton.setObjectName("setParent_pushButton")
        self.horizontalLayout_2.addWidget(self.setParent_pushButton)
        self.horizontalLayout_2.setStretch(1, 8)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout_5.addWidget(self.parent_groupBox)
        self.chain_horizontalLayout = QtWidgets.QHBoxLayout()
        self.chain_horizontalLayout.setSpacing(5)
        self.chain_horizontalLayout.setObjectName("chain_horizontalLayout")
        self.chain_listWidget = QtWidgets.QListWidget(self.chain_groupBox)
        self.chain_listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.chain_listWidget.setObjectName("chain_listWidget")
        self.chain_horizontalLayout.addWidget(self.chain_listWidget)
        self.chainButtons_verticalLayout = QtWidgets.QVBoxLayout()
        self.chainButtons_verticalLayout.setSpacing(2)
        self.chainButtons_verticalLayout.setObjectName("chainButtons_verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.chainAdd_pushButton = QtWidgets.QPushButton(self.chain_groupBox)
        self.chainAdd_pushButton.setObjectName("chainAdd_pushButton")
        self.horizontalLayout_4.addWidget(self.chainAdd_pushButton)
        self.chainRemove_pushButton = QtWidgets.QPushButton(self.chain_groupBox)
        self.chainRemove_pushButton.setObjectName("chainRemove_pushButton")
        self.horizontalLayout_4.addWidget(self.chainRemove_pushButton)
        self.chainButtons_verticalLayout.addLayout(self.horizontalLayout_4)
        self.createFromData_pushButton = QtWidgets.QPushButton(self.chain_groupBox)
        self.createFromData_pushButton.setObjectName("createFromData_pushButton")
        self.chainButtons_verticalLayout.addWidget(self.createFromData_pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.chainButtons_verticalLayout.addItem(spacerItem3)
        self.bake_pushButton = QtWidgets.QPushButton(self.chain_groupBox)
        self.bake_pushButton.setObjectName("bake_pushButton")
        self.chainButtons_verticalLayout.addWidget(self.bake_pushButton)
        self.chainButtons_verticalLayout.setStretch(0, 1)
        self.chainButtons_verticalLayout.setStretch(2, 5)
        self.chainButtons_verticalLayout.setStretch(3, 2)
        self.chain_horizontalLayout.addLayout(self.chainButtons_verticalLayout)
        self.chain_horizontalLayout.setStretch(0, 3)
        self.chain_horizontalLayout.setStretch(1, 1)
        self.verticalLayout_5.addLayout(self.chain_horizontalLayout)
        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 4)
        self.verticalLayout_2.addWidget(self.chain_groupBox)
        self.verticalLayout_2.setStretch(0, 6)
        self.verticalLayout_2.setStretch(1, 4)
        DynamicFk_mainWindow.setCentralWidget(self.centralwidget)
        self.credit_statusBar = QtWidgets.QStatusBar(DynamicFk_mainWindow)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(True)
        self.credit_statusBar.setFont(font)
        self.credit_statusBar.setStatusTip("")
        self.credit_statusBar.setObjectName("credit_statusBar")
        DynamicFk_mainWindow.setStatusBar(self.credit_statusBar)

        self.retranslateUi(DynamicFk_mainWindow)
        QtCore.QMetaObject.connectSlotsByName(DynamicFk_mainWindow)

    def retranslateUi(self, DynamicFk_mainWindow):
        DynamicFk_mainWindow.setWindowTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Dynamic FK Tool", None, -1))
        self.system_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "System", None, -1))
        self.system_listWidget.setSortingEnabled(True)
        self.preset_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Preset", None, -1))
        self.savePreset_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Save", None, -1))
        self.loadPreset_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Load", None, -1))
        self.systemAdd_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "+", None, -1))
        self.systemRemove_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "-", None, -1))
        self.refresh_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Refresh", None, -1))
        self.stiffness_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Stiffness", None, -1))
        self.stiffness_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "0.00", None, -1))
        self.attract_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Attract", None, -1))
        self.attract_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "0.00", None, -1))
        self.damp_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Damp", None, -1))
        self.damp_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "0.00", None, -1))
        self.drag_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Drag", None, -1))
        self.drag_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "0.00", None, -1))
        self.startFrame_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Start Frame", None, -1))
        self.startFrame_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "1.00", None, -1))
        self.wind_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Wind", None, -1))
        self.strength_label.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Strength", None, -1))
        self.strength_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "0.00", None, -1))
        self.speed_label.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Speed", None, -1))
        self.speed_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "0.00", None, -1))
        self.frequency_label.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Frequency", None, -1))
        self.frequency_lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "0.00", None, -1))
        self.chain_groupBox.setTitle(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "FK Chain", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Parent: ", None, -1))
        self.setParent_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Set", None, -1))
        self.chain_listWidget.setSortingEnabled(True)
        self.chainAdd_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "+", None, -1))
        self.chainRemove_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "-", None, -1))
        self.createFromData_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Create from data", None, -1))
        self.bake_pushButton.setText(QtWidgets.QApplication.translate("DynamicFk_mainWindow", "Bake", None, -1))

