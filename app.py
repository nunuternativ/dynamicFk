# system modules
import os

# utilities
from collections import defaultdict
import json

# QT modules
from PySide2 import QtCore, QtWidgets, QtGui

# maya modules
import pymel.core as pm
import maya.OpenMaya as om

# Tool modules
import core
reload(core)

import ui
reload(ui)

# custom modules
from nuTools import misc
reload(misc)

PACKAGE_DIR = os.path.dirname(__file__)
DEFAULT_PRESET_DIR = 'P:/Library/animation/dynamicFk_preset'
STIFFNESS_RANGE = (0.0, 1.0)
ATTRACT_RANGE = (0.0, 1.0)
DAMP_RANGE = (0.0, 10.0)
DRAG_RANGE = (0.0, 10.0)
STRENGTH_RANGE = (0.0, 100.0)
SPEED_RANGE = (0.0, 100.0)
FREQUENCY_RANGE = (0.0, 100.0)

DOUBLEVALIDATOR= QtGui.QDoubleValidator()

# UI class
class DynamicFkUi(QtWidgets.QMainWindow, ui.Ui_DynamicFk_mainWindow):
	def __init__(self, parent):
		super(DynamicFkUi, self).__init__(parent)
		self.setupUi(self)

		self._scriptJobs = []  # script job ids

		# modify the title
		self.setWindowTitle(QtWidgets.QApplication.translate("Ui_DynamicFk_mainWindow", 
													"Dynamic FK Tool %s" %core.VERSION, None))
		# window icon
		self.setWindowIcon(QtGui.QIcon('%s\\ui\\img\\icon.png' %(PACKAGE_DIR)))

		# tool tips
		startFrame_toolTip = 'Frame number when the dynamic effect starts.'
		self.startFrame_lineEdit.setToolTip(startFrame_toolTip)
		self.startFrame_groupBox.setToolTip(startFrame_toolTip)

		stiffness_toolTip = 'How much the object will keep its shape.'
		stiffness_toolTip += '\nThe less value, the easier the object will fall'
		stiffness_toolTip += '\n\n0 = flexible'
		stiffness_toolTip += '\n1 = hard'
		self.stiffness_groupBox.setToolTip(stiffness_toolTip)
		self.stiffness_lineEdit.setToolTip(stiffness_toolTip)

		attract_toolTip = 'How rigid the object will behave.'
		attract_toolTip += '\nThe more value, the more the object will try'
		attract_toolTip += '\nto stick to the default shape.'
		attract_toolTip += '\n\n0 = flexible'
		attract_toolTip += '\n1 = hard'
		self.attract_groupBox.setToolTip(attract_toolTip)
		self.attract_lineEdit.setToolTip(attract_toolTip)

		stiffnessScale_toolTip = 'Controls the distribution of stiffness along the chain length.'
		stiffnessScale_toolTip += '\nThe far left slider controls the base, the next 3 controls'
		stiffnessScale_toolTip += '\nthe middle and the far right controls the tip of the chain.'
		stiffnessScale_toolTip += '\n\nIf a slider is completely toned down, that area of the chain'
		stiffnessScale_toolTip += '\nwill not get any effect from stiffness althrough stiffness'
		stiffnessScale_toolTip += '\nvalue is very high.'
		self.stiffness1_verticalSlider.setToolTip(stiffnessScale_toolTip)
		self.stiffness2_verticalSlider.setToolTip(stiffnessScale_toolTip)
		self.stiffness3_verticalSlider.setToolTip(stiffnessScale_toolTip)
		self.stiffness4_verticalSlider.setToolTip(stiffnessScale_toolTip)
		self.stiffness5_verticalSlider.setToolTip(stiffnessScale_toolTip)

		damp_toolTip = 'How fast the object loses energy.'
		damp_toolTip += '\nObject with energy will bounce around'
		damp_toolTip += '\nand tend to bend more easily.'
		damp_toolTip += '\n\nless = object will bend more and take longer to stable'
		damp_toolTip += '\nmore = object will bend less and stable sooner'
		self.damp_lineEdit.setToolTip(damp_toolTip)
		self.damp_groupBox.setToolTip(damp_toolTip)

		drag_toolTip = 'Controls how laggy the object will behave.'
		drag_toolTip += '\n\n0 = No lag at all'
		drag_toolTip += '\n1 = Object will lag behind as if it is moving under water'
		self.drag_lineEdit.setToolTip(drag_toolTip)
		self.drag_groupBox.setToolTip(drag_toolTip)

		strength_toolTip = 'Controls how strong is the wind.'
		strength_toolTip += '\nStronger wind will blow object further in distance.'
		self.strength_lineEdit.setToolTip(strength_toolTip)
		self.strength_label.setToolTip(strength_toolTip)

		speed_toolTip = 'Controls how fast the wind is blowing.'
		speed_toolTip += '\nThis will effect how fast the object will move.'
		self.speed_lineEdit.setToolTip(speed_toolTip)
		self.speed_label.setToolTip(speed_toolTip)

		freq_toolTip = 'Controls the size of the wind field.'
		freq_toolTip += '\nThis will effect how object will bend to the wind.'
		freq_toolTip += '\n\nless = large wind will move object as a whole in one direction'
		freq_toolTip += '\nmore = small wind will move parts of object in different directions.'

		self.frequency_lineEdit.setToolTip(freq_toolTip)
		self.frequency_label.setToolTip(freq_toolTip)

		# credit statusBar
		self.credit_statusBar.showMessage('by Nuternativ [nuttynew@hotmail.com]')

		# validator
		self.startFrame_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.damp_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.drag_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.strength_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.speed_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.frequency_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.stiffness_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.attract_lineEdit.setValidator(DOUBLEVALIDATOR)

	def closeEvent(self, event):
		for jid in self._scriptJobs:
			if pm.scriptJob(ex=jid):
				pm.scriptJob(kill=jid, force=True)

