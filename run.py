import sys

from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import app
reload(app)

def mayaRun():
	'''
		from nuTools.util.dynamicFk import run as dfkRun
		reload(dfkRun)
		dfkApp = dfkRun.mayaRun()
	'''
	import maya.OpenMayaUI as omui
	global dynamicFkToolApp

	try:
		dynamicFkToolApp.ui.close()
	except:
		pass
	
	ptr = omui.MQtUtil.mainWindow()
	dynamicFkToolApp = app.DynamicFkTool(parent=wrapInstance(long(ptr), QtWidgets.QWidget))
	dynamicFkToolApp.ui.show()

	return dynamicFkToolApp