class NewSystemDialog(QtWidgets.QDialog, ui.Ui_newSystem_Dialog):
	def __init__(self, parent):		
		super(NewSystemDialog, self).__init__(parent)
		self.setupUi(self)

		reValidator = QtGui.QRegExpValidator(QtCore.QRegExp('[A-Za-z0-9_]+'))
		self.sysName_lineEdit.setValidator(reValidator)
		self.startFrame_lineEdit.setValidator(DOUBLEVALIDATOR)

class BakeDialog(QtWidgets.QDialog, ui.Ui_bake_dialog):
	def __init__(self, parent):		
		super(BakeDialog, self).__init__(parent)
		self.setupUi(self)

		self.startFrame_lineEdit.setValidator(DOUBLEVALIDATOR)
		self.endFrame_lineEdit.setValidator(DOUBLEVALIDATOR)

# app class
class DynamicFkTool(object):
	def __init__( self, parent):
		self.systems = {}  # {'name': (uiObj, rigObj), ...}
		self.chains = defaultdict(list)  # {name: [chainA, chainB, ...]}
		self.loadedParent = None

		# directory var
		self.default_preset_dir = DEFAULT_PRESET_DIR
		if not os.path.exists(DEFAULT_PRESET_DIR):
			# if DEFAULT_FILE_DIR doesn't exist use my doc instead
			self.default_preset_dir = os.path.expanduser('~')

		self._sysStateDict = {1:QtCore.Qt.CheckState.Unchecked, 2:QtCore.Qt.CheckState.Checked}
		self._stateSysDict = {QtCore.Qt.CheckState.Unchecked:1, QtCore.Qt.CheckState.Checked:2}

		self._chainStateDict = {0:QtCore.Qt.CheckState.Unchecked, 2:QtCore.Qt.CheckState.Checked}
		self._stateChainDict = {QtCore.Qt.CheckState.Unchecked:0, QtCore.Qt.CheckState.Checked:2}

		# ------ UI
		self.ui = DynamicFkUi(parent)

		# --- connections
		self.ui.startFrame_lineEdit.editingFinished.connect(self.updateStartFrame)
		
		self.ui.stiffness_lineEdit.editingFinished.connect(self.updateStiffness)
		self.ui.stiffness1_verticalSlider.sliderReleased.connect(lambda: self.adjustStiffnessScale(self.ui.stiffness1_verticalSlider, 0))
		self.ui.stiffness2_verticalSlider.sliderReleased.connect(lambda: self.adjustStiffnessScale(self.ui.stiffness2_verticalSlider, 1))
		self.ui.stiffness3_verticalSlider.sliderReleased.connect(lambda: self.adjustStiffnessScale(self.ui.stiffness3_verticalSlider, 2))
		self.ui.stiffness4_verticalSlider.sliderReleased.connect(lambda: self.adjustStiffnessScale(self.ui.stiffness4_verticalSlider, 3))
		self.ui.stiffness5_verticalSlider.sliderReleased.connect(lambda: self.adjustStiffnessScale(self.ui.stiffness5_verticalSlider, 4))

		self.ui.attract_lineEdit.editingFinished.connect(self.updateAttract)
		self.ui.attract1_verticalSlider.sliderReleased.connect(lambda: self.adjustAttractScale(self.ui.attract1_verticalSlider, 0))
		self.ui.attract2_verticalSlider.sliderReleased.connect(lambda: self.adjustAttractScale(self.ui.attract2_verticalSlider, 1))
		self.ui.attract3_verticalSlider.sliderReleased.connect(lambda: self.adjustAttractScale(self.ui.attract3_verticalSlider, 2))
		self.ui.attract4_verticalSlider.sliderReleased.connect(lambda: self.adjustAttractScale(self.ui.attract4_verticalSlider, 3))
		self.ui.attract5_verticalSlider.sliderReleased.connect(lambda: self.adjustAttractScale(self.ui.attract5_verticalSlider, 4))

		self.ui.damp_lineEdit.editingFinished.connect(self.updateDampSlider)						
		self.ui.damp_verticalSlider.valueChanged.connect(self.updateDampLineEdit)

		self.ui.drag_lineEdit.editingFinished.connect(self.updateDragSlider)
		self.ui.drag_verticalSlider.valueChanged.connect(self.updateDragLineEdit)

		self.ui.strength_lineEdit.editingFinished.connect(self.updateStrength)
		self.ui.speed_lineEdit.editingFinished.connect(self.updateSpeed)
		self.ui.frequency_lineEdit.editingFinished.connect(self.updateFrequency)

		# buttons
		self.ui.refresh_pushButton.clicked.connect(self.populateSystem)
		self.ui.systemAdd_pushButton.clicked.connect(self.newSystem)
		self.ui.systemRemove_pushButton.clicked.connect(self.removeSystem)

		self.ui.savePreset_pushButton.clicked.connect(self.savePreset)
		self.ui.loadPreset_pushButton.clicked.connect(self.loadPreset)

		self.ui.setParent_pushButton.clicked.connect(self.setParent)
		self.ui.chainAdd_pushButton.clicked.connect(self.newChain)
		self.ui.chainRemove_pushButton.clicked.connect(self.removeChain)
		self.ui.createFromData_pushButton.clicked.connect(self.createFromData)
		self.ui.bake_pushButton.clicked.connect(self.bake)

		# list widget
		self.ui.system_listWidget.itemSelectionChanged.connect(self.systemSelected)
		self.ui.chain_listWidget.itemSelectionChanged.connect(self.chainSelected)
		
		# setting groupBox
		self.ui.settings_groupBox.setEnabled(False)

		# list widget
		self.ui.system_listWidget.itemChanged.connect(self.systemChecked)
		self.ui.chain_listWidget.itemChanged.connect(self.chainChecked)

		# setup script job to monitor systems
		self.setupScriptJob()

		# populate systems
		# self.cleanupLeftOverNetworks()
		self.populateSystem()

	def setupScriptJob(self):
		openSceneJob = pm.scriptJob(e=('SceneOpened', self.populateSystem))
		newSceneJob = pm.scriptJob(e=('NewSceneOpened', self.populateSystem))
		self.ui._scriptJobs = [openSceneJob, newSceneJob]
		# print self.ui._scriptJobs

	def updateStartFrame(self):
		value = float(self.ui.startFrame_lineEdit.text())
		self.updateNucleus(value, ['startFrame'])

	def updateStiffness(self):
		value = float(self.ui.stiffness_lineEdit.text())
		value = self.clamp(value, STIFFNESS_RANGE)
		self.ui.stiffness_lineEdit.setText(str(value))

		self.updateSystem(value, ['stiffness'])

	def updateAttract(self):
		value = float(self.ui.attract_lineEdit.text())
		value = self.clamp(value, ATTRACT_RANGE)
		self.ui.attract_lineEdit.setText(str(value))

		self.updateSystem(value, ['startCurveAttract'])

	def updateStrength(self):
		value = float(self.ui.strength_lineEdit.text())
		value = self.clamp(value, STRENGTH_RANGE)
		self.ui.strength_lineEdit.setText(str(value))

		self.updateSystem(value, ['turbulenceStrength'])

	def updateSpeed(self):
		value = float(self.ui.speed_lineEdit.text())
		value = self.clamp(value, SPEED_RANGE)
		self.ui.speed_lineEdit.setText(str(value))

		self.updateSystem(value, ['turbulenceSpeed'])

	def updateFrequency(self):
		value = float(self.ui.frequency_lineEdit.text())
		value = self.clamp(value, FREQUENCY_RANGE)
		self.ui.frequency_lineEdit.setText(str(value))

		self.updateSystem(value, ['turbulenceFrequency'])

	def savePreset(self):
		activeSysNames = self.getActiveSystemNames()
		if len(activeSysNames) != 1:
			self.popup_error('Please select a system to save as preset.')
			return
		system = self.systems[activeSysNames[0]][1]

		dialog = QtWidgets.QFileDialog(self.ui)
		dialog.setWindowTitle('Save Preset')
		dialog.setNameFilter('*.dfk')
		dialog.setDefaultSuffix('dfk')
		dialog.setDirectory(self.default_preset_dir)
		dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			pklPath = dialog.selectedFiles()[0]
			systemShape = system.hairSystem.getShape()
			data = {'stiffness': systemShape.stiffness.get(),
					'stiffnessScale[0].stiffnessScale_FloatValue': systemShape.stiffnessScale[0].stiffnessScale_FloatValue.get(),
					'stiffnessScale[1].stiffnessScale_FloatValue': systemShape.stiffnessScale[1].stiffnessScale_FloatValue.get(),
					'stiffnessScale[2].stiffnessScale_FloatValue': systemShape.stiffnessScale[2].stiffnessScale_FloatValue.get(),
					'stiffnessScale[3].stiffnessScale_FloatValue': systemShape.stiffnessScale[3].stiffnessScale_FloatValue.get(),
					'stiffnessScale[4].stiffnessScale_FloatValue': systemShape.stiffnessScale[4].stiffnessScale_FloatValue.get(),
					'startCurveAttract': systemShape.startCurveAttract.get(),
					'attractionScale[0].attractionScale_FloatValue': systemShape.attractionScale[0].attractionScale_FloatValue.get(),
					'attractionScale[1].attractionScale_FloatValue': systemShape.attractionScale[1].attractionScale_FloatValue.get(),
					'attractionScale[2].attractionScale_FloatValue': systemShape.attractionScale[2].attractionScale_FloatValue.get(),
					'attractionScale[3].attractionScale_FloatValue': systemShape.attractionScale[3].attractionScale_FloatValue.get(),
					'attractionScale[4].attractionScale_FloatValue': systemShape.attractionScale[4].attractionScale_FloatValue.get(),
					'damp': systemShape.damp.get(), 
					'drag': systemShape.drag.get(),
					'motionDrag': systemShape.motionDrag.get(), 
					'turbulenceStrength': systemShape.turbulenceStrength.get(), 
					'turbulenceSpeed': systemShape.turbulenceSpeed.get(), 
					'turbulenceFrequency': systemShape.turbulenceFrequency.get(),
					'__name': system.name,
					'__chainData': system.getChainData()}  # {chainName: {'ctrls':[(jA1, jA2, ..), (jB1, ...)], 'parent':parent}}

			with open(pklPath, 'w') as handle:
				json.dump(data, handle)

	def loadPreset(self):
		dialog = QtWidgets.QFileDialog(self.ui)
		dialog.setWindowTitle('Open')
		dialog.setNameFilter('*.dfk')
		dialog.setDefaultSuffix('dfk')
		dialog.setDirectory(self.default_preset_dir)
		dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
		pklPath = None
		if dialog.exec_() == QtWidgets.QDialog.Accepted:
			pklPath = dialog.selectedFiles()[0]
			
			data = None
			with open(pklPath, 'r') as handle:
				data = json.load(handle)

			name = data['__name']
			fileName = os.path.splitext(os.path.basename(pklPath))[0]

			minFrame = pm.playbackOptions(q=True, min=True)
			name = self.doNewSystem(name=name, startFrame=minFrame)
			# need to update the name in data to avoid crashing with
			# existing system names
			data['__name'] = name 

			for attrName, value in data.iteritems():
				systemUi = self.systems[name][0]
				system = self.systems[name][1]
				if attrName.startswith('__'):  # set the network attribute
					plug = system.network.attr(attrName[2:])  # not to include "__" at the beginning
					if plug.isLocked():
						plug.unlock()
					plug.set(str(value))
					plug.lock()
				else:
					systemShape = system.hairSystem.getShape()
					systemShape.attr(attrName).set(value)

			# repopulate all the existing systems
			self.populateSystem()
			# select the system in the UI
			ui = self.systems[name][0]
			ui.setSelected(True)

	def chainSelected(self):
		activeSysNames = self.getActiveSystemNames()
		toSels = []
		for sysName in activeSysNames:
			for item in [i for i in self.chains[sysName] if i.isSelected()]:
				system = self.systems[sysName][1]
				chainName = item.text()
				ctrls = system.fkCtrls[chainName]
				toSels.extend(ctrls)

		if toSels:
			pm.select(toSels, r=True)

	def chainRightClicked(self, pos):
		if not self.ui.chain_listWidget.itemAt(pos):
			return
		
		# show the menu
		self.ui.chainRightClickMenu.exec_(self.ui.chain_listWidget.mapToGlobal(pos))

	def systemChecked(self):
		for i in xrange(self.ui.system_listWidget.count()):
			item = self.ui.system_listWidget.item(i)

			state = item.checkState()

			sysName = item.text()
			system = self.systems[sysName][1]

			currSimMethod = system.hairSystem.simulationMethod.get()
			currState = self._sysStateDict[currSimMethod]
			stateToSet = self._stateSysDict[state]
			if currState != stateToSet:
				# toggle simulation method between static and dynamic follicles only
				system.hairSystem.simulationMethod.set(stateToSet)

	def chainChecked(self):
		activeSysNames = self.getActiveSystemNames()
		for sysName in activeSysNames:
			for item in self.chains[sysName]:
				system = self.systems[sysName][1]
				state = item.checkState()
				chainName = item.text()

				currSimMethod = system.follicles[chainName].simulationMethod.get()
				currState = self._chainStateDict[currSimMethod]
				stateToSet = self._stateChainDict[state]
				if currState != stateToSet:
					# toggle simulation method between static and dynamic
					system.follicles[chainName].simulationMethod.set(self._stateChainDict[state])

	def adjustStiffnessScale(self, slider, rampIndx):
		value = slider.value() * 0.001
		activeSysNames = self.getActiveSystemNames()
		for name in activeSysNames:
			system = self.systems[name][1]
			system.hairSystem.stiffnessScale[rampIndx].stiffnessScale_FloatValue.set(value)

	def adjustAttractScale(self, slider, rampIndx):
		value = slider.value() * 0.001
		activeSysNames = self.getActiveSystemNames()
		for name in activeSysNames:
			system = self.systems[name][1]
			system.hairSystem.attractionScale[rampIndx].attractionScale_FloatValue.set(value)

	def getActiveSystemNames(self):
		selItems = self.ui.system_listWidget.selectedItems()
		names = [i.text() for i in selItems]
		return names

	def updateSystem(self, value, attrNames):
		activeSysNames = self.getActiveSystemNames()

		for name in activeSysNames:
			system = self.systems[name][1]
			for attrName in attrNames:
				system.hairSystem.attr(attrName).set(value)

	def updateNucleus(self, value, attrNames):
		activeSysNames = self.getActiveSystemNames()
		for name in activeSysNames:
			system = self.systems[name][1]
			for attrName in attrNames:
				system.nucleus.attr(attrName).set(value)

	def deleteTrash(self, errNodes):
		# sub network
		if errNodes['subNetwork']:
			for node in errNodes['subNetwork']:
				if not pm.objExists(node):
					continue
				ctrls = node.ctrls.inputs()
				his = node.listHistory(lv=1)
				if his:
					try:
						pm.delete([h for h in his if h not in ctrls])  # don't delete the original controlelr
					except Exception, e:
						pass

		# loc
		if errNodes['rootLocator']:
			for node in errNodes['rootLocator']:
				if not pm.objExists(node):
					continue
				parent = node.parent.inputs()
				his = node.listHistory(lv=1)
				if his:
					try:
						pm.delete([h for h in his if h!=parent])  # don't delete the parent
					except Exception, e:
						pass

		# network
		networkNode = errNodes['network']
		if networkNode and pm.objExists(networkNode):
			his = networkNode.listHistory(lv=1)
			if his:
				try:
					pm.delete(his)
				except Exception, e:
					pass
			return False  # return false if the main network node is deleted
		return True

	def populateSystem(self):
		self.systems = {}
		self.chains = {}
		self.ui.parent_label.setText('')
		self.loadedParent = None
		
		self.ui.system_listWidget.clear()
		self.ui.chain_listWidget.clear()
		self.setSettingsToDefaultState()

		for node in pm.ls(type='network'):
			if not node.hasAttr('__NODE_TYPE')\
				or node.attr('__NODE_TYPE').get() != core.DynamicFkRig.__name__:
				continue

			system = core.DynamicFkRig(network=node)
			if any(system._err.values()):
				ret = self.deleteTrash(errNodes=system._err)
				if not ret:
					continue
				else:
					system = core.DynamicFkRig(network=node)
			systemName = system.name

			# current simulation method of the hairsystem
			currSimMethod = system.hairSystem.simulationMethod.get()
			currState = self._sysStateDict[currSimMethod]

			itemWidget = QtWidgets.QListWidgetItem(systemName)
			itemWidget.setCheckState(currState)
			self.ui.system_listWidget.addItem(itemWidget)

			self.systems[systemName] = [itemWidget, system]

	def setSettingsToDefaultState(self):
		self.ui.settings_groupBox.setEnabled(True)
		self.ui.startFrame_lineEdit.setText('1.00')
		self.ui.stiffness_lineEdit.setText('0.00')
		self.ui.attract_lineEdit.setText('0.00')
		self.ui.stiffness1_verticalSlider.setValue(1000)
		self.ui.stiffness2_verticalSlider.setValue(1000)
		self.ui.stiffness3_verticalSlider.setValue(1000)
		self.ui.stiffness4_verticalSlider.setValue(1000)
		self.ui.stiffness5_verticalSlider.setValue(1000)

		self.ui.damp_lineEdit.setText('0.00')
		self.ui.damp_verticalSlider.setValue(0)

		self.ui.drag_lineEdit.setText('0.00')
		self.ui.drag_verticalSlider.setValue(0)

		self.ui.strength_lineEdit.setText('0.00')
		self.ui.speed_lineEdit.setText('0.00')
		self.ui.frequency_lineEdit.setText('0.00')

		self.ui.settings_groupBox.setEnabled(False)

	def systemSelected(self):
		activeSysNames = self.getActiveSystemNames()
		if not activeSysNames:
			self.setSettingsToDefaultState()
			self.ui.settings_groupBox.setEnabled(False)
			self.ui.chain_listWidget.clear()
			return
		
		# update setting UI to the last system selected
		lastSelSystem = self.systems[activeSysNames[-1]][1]
		self.updateSettingsGroupBox(system=lastSelSystem)

		# populate FK chain list widget
		self.populateChain(names=activeSysNames)

	def populateChain(self, names):
		self.ui.chain_listWidget.clear()
		toSels = []
		self.chains = defaultdict(list)
		for name in names:
			system = self.systems[name][1]

			for chainName, ctrlChain in system.ctrls.iteritems():
				currSimMethod = system.follicles[chainName].simulationMethod.get()
				currState = self._chainStateDict[currSimMethod]

				# add to ui
				itemWidget = QtWidgets.QListWidgetItem(chainName)
				itemWidget.setCheckState(currState)

				# set tooltip to indicate parent of the chain
				rootLoc = system.rootLocators[chainName]
				parent = rootLoc.parent.inputs()[0]
				ctrls = [c.nodeName() for c in system.ctrls[chainName]]
				toolTip = 'system: %s\nparent: %s\nmembers:\n%s' %(name, parent.nodeName(), '\n'.join(ctrls))
				
				self.ui.chain_listWidget.addItem(itemWidget)
				itemWidget.setToolTip(toolTip)

				self.chains[name].append(itemWidget)

	def setParent(self, sel=None):
		if not sel:
			sel = misc.getSel()
			if not sel:
				return

		# clear out existing parent
		self.ui.parent_label.setText('')
		self.loadedParent = None

		# set new text
		parentName = sel.nodeName()
		self.ui.parent_label.setText(parentName)
		self.loadedParent = sel

	def createFromData(self):
		activeSysNames = self.getActiveSystemNames()
		if len(activeSysNames) != 1:
			self.popup_error('Select a system to add FK chain to.')
			return

		system = self.systems[activeSysNames[0]][1]
		exec('raw_data = %s' %system.network.attr('chainData').get())
		if not raw_data:
			self.popup_error('No chain data found in current system.')
			return

		# get user selection
		sel = misc.getSel(num=1, selType='any')
		if not sel:
			self.popup_error('Select an object with the namespace to create FK chain from data.')
			return

		ns = sel.namespace()
		for data in raw_data:
			parentName = '%s%s' %(ns, data['parent'])
			ctrls = data['ctrls']
			if not pm.objExists(parentName):
				om.MGlobal.displayError('Parent does not exits: %s' %parentName)
				continue
			parent = pm.PyNode(parentName)
			self.setParent(parent)

			ctrl_nodes = []
			for ctrl in ctrls:
				ctrlName = '%s%s' %(ns, ctrl)
				if not pm.objExists(ctrlName):
					om.MGlobal.displayError('ctrl does not exits: %s' %ctrlName)
					continue
				ctrl_nodes.append(pm.PyNode(ctrlName))
			
			# do a pre checks
			result = self.checkCtrls(ctrl_nodes)	
			if not result:
				continue

			# do add new chain
			pm.undoInfo(openChunk=True)
			newChainNames = system.add(parent=self.loadedParent, ctrls=[ctrl_nodes])
			pm.undoInfo(closeChunk=True)

		# will have return value as the new chian names[] in case of success
		# update ui
		self.populateChain(names=activeSysNames)
		
		# select the new chain
		newChainUi = [c for c in self.chains[system.name] if c.text() == newChainNames[0]][0]
		newChainUi.setSelected(True)

	def checkCtrls(self, ctrls):
		# populate controls that has been add to a system for the entire scene
		systems = [s[1] for s in self.systems.values()]
		existingCtrls = []
		for sys in systems:
			for chainName, ctrlChain in sys.fkCtrls.iteritems():
				existingCtrls.extend(ctrlChain)

		errMsgs = defaultdict(list)
		for ctrl in ctrls:
			ctrlName = ctrl.nodeName()

			# make sure the control is not part of any ohter system
			if ctrl in existingCtrls:
				errMsg = 'This control is already a member of other system.'
				errMsgs[ctrlName].append(errMsg)

			# make sure there's no connection or constraint
			trInputs = []
			for attr in [ctrl.translate, ctrl.rotate]:
				for cAttr in attr.getChildren():
					inputs = cAttr.inputs()
					trInputs.extend(inputs)

			if [c for c in trInputs if c.type() not in ['animCurveTL', 'animCurveTA', 'animCurveTU']]:
				errMsg = 'Translate or Rotate channel must not have any constraint or connection.'
				errMsgs[ctrlName].append(errMsg)

			# make sure translate is not locked
			if [t for t in ctrl.translate.getChildren() if t.isLocked() or not t.isKeyable()]:
				errMsg = 'Translate attribute is locked.'
				errMsgs[ctrlName].append(errMsg)

			# make sure rotate is not locked
			if [r for r in ctrl.rotate.getChildren() if r.isLocked() or not r.isKeyable()]:
				errMsg = 'Rotate attribute is locked.'
				errMsgs[ctrlName].append(errMsg)

		if errMsgs:
			msg = ''
			for ctrlName, msgs in errMsgs.iteritems():
				msg += '%s\n' %ctrlName
				for m in msgs:
					msg += '  -%s\n' %m
			self.popup_error(msg)
			return False
		return True

	def newChain(self, ctrls=[]):
		activeSysNames = self.getActiveSystemNames()
		if len(activeSysNames) != 1:
			self.popup_error('Select a system to add FK chain to.')
			return

		# check parent
		if not self.loadedParent:
			self.popup_error('A FK chain must has a parent, set parent first.')
			return
		
		if not pm.objExists(self.loadedParent):
			self.popup_error('Parent does not exists, try resetting the parent.')
			return
		
		# get controls from user selection
		if not ctrls:
			ctrls = misc.getSel(num='inf', selType='transform')
			if not ctrls or len(ctrls) < 2:
				self.popup_error('Select 2 or more controllers from base to tip in order.')
				return
		
		# get the active system
		system = self.systems[activeSysNames[0]][1]
		# do a pre checks
		result = self.checkCtrls(ctrls)	
		if not result:
			return

		# do add new chain
		pm.undoInfo(openChunk=True)
		newChainNames = system.add(parent=self.loadedParent, ctrls=[ctrls])
		pm.undoInfo(closeChunk=True)

		# will have return value as the new chian names[] in case of success
		# update ui
		self.populateChain(names=activeSysNames)
		
		# select the new chain
		newChainUi = [c for c in self.chains[system.name] if c.text() == newChainNames[0]][0]
		newChainUi.setSelected(True)

	def getActiveChainNames(self):
		selItems = self.ui.chain_listWidget.selectedItems()
		if not selItems:
			return
		activeSysNames = self.getActiveSystemNames()

		res = defaultdict(list)
		for sysName in activeSysNames:
			for item in self.chains[sysName]:
				if item.isSelected():
					system = self.systems[sysName][1]
					res[system].append(item.text())
		return res

	def removeChain(self):
		
		activeSysNames = self.getActiveSystemNames()
		activeChainNames = self.getActiveChainNames()
		if not activeChainNames:
			return

		pm.undoInfo(openChunk=True)
		for system, delNames in activeChainNames.iteritems():
			system.remove(delNames)
		pm.undoInfo(closeChunk=True)

		self.populateChain(names=activeSysNames)

	def updateSettingsGroupBox(self, system):
		# unlock settings ui
		self.ui.settings_groupBox.setEnabled(True)

		# start frame
		startFrameValue = system.nucleus.startFrame.get()
		self.ui.startFrame_lineEdit.setText(str(startFrameValue))

		# stiffness
		stiffnessValue = system.hairSystem.stiffness.get()
		self.ui.stiffness_lineEdit.setText(str(stiffnessValue))
		attractValue = system.hairSystem.startCurveAttract.get()
		self.ui.attract_lineEdit.setText(str(attractValue))

		sv1 = system.hairSystem.stiffnessScale[0].stiffnessScale_FloatValue.get()
		sv2 = system.hairSystem.stiffnessScale[1].stiffnessScale_FloatValue.get()
		sv3 = system.hairSystem.stiffnessScale[2].stiffnessScale_FloatValue.get()
		sv4 = system.hairSystem.stiffnessScale[3].stiffnessScale_FloatValue.get()
		sv5 = system.hairSystem.stiffnessScale[4].stiffnessScale_FloatValue.get()

		# stiffness bars
		self.ui.stiffness1_verticalSlider.setValue(sv1*1000)
		self.ui.stiffness2_verticalSlider.setValue(sv2*1000)
		self.ui.stiffness3_verticalSlider.setValue(sv3*1000)
		self.ui.stiffness4_verticalSlider.setValue(sv4*1000)
		self.ui.stiffness5_verticalSlider.setValue(sv5*1000)

		av1 = system.hairSystem.attractionScale[0].attractionScale_FloatValue.get()
		av2 = system.hairSystem.attractionScale[1].attractionScale_FloatValue.get()
		av3 = system.hairSystem.attractionScale[2].attractionScale_FloatValue.get()
		av4 = system.hairSystem.attractionScale[3].attractionScale_FloatValue.get()
		av5 = system.hairSystem.attractionScale[4].attractionScale_FloatValue.get()

		# attraction bars
		self.ui.attract1_verticalSlider.setValue(av1*1000)
		self.ui.attract2_verticalSlider.setValue(av2*1000)
		self.ui.attract3_verticalSlider.setValue(av3*1000)
		self.ui.attract4_verticalSlider.setValue(av4*1000)
		self.ui.attract5_verticalSlider.setValue(av5*1000)

		# damp
		dampValue = system.hairSystem.damp.get()
		self.ui.damp_lineEdit.setText(str(dampValue))
		self.updateDampSlider()

		# drag
		dragValue = system.hairSystem.drag.get()
		self.ui.drag_lineEdit.setText(str(dragValue))
		self.updateDragSlider()

		# wind
		turbStrValue = system.hairSystem.turbulenceStrength.get()
		self.ui.strength_lineEdit.setText(str(turbStrValue))

		turbFeqValue = system.hairSystem.turbulenceFrequency.get()
		self.ui.frequency_lineEdit.setText(str(turbFeqValue))

		turbSpeedValue = system.hairSystem.turbulenceSpeed.get()
		self.ui.speed_lineEdit.setText(str(turbSpeedValue))

	def popup_error(self, msg, header='Error'):
		QtWidgets.QMessageBox.critical(self.ui,
			header,
			msg,
			QtWidgets.QMessageBox.Ok)

	def newSystem(self):
		newSysDialog = NewSystemDialog(self.ui)
		newSysDialog.startFrame_lineEdit.setText(str(pm.playbackOptions(q=True, min=True)))
		if newSysDialog.exec_() == QtWidgets.QDialog.Accepted:
			name = newSysDialog.sysName_lineEdit.text()
			startFrame = float(newSysDialog.startFrame_lineEdit.text())

			# return
			self.doNewSystem(name, startFrame)

	def doNewSystem(self, name, startFrame):
		# check for clashing system names
		exit = False
		i = 1
		test_name = name
		while not exit:
			if test_name in [s[1].name for s in self.systems.values()]:
				# self.popup_error('System with the same name exists: %s' %name)
				test_name = '%s%s' %(name, i)
				i += 1
			else:
				name = test_name
				exit = True
		# create the object
		pm.undoInfo(openChunk=True)
		system = core.DynamicFkRig(name=name)
		system.new()
		system.nucleus.startFrame.set(startFrame)
		pm.undoInfo(closeChunk=True)

		# add to ui
		self.populateSystem()
		item = self.systems[name][0]
		item.setSelected(True)
		return name

	def removeSystem(self):
		toRemoveNames = self.getActiveSystemNames()
		if toRemoveNames:
			pm.undoInfo(openChunk=True)
			self.doRemoveSystem(toRemoveNames)
			pm.undoInfo(closeChunk=True)
		# else:
		# 	self.popup_error(msg='Select one or more system to remove.')
		self.populateSystem()

	def doRemoveSystem(self, names):
		for name in names:
			# delete maya object
			rigObj = self.systems[name][1]
			allChainNames = rigObj.ctrls.keys()
			rigObj.remove(chainNames=allChainNames)
			pm.delete([rigObj.rigGrp, rigObj.expression, rigObj.displayLayer])

			# delete UI
			itemWidget = self.systems[name][0]
			itemRow = self.ui.system_listWidget.row(itemWidget)
			self.ui.system_listWidget.takeItem(itemRow)

			# remove from class var
			del self.systems[name]

	def clamp(self, value, valueRange):
		if value < valueRange[0]:
			value = valueRange[0]
		elif value > valueRange[1]:
			value = valueRange[1]
		return value

	def updateDampSlider(self):
		inputValue = float(self.ui.damp_lineEdit.text())
		inputValue = self.clamp(inputValue, DAMP_RANGE)
		self.ui.damp_lineEdit.setText(str(inputValue))

		# set slider
		value = inputValue * 1000
		self.ui.damp_verticalSlider.setValue(value)

	def updateDampLineEdit(self):
		inputValue = self.ui.damp_verticalSlider.value() * 0.001
		inputValue = self.clamp(inputValue, DAMP_RANGE)
		self.ui.damp_verticalSlider.setValue(inputValue * 1000)

		self.ui.damp_lineEdit.setText(str(round(inputValue, 3)))

		self.updateSystem(inputValue, ['damp'])

	def updateDragSlider(self):
		inputValue = float(self.ui.drag_lineEdit.text())
		inputValue = self.clamp(inputValue, DRAG_RANGE)
		self.ui.drag_lineEdit.setText(str(inputValue))

		# set slider
		value = inputValue * 1000
		self.ui.drag_verticalSlider.setValue(value)

	def updateDragLineEdit(self):
		inputValue = self.ui.drag_verticalSlider.value() * 0.001
		inputValue = self.clamp(inputValue, DRAG_RANGE)

		self.ui.drag_verticalSlider.setValue(inputValue * 1000)

		self.ui.drag_lineEdit.setText(str(round(inputValue, 3)))

		self.updateSystem(inputValue, ['drag', 'motionDrag'])

	def bake(self):
		activeSysNames = self.getActiveSystemNames()
		chainDict = self.getActiveChainNames()
		if not chainDict:
			return

		bakeDialog = BakeDialog(self.ui)
		bakeDialog.startFrame_lineEdit.setText(str(pm.playbackOptions(q=True, min=True)))
		bakeDialog.endFrame_lineEdit.setText(str(pm.playbackOptions(q=True, max=True)))
		if bakeDialog.exec_() == QtWidgets.QDialog.Accepted:
			startFrame = float(bakeDialog.startFrame_lineEdit.text())
			endFrame = float(bakeDialog.endFrame_lineEdit.text())
			simplifyCurve = bakeDialog.simplifyCurve_checkBox.isChecked()
			pm.undoInfo(openChunk=True)
			for system, chainNames in chainDict.iteritems():
				system.bake(chainNames, startFrame, endFrame, simplifyCurve)
				system.remove(chainNames)
			pm.undoInfo(closeChunk=True)

			self.populateChain(names=activeSysNames)
				
			# if no chain left, remove the system
			remainingSysNames = []
			for systemName in activeSysNames:
				chains = self.chains[systemName]
				sysUi = self.systems[systemName][0]
				if not chains:
					sysUi.setSelected(True)
				else:
					sysUi.setSelected(False)
					remainingSysNames.append(systemName)

			self.removeSystem()
			for systemName in remainingSysNames:
				ui = self.systems[systemName][0]
				ui.setSelected(True)
