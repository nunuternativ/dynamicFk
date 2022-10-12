# ---------- CHANGE NOTES ----------
# v1.0  - Base version
# v1.1  - Add "Attract" controls
#       - Fix expression bug when remove a chain
#       - Fix scriptJob warning when re-launching the app
# v1.2  - Add "Create from data" feature that enable user 
#         to re-create FK chains from previously created one
#       - Fix UI bug when loading a system from file
#       - Fix name crashing when loading system from file
# v1.2.1- Fix DynCtrl Zro group naming bug
# v1.3  - Fix Maya2018 bake animation result NaN values in
#         animation curves 
# v1.31 - Added "Simplify Curve" as checkbox in bake dialog
# ----------------------------------

from string import ascii_uppercase
from textwrap import dedent as textwrap_dedent
from re import search as re_search
from re import DOTALL as re_DOTALL
from collections import defaultdict

import pymel.core as pm
import maya.OpenMaya as om
import maya.mel as mel

from nuTools import misc, controller
from nuTools.pipeline import pipeTools
from nuTools import naming
# reload(misc)
reload(controller)
reload(pipeTools)
reload(naming)

VERSION = '1.31'

CONTROL_SHAPE = 'crossDiamond'
CONTROL_COLOR = 'purple'

# hairSystem default attribute values
DEFAULT_ITERATIONS = 16
DEFAULT_STIFFNESS = 0.1
DEFAULT_STARTCURVEATTRACT = 1.0
DEFAULT_DAMP = 0.5
DEFAULT_DRAG = 0.0
DEFAULT_MASS = 1.0

DEFAULT_TURB_STRENGTH = 0.0
DEFAULT_TURB_FREQUENCY = 0.3
DEFAULT_TURB_SPEED = 0.3

# nucleus default attribute values
DEFAULT_SUBSTEPS = 8
DEFAULT_SPACESCALE = 0.1
DEFAULT_GRAVITY = 0.98


dyn_exp_str = '''if ((frame == {}.startFrame)||({}.simulationMethod == 1)) {{
    {}.currentTime = {}.startFrame;
}} else {{
    {}.currentTime += 1;
}}'''

class DynamicFkRig(object):
    '''
    Dynamic Fk rig class
    '''

    def __init__(self,
                name='chain', 
                size=1.0,
                network=None,
                ctrlShape=CONTROL_SHAPE,
                ctrlColor=CONTROL_COLOR):

        # string
        self.name = name
        self.size = size
        self.ctrlShape = ctrlShape
        self.ctrlColor = ctrlColor
        # self.chainData = defaultdict(dict)  # {chainName:{'ctrls':[(jA1, jA2, ..), (jB1, ...)], 'parent':parent}}

        self.parents = {}  # {parent:rootLocator, ...}
        self.rootLocators = {}  #{name:rootLocator, ...}

        # groups
        self.rigGrp = None
        self.chainGrps = {}

        # ctrls
        self.ctrls = {}  # {name:(objA1, objA2, ...), ...}
        self.fkCtrls = {} 
        self.fkCtrlZgrps = {}

        # jnts
        self.fkJnts = {}
        self.spJnts = {}

        # ikHandles
        self.ikHandles = {}

        # curves
        self.startCurves = {}
        self.dynCurves = {}

        # nodes
        self.hairSystem = None
        self.nucleus = None
        self.expression = None
        self.displayLayer = None
        self.follicles = {}
        self.trPmas = {}
        self.roPmas = {}
        self.reverses = {}
        self.blendShapes = {}
        self.ctrlConstraints = {}

        self._err = {}

        # if network is passed, override 
        if network:
            # print 'Initing from %s...' %network
            return self.initFromNetwork(network=network)

    def initFromNetwork(self, network):
        self._err['network'] = None
        self._err['rootLocator'] = set()
        self._err['subNetwork'] = set()

        # get attr in main network node
        self.name = network.attr('name').get()
        self.size = float(network.attr('size').get())
        self.ctrlShape = network.attr('ctrlShape').get()
        self.ctrlColor = network.attr('ctrlColor').get()

        self.rigGrp = self.getNodeFromNetwork(network, 'rigGrp')
        self.hairSystem = self.getNodeFromNetwork(network, 'hairSystem')
        self.nucleus = self.getNodeFromNetwork(network, 'nucleus')
        self.expression = self.getNodeFromNetwork(network, 'expression')
        self.displayLayer = self.getNodeFromNetwork(network, 'displayLayer')

        # check for error
        for elem in [self.rigGrp, self.hairSystem, self.nucleus, self.expression, self.displayLayer]:
            if not elem:
                self._err['network'] = network  # a fully function system must has all these attr connected

        # get self.parents
        rootLocators = self.getNodesFromNetwork(network, 'rootLocators')

        errChainLocs = set()
        for loc in rootLocators:
            parent = loc.attr('parent').inputs()
            if parent:
                self.parents[parent[0]] = loc
            else:
                # check for error
                self._err['rootLocator'].add(loc) # a loc must has a parent connection

        # get chains
        for parent, loc in self.parents.iteritems():
            chain_networks = self.getNodesFromNetwork(loc, 'chains')
            for cnw in chain_networks:
                chainName = cnw.attr('name').get()
                self.rootLocators[chainName] = loc

                # single attrs
                self.chainGrps[chainName] = self.getNodeFromNetwork(cnw, 'chainGrp')
                self.ikHandles[chainName] = self.getNodeFromNetwork(cnw, 'ikHandle')
                self.startCurves[chainName] = self.getNodeFromNetwork(cnw, 'startCurve')
                self.dynCurves[chainName] = self.getNodeFromNetwork(cnw, 'dynCurve')
                self.follicles[chainName] = self.getNodeFromNetwork(cnw, 'follicle')
                self.trPmas[chainName] = self.getNodeFromNetwork(cnw, 'trPma')
                self.roPmas[chainName] = self.getNodeFromNetwork(cnw, 'roPma')

                # check for error
                for elem in (self.chainGrps[chainName], self.ikHandles[chainName], \
                            self.startCurves[chainName], self.dynCurves[chainName], \
                            self.follicles[chainName], self.trPmas[chainName], \
                            self.roPmas[chainName]):
                    if not elem:
                        self._err['subNetwork'].add(cnw)

                # multi attrs
                self.ctrls[chainName] = self.getNodesFromNetwork(cnw, 'ctrls')
                self.fkCtrls[chainName] = self.getNodesFromNetwork(cnw, 'fkCtrls')
                self.fkCtrlZgrps[chainName] = self.getNodesFromNetwork(cnw, 'fkCtrlZgrps')
                self.fkJnts[chainName] = self.getNodesFromNetwork(cnw, 'fkJnts')
                self.spJnts[chainName] = self.getNodesFromNetwork(cnw, 'spJnts')
                self.ctrlConstraints[chainName] = self.getNodesFromNetwork(cnw, 'ctrlConstraints')

                # check for error
                for elems in [self.ctrls[chainName], self.fkCtrls[chainName], self.fkCtrlZgrps[chainName], 
                            self.fkJnts[chainName], self.spJnts[chainName], self.ctrlConstraints[chainName]]:
                    if not elems:
                        self._err['subNetwork'].add(cnw)
                        break

        

        self.network = network

    def getNodeFromNetwork(self, network, attrName):
        node = None
        try:
            node = network.attr(attrName).inputs()[0]
        except:
            pass
        return node

    def getNodesFromNetwork(self, network, attrName):
        nodes = []
        try:
            nodes = network.attr(attrName).inputs()  
        except:
            pass
        return nodes

    def new(self):
        # grouping
        self.rigGrp = pm.group(em=True, n=naming.NAME((self.name, 'DynFk'), '', naming.GRP))
        # self.rigGrp.hiddenInOutliner.set(True)

        # create hairSystem
        self.hairSystem = pm.createNode('hairSystem')
        self.hairSystem.rename(naming.NAME((self.name, 'DynFk'), '', '%sShape' %naming.HSYS))
        hSysTr = self.hairSystem.getParent()
        hSysTr.visibility.set(0)
        hSysTr.rename(naming.NAME((self.name, 'DynFk'), '', naming.HSYS))

        # force set
        # self.hairSystem.active.set(True)
        # self.hairSystem.ignoreSolverGravity.set(False)
        # self.hairSystem.ignoreSolverWind.set(False)
        self.hairSystem.collide.set(0)  # collide - off
        self.hairSystem.simulationMethod.set(2)  # dynamic follicle only
        self.hairSystem.tangentialDrag.set(0)
        self.hairSystem.motionDrag.set(0)
        self.hairSystem.startCurveAttract.set(0)

        # for user
        self.hairSystem.iterations.set(DEFAULT_ITERATIONS)
        self.hairSystem.stiffness.set(DEFAULT_STIFFNESS)
        self.hairSystem.startCurveAttract.set(DEFAULT_STARTCURVEATTRACT)
        self.hairSystem.damp.set(DEFAULT_DAMP)
        self.hairSystem.drag.set(DEFAULT_DRAG)
        self.hairSystem.mass.set(DEFAULT_MASS)

        self.hairSystem.turbulenceStrength.set(DEFAULT_TURB_STRENGTH)
        self.hairSystem.turbulenceFrequency.set(DEFAULT_TURB_FREQUENCY)
        self.hairSystem.turbulenceSpeed.set(DEFAULT_TURB_SPEED)

        # hair stiffness ramp settings
        self.hairSystem.stiffnessScale[0].stiffnessScale_Position.set(0.0)
        self.hairSystem.stiffnessScale[0].stiffnessScale_Position.lock()
        self.hairSystem.stiffnessScale[0].stiffnessScale_Interp.set(1)
        self.hairSystem.stiffnessScale[0].stiffnessScale_FloatValue.set(1.0)

        self.hairSystem.stiffnessScale[1].stiffnessScale_Position.set(0.25)
        self.hairSystem.stiffnessScale[1].stiffnessScale_Position.lock()
        self.hairSystem.stiffnessScale[1].stiffnessScale_Interp.set(1)
        self.hairSystem.stiffnessScale[1].stiffnessScale_FloatValue.set(1.0)

        self.hairSystem.stiffnessScale[2].stiffnessScale_Position.set(0.5)
        self.hairSystem.stiffnessScale[2].stiffnessScale_Position.lock()
        self.hairSystem.stiffnessScale[2].stiffnessScale_Interp.set(1)
        self.hairSystem.stiffnessScale[2].stiffnessScale_FloatValue.set(1.0)

        self.hairSystem.stiffnessScale[3].stiffnessScale_Position.set(0.75)
        self.hairSystem.stiffnessScale[3].stiffnessScale_Position.lock()
        self.hairSystem.stiffnessScale[3].stiffnessScale_Interp.set(1)
        self.hairSystem.stiffnessScale[3].stiffnessScale_FloatValue.set(1.0)

        self.hairSystem.stiffnessScale[4].stiffnessScale_Position.set(1.0)
        self.hairSystem.stiffnessScale[4].stiffnessScale_Position.lock()
        self.hairSystem.stiffnessScale[4].stiffnessScale_Interp.set(1)
        self.hairSystem.stiffnessScale[4].stiffnessScale_FloatValue.set(1.0)

        # hair attract ramp settings
        self.hairSystem.attractionScale[0].attractionScale_Position.set(0.0)
        self.hairSystem.attractionScale[0].attractionScale_Position.lock()
        self.hairSystem.attractionScale[0].attractionScale_Interp.set(1)
        self.hairSystem.attractionScale[0].attractionScale_FloatValue.set(0.0)

        self.hairSystem.attractionScale[1].attractionScale_Position.set(0.25)
        self.hairSystem.attractionScale[1].attractionScale_Position.lock()
        self.hairSystem.attractionScale[1].attractionScale_Interp.set(1)
        self.hairSystem.attractionScale[1].attractionScale_FloatValue.set(0.0)

        self.hairSystem.attractionScale[2].attractionScale_Position.set(0.5)
        self.hairSystem.attractionScale[2].attractionScale_Position.lock()
        self.hairSystem.attractionScale[2].attractionScale_Interp.set(1)
        self.hairSystem.attractionScale[2].attractionScale_FloatValue.set(0.0)

        self.hairSystem.attractionScale[3].attractionScale_Position.set(0.75)
        self.hairSystem.attractionScale[3].attractionScale_Position.lock()
        self.hairSystem.attractionScale[3].attractionScale_Interp.set(1)
        self.hairSystem.attractionScale[3].attractionScale_FloatValue.set(0.0)

        self.hairSystem.attractionScale[4].attractionScale_Position.set(1.0)
        self.hairSystem.attractionScale[4].attractionScale_Position.lock()
        self.hairSystem.attractionScale[4].attractionScale_Interp.set(1)
        self.hairSystem.attractionScale[4].attractionScale_FloatValue.set(0.0)

        # create nucleus
        self.nucleus = pm.createNode('nucleus')
        self.nucleus.rename(naming.NAME((self.name, 'DynFk'), '', naming.NCLS))
        self.nucleus.visibility.set(0)
        pm.parent([self.hairSystem.getParent(), self.nucleus], self.rigGrp)

        # force set
        self.nucleus.maxCollisionIterations.set(0)
        self.nucleus.subSteps.set(DEFAULT_SUBSTEPS)
        # self.nucleus.spaceScale.set(DEFAULT_SPACESCALE)
        # self.nucleus.gravity.set(DEFAULT_GRAVITY)
        
        # for user
        # self.nucleus.timeScale.set(DEFAULT_TIMESCALE)

        # connect hairsytem to nucleus
        pm.connectAttr(self.nucleus.startFrame, self.hairSystem.startFrame)
        pm.connectAttr(self.nucleus.currentTime, self.hairSystem.currentTime)
        pm.connectAttr(self.nucleus.outputObjects[0], self.hairSystem.nextState)
        pm.connectAttr(self.hairSystem.currentState, self.nucleus.inputActive[0])
        pm.connectAttr(self.hairSystem.startState, self.nucleus.inputActiveStart[0])

        # create expession
        hSysName = self.hairSystem.nodeName()
        nclsName = self.nucleus.nodeName()
        exp_str = dyn_exp_str.format(nclsName, hSysName, nclsName, nclsName, nclsName)
        self.expression = pm.expression(s=exp_str)
        self.expression.rename(naming.NAME(self.name, '', naming.EXP))
        
        # create display layer to hide original controllers
        self.displayLayer = pm.createDisplayLayer(name=naming.NAME((self.name, 'DynFk'), '', naming.DLYR), number=1, empty=True)

        # connect network
        self.network = pm.createNode('network', n=naming.NAME((self.name, 'DynFk'), '', naming.NETWORK))
        misc.addStrAttr(self.network, '__NODE_TYPE', txt=self.__class__.__name__, lock=True)
        misc.addStrAttr(self.network, '__VERSION', txt=VERSION, lock=True)

        nameAttr = misc.addStrAttr(self.network, 'name', txt=self.name, lock=True)
        sizeAttr = misc.addStrAttr(self.network, 'size', txt=self.size, lock=True)
        ctrlShpAttr = misc.addStrAttr(self.network, 'ctrlShape', txt=self.ctrlShape, lock=True)
        ctrlColorAttr = misc.addStrAttr(self.network, 'ctrlColor', txt=self.ctrlColor, lock=True)
        chainDataAttr = misc.addStrAttr(self.network, 'chainData', txt='', lock=False)

        self.connectNodeToMainNetwork(self.rigGrp, 'rigGrp')
        self.connectNodeToMainNetwork(self.hairSystem, 'hairSystem')
        self.connectNodeToMainNetwork(self.nucleus, 'nucleus')
        self.connectNodeToMainNetwork(self.expression, 'expression')
        self.connectNodeToMainNetwork(self.displayLayer, 'displayLayer')

        misc.addMsgAttr(self.network, 'rootLocators', multi=True)


    def createChainNetwork(self, chainName, parent):
        single_attr_names = ['chainGrp',
                            'ikHandle', 
                            'startCurve', 
                            'dynCurve', 
                            'follicle', 
                            'trPma', 
                            'roPma']

        multi_attr_names = ['ctrls', 
                            'fkCtrls',  
                            'fkCtrlZgrps', 
                            'fkJnts', 
                            'spJnts', 
                            'ctrlConstraints']

        network_node = pm.createNode('network', n=naming.NAME(chainName, '', naming.NETWORK))
        misc.addStrAttr(obj=network_node, attr='name', txt=chainName, lock=True, multi=False)

        indx = parent.chains.numElements()
        pm.connectAttr(network_node.message, parent.chains[indx])

        for attr_name in single_attr_names:
            attr = misc.addMsgAttr(network_node, attr_name, multi=False)
        for attr_name in multi_attr_names:
            attr = misc.addMsgAttr(network_node, attr_name, multi=True)

        return network_node

    def addObjectsToSubNetwork(self, network, attrName, objs):
        chainAttr = misc.addMsgAttr(network, attrName, multi=True)

        chainAttr.disconnect()
        for i, obj in enumerate(objs):
            pm.connectAttr(obj.message, chainAttr[i], f=True)

    def addObjectToSubNetwork(self, network, attrName, obj):
        chainAttr = misc.addMsgAttr(network, attrName, multi=False)

        pm.connectAttr(obj.message, chainAttr, f=True)

    def connectNodeToMainNetwork(self, obj, attrName):
        msgAttr = misc.addMsgAttr(self.network, attrName)
        pm.connectAttr(obj.message, msgAttr, f=True)

    def drawCurveFromJoints(self, joints, degree=1):
        positions = []
        for j in joints:
            pos = j.getTranslation('world')
            positions.append(pos)

        curve = pm.curve(d=degree, p=positions)
        return curve

    def addExpression(self, addStr):
        addStr = textwrap_dedent(addStr)  # get rid of extra \t
        addStr = '\t'.join(addStr.splitlines(True))
        
        current_exp_str = pm.expression(self.expression, q=True, s=True)[:-1]
        new_exp_str = '%s%s}' %(current_exp_str, addStr)
        pm.expression(self.expression, e=True, s=new_exp_str)


    def add(self, parent, ctrls):
        '''
        adding ctrl to hair system
        '''
        newCtrls = {}
        # existingCtrls = [ctrl for chain in self.ctrls.values() for ctrl in chain]
        for chain in ctrls:

            chainTmp = []
            alpIt = misc.alphabetIter(seq=ascii_uppercase)

            for ctrl in chain:
                # convert string name to PyNode
                if isinstance(ctrl, (str, unicode)):
                    ctrl = pm.PyNode(ctrl)

                if not isinstance(ctrl, pm.PyNode):
                    om.MGlobal.displayError('Invalid object type: %s(%s)' %(ctrl, type(ctrl)))
                    return

                chainTmp.append(ctrl)

            exit = False
            while not exit:
                alp = alpIt.next()
                chainName = '%s%s' %(self.name.replace('_', ''), alp)  # stip _ for better zro group naming
                if chainName in self.ctrls.keys():
                    continue
                else:
                    self.ctrls[chainName] = chainTmp
                    newCtrls[chainName] = chainTmp
                    exit = True

        # if parent is not the same as existing loc parents
        parentName = parent.nodeName().split(':')[-1]
        if parent not in self.parents.keys():   
            rootLocator = pm.spaceLocator()
            rootLocator.rename(naming.NAME('%s__%s__%s' %(self.name, parentName, 'DynFk'), '', naming.LOC))
            rootLocator.getShape().visibility.set(0)
            pm.parent(rootLocator, self.rigGrp)
            pm.parentConstraint(parent, rootLocator)
            pm.scaleConstraint(parent, rootLocator)
            self.parents[parent] = rootLocator
            
            # locator expression
            rootLocatorName = rootLocator.nodeName()
            exp_add_str = '''
                        // --- Start {}
                        float ${}RefreshTx = {}.tx;
                        float ${}RefreshTy = {}.ty;
                        float ${}RefreshTz = {}.tz;
                        float ${}RefreshRx = {}.rx;
                        float ${}RefreshRy = {}.ry;
                        float ${}RefreshRz = {}.rz;
                        // --- End {}
                        '''
            exp_add_str = exp_add_str.format(parentName, 
                                        parentName, rootLocatorName,
                                        parentName, rootLocatorName,
                                        parentName, rootLocatorName,
                                        parentName, rootLocatorName,
                                        parentName, rootLocatorName,
                                        parentName, rootLocatorName,
                                        parentName)

            self.addExpression(addStr=exp_add_str)

            # add loc to network
            nwIndx = self.network.rootLocators.numElements()
            pm.connectAttr(rootLocator.message, self.network.rootLocators[nwIndx])

            parentAttr = misc.addMsgAttr(rootLocator, 'parent')
            pm.connectAttr(parent.message, parentAttr)

            chainAttr = misc.addMsgAttr(rootLocator, 'chains', multi=True)
        else:
            rootLocator = self.parents[parent]
        
        # loop over each chain
        ctrlTypDict = {'joint':controller.JointController, 'transform':controller.Controller}
        for chainName, ctrls in newCtrls.iteritems():
            # create network
            chain_nw = self.createChainNetwork(chainName=chainName, parent=rootLocator)

            # update self.rootLocators
            self.rootLocators[chainName] = rootLocator

            chainGrp = pm.group(em=True, n=naming.NAME((chainName, 'DynFk'), '', naming.GRP))
            chainGrp.visibility.set(0)
            pm.parent(chainGrp, self.rigGrp)

            self.chainGrps[chainName] = chainGrp
            self.addObjectToSubNetwork(network=chain_nw, attrName='chainGrp', obj=chainGrp)

            # create follicle
            folShp = pm.createNode('follicle', n=naming.NAME(chainName, '', '%sShape' %naming.FOL))
            folTr = folShp.getParent()
            folTr.rename(naming.NAME(chainName, '', naming.FOL))

            folShp.pointLock.set(1)  # pointLock - base
            folShp.restPose.set(1)  # restPose - same as start
            folShp.startDirection.set(1)  # startDirection - start curve base
            folShp.degree.set(1)  # degree - linear
            folShp.collide.set(0)  # collide - off

            misc.snapTransform('parent', ctrls[0], folTr, False, True)
            pm.parent(folTr, chainGrp)

            self.follicles[chainName] = folTr
            self.addObjectToSubNetwork(network=chain_nw, attrName='follicle', obj=folTr)

            # draw curve
            startCrv = self.drawCurveFromJoints(joints=ctrls)
            startCrvShp = startCrv.getShape()
            startCrv.rename(naming.NAME((chainName, 'Start'), '', naming.CRV))

            dynCrv = startCrv.duplicate()[0]
            dynCrvShp = dynCrv.getShape()
            dynCrv.rename(naming.NAME((chainName, 'Dyn'), '', naming.CRV))

            pm.parent(startCrv, folTr)
            pm.parent(dynCrv, chainGrp)

            self.startCurves[chainName] = startCrv
            self.dynCurves[chainName] = dynCrv

            self.addObjectToSubNetwork(network=chain_nw, attrName='startCurve', obj=startCrv)
            self.addObjectToSubNetwork(network=chain_nw, attrName='dynCurve', obj=dynCrv)

            # make connections to add to hairSystem
            # hSysIndx = self.hairSystem.inputHair.numElements()
            old_num = 0
            indices = self.hairSystem.inputHair.getArrayIndices()
            if not indices:
                hSysIndx = 0
            else:
                for i in xrange(indices[-1]):
                    if i not in indices:
                        hSysIndx = i
                        break
                else:
                    hSysIndx = indices[-1] + 1

            pm.connectAttr(folShp.outHair, self.hairSystem.inputHair[hSysIndx])
            pm.connectAttr(self.hairSystem.outputHair[hSysIndx], folShp.currentPosition)
            pm.connectAttr(startCrv.worldMatrix[0], folShp.startPositionMatrix)
            pm.connectAttr(startCrvShp.local, folShp.startPosition)
            pm.connectAttr(folShp.outCurve, dynCrvShp.create)

            # create plusMinusAverage to sum trnaslate and rotate
            trPma = pm.createNode('plusMinusAverage', n=naming.NAME((chainName, 'Traslate'), '', naming.PMA))
            roPma = pm.createNode('plusMinusAverage', n=naming.NAME((chainName, 'Rotate'), '', naming.PMA))

            pm.connectAttr(rootLocator.translate, trPma.input3D.input3D[0])
            pm.connectAttr(rootLocator.rotate, roPma.input3D.input3D[0])

            self.trPmas[chainName] = trPma
            self.roPmas[chainName] = roPma

            self.addObjectToSubNetwork(network=chain_nw, attrName='trPma', obj=trPma)
            self.addObjectToSubNetwork(network=chain_nw, attrName='roPma', obj=roPma)

            # add to expressions
            trPmaNodeName = trPma.nodeName()
            roPmaNodeName = roPma.nodeName()
            exp_add_str = '''
                        // --- Start {}
                        float ${}RefreshTx = {}.output3D.output3Dx;
                        float ${}RefreshTy = {}.output3D.output3Dy;
                        float ${}RefreshTz = {}.output3D.output3Dz;
                        float ${}RefreshRx = {}.output3D.output3Dx;
                        float ${}RefreshRy = {}.output3D.output3Dy;
                        float ${}RefreshRz = {}.output3D.output3Dz;
                        // --- End {}
                        '''
            exp_add_str = exp_add_str.format(chainName,
                                            chainName, trPmaNodeName,
                                            chainName, trPmaNodeName,
                                            chainName, trPmaNodeName,
                                            chainName, roPmaNodeName,
                                            chainName, roPmaNodeName,
                                            chainName, roPmaNodeName,
                                            chainName)
            self.addExpression(addStr=exp_add_str)

            # loop over each ctrl
            fkJnts, fkCtrls, spJnts, fkCtrlZgrps = [], [], [], []
            ctrlConstraints = []
            for i, ctrl in enumerate(ctrls):
                ro = ctrl.rotateOrder.get()

                # create fk jnt
                fkJnt = pm.createNode('joint', n=naming.NAME((chainName, (i+1), 'Fk'), '', naming.JNT))
                fkJnt.radius.set(self.size*0.1)
                fkJnt.rotateOrder.set(ro)
                misc.snapTransform('parent', ctrl, fkJnt, False, True)
                pm.makeIdentity(fkJnt, apply=True)
                fkJnts.append(fkJnt)

                # create fk ctrl
                ctrlShp = ctrl.getShape(ni=True)
                ctrlTyp = ctrl.type()
                fkCtrl = ctrlTypDict[ctrlTyp](st=self.ctrlShape,
                                            color=self.ctrlColor,
                                            n=naming.NAME((chainName, (i+1), 'DynFk'), '', naming.CTRL),
                                            draw=False)

                fkCtrlShp = fkCtrl.getShape(ni=True)
                if ctrlShp and isinstance(ctrlShp, pm.nt.NurbsCurve):
                    # print ctrlShp, fkCtrlShp
                    pm.connectAttr(ctrlShp.worldSpace, fkCtrlShp.create)
                    # pm.disconnectAttr(ctrlShp.worldSpace, fkCtrlShp.create)
                
                fkCtrl.rotateOrder.set(ro)
                fkCtrlZgrp = misc.zgrp(fkCtrl, element='Zro', suffix='grp')[0]
                
                ctrlParent = ctrl.getParent()
                if not ctrlParent:
                    ctrlParent = ctrl

                fkCtrlZgrp.rotateOrder.set(ctrlParent.rotateOrder.get())

                # connect to pma
                n = trPma.input3D.numElements()
                pm.connectAttr(fkCtrl.translate, trPma.input3D.input3D[n])
                pm.connectAttr(fkCtrl.rotate, roPma.input3D.input3D[n])

                misc.snapTransform('parent', ctrlParent, fkCtrlZgrp, False, True)
                if ctrlTyp == 'joint':
                    jo = ctrl.jointOrient.get()
                    fkCtrl.jointOrient.set(jo)

                misc.snapTransform('parent', ctrl, fkCtrl, False, True)
                misc.snapTransform('parent', fkCtrl, fkJnt, False, False)

                misc.lockAttr(fkCtrl, t=False, r=False, s=True, v=True)
                misc.hideAttr(fkCtrl, t=False, r=False, s=True, v=True)

                fkCtrls.append(fkCtrl)
                fkCtrlZgrps.append(fkCtrlZgrp)
                
                # create spline jnt
                spJnt = pm.createNode('joint', n=naming.NAME((chainName, (i+1), 'Sp'), '', naming.JNT))
                fkJnt.radius.set(self.size*0.5)
                spJnt.rotateOrder.set(ro)
                misc.snapTransform('parent', ctrl, spJnt, False, True)
                pm.makeIdentity(spJnt, apply=True)
                spJnts.append(spJnt)

                # parent into chain
                if i == 0:
                    pm.parent([fkJnt, spJnt], chainGrp)
                    pm.parent(fkCtrlZgrp, rootLocator)
                else:
                    pm.parent(fkJnt, fkJnts[i-1])
                    pm.parent(fkCtrlZgrp, fkCtrls[i-1])
                    pm.parent(spJnt, spJnts[i-1])

                misc.lockAttr(fkCtrlZgrp, t=True, r=True, s=True, v=True)
                # lock fkCtrl zro grp, in case our animator is a naughty one
                
                # move keys from controls to fkCtrls and constraint controls to spJnt
                for attr_str in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                    attr = ctrl.attr(attr_str)
                    attrInputs = attr.inputs(type='animCurve')
                    for ac in attrInputs:
                        # attr.disconnect()
                        pm.disconnectAttr(ac.output, attr)
                        pm.connectAttr(ac.output, fkCtrl.attr(attr_str))

                cons = pm.parentConstraint(spJnt, ctrl, mo=True)
                ctrlConstraints.append(cons)

            self.ctrls[chainName] = ctrls
            self.fkJnts[chainName] = fkJnts
            self.fkCtrls[chainName] = fkCtrls
            self.fkCtrlZgrps[chainName] = fkCtrlZgrps
            self.spJnts[chainName] = spJnts
            self.ctrlConstraints[chainName] = ctrlConstraints

            self.addObjectsToSubNetwork(network=chain_nw, attrName='ctrls', objs=ctrls)
            self.addObjectsToSubNetwork(network=chain_nw, attrName='fkJnts', objs=fkJnts)
            self.addObjectsToSubNetwork(network=chain_nw, attrName='fkCtrls', objs=fkCtrls)
            self.addObjectsToSubNetwork(network=chain_nw, attrName='fkCtrlZgrps', objs=fkCtrlZgrps)
            self.addObjectsToSubNetwork(network=chain_nw, attrName='spJnts', objs=spJnts)
            self.addObjectsToSubNetwork(network=chain_nw, attrName='ctrlConstraints', objs=ctrlConstraints)         

            # create spline IK
            ikHndl, ikEff = pm.ikHandle(sj=spJnts[0], ee=spJnts[-1],
                                        sol='ikSplineSolver', scv=False, roc=True, pcv=False,
                                        ccv=False, curve=dynCrv)
            ikHndl.rename(naming.NAME((chainName, 'DynFk'), '', naming.IKHNDL))
            pm.parent(ikHndl, chainGrp)
            self.ikHandles[chainName] = ikHndl
            self.addObjectToSubNetwork(network=chain_nw, attrName='ikHandle', obj=ikHndl)

            rollAttr = misc.addNumAttr(fkCtrls[0], 'roll', 'double')
            pm.connectAttr(rollAttr, ikHndl.roll)
            twAttr = misc.addNumAttr(fkCtrls[0], 'twist', 'double')
            pm.connectAttr(twAttr, ikHndl.twist)

            # bind skin the start curve
            skinCluster = pm.skinCluster(fkJnts, startCrv, tsb=True, dr=2, mi=1)

        # set display layer
        self.displayLayer.addMembers(list(sum(self.ctrls.values(), [])))
        currLyrVis = self.displayLayer.visibility.get()
        # self.displayLayer.visibility.set(0)
        if currLyrVis:
            mel.eval('layerEditorLayerButtonVisibilityChange %s;' %self.displayLayer.nodeName())

        return newCtrls.keys()

    def remove(self, chainNames):
        '''
        remove a chain from the system
        '''
        for chainName in chainNames:
            # check if chain name exists in the system
            if not chainName in self.fkCtrls.keys():
                return

            # delete constraint on original controllers
            pm.delete(self.ctrlConstraints[chainName])

            # move keys from fkCtrl back to original controls (if any)
            for ctrl, fkCtrl in zip(self.ctrls[chainName], self.fkCtrls[chainName]):
                for attr_str in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                    fkAttr = fkCtrl.attr(attr_str)
                    fkAttrInputs = fkAttr.inputs(type='animCurve')
                    for ac in fkAttrInputs:
                        fkAttr.disconnect()
                        pm.connectAttr(ac.output, ctrl.attr(attr_str))

            # remove the chain's part of expression
            current_exp_str = pm.expression(self.expression, q=True, s=True)
            search_res = re_search('(\n\t// --- Start %s.*\n\t// --- End %s\n)' %(chainName, chainName), 
                                current_exp_str, 
                                re_DOTALL)
            remove_part = search_res.group(1)

            new_exp_str = current_exp_str.replace(remove_part, '')
            pm.expression(self.expression, e=True, s=new_exp_str)

            # delete chain group, fk controls and some left over nodes
            pm.delete(self.chainGrps[chainName])
            pm.delete(self.fkCtrls[chainName])
            pm.delete(self.trPmas[chainName])
            pm.delete(self.roPmas[chainName])

            # remove original controls from displaylayer membership
            for c in self.ctrls[chainName]:
                pm.disconnectAttr(self.displayLayer.drawInfo, c.drawOverride)

            # delete the variables
            try: del self.chainGrps[chainName] 
            except KeyError: pass

            try: del self.ctrls[chainName] 
            except KeyError: pass

            try: del self.fkCtrls[chainName] 
            except KeyError: pass

            try: del self.fkCtrlZgrps [chainName] 
            except KeyError: pass

            try: del self.fkJnts[chainName] 
            except KeyError: pass

            try: del self.spJnts[chainName] 
            except KeyError: pass

            try: del self.ikHandles[chainName] 
            except KeyError: pass

            try: del self.startCurves[chainName] 
            except KeyError: pass

            try: del self.dynCurves[chainName] 
            except KeyError: pass

            try: del self.follicles[chainName] 
            except KeyError: pass

            try: del self.trPmas[chainName] 
            except KeyError: pass

            try: del self.roPmas[chainName] 
            except KeyError: pass

            try: del self.ctrlConstraints[chainName]
            except KeyError: pass

    def getChainData(self):
         # get self.parents
        rootLocators = self.getNodesFromNetwork(self.network, 'rootLocators')

        result = []
        for loc in rootLocators:
            parents = loc.attr('parent').inputs()
            if not parents:
                continue
            parent = parents[0]
            chain_networks = self.getNodesFromNetwork(loc, 'chains')
            chain_networks = sorted(chain_networks, key=lambda n: n.attr('name').get())
            for nw in chain_networks:
                # nw_name = nw.attr('name').get()
                ctrls = self.getNodesFromNetwork(nw, 'ctrls')
                if ctrls:
                    parentName = misc.removeDagPathNamespace(str(parent.shortName()))
                    ctrlNames = [misc.removeDagPathNamespace(str(c.shortName())) for c in ctrls]
                    result.append({'parent':parentName, 'ctrls':ctrlNames})

        # update attr
        self.network.chainData.unlock()
        self.network.chainData.set(str(result))
        self.network.chainData.lock()
        return result 
            
    def bake(self, chainNames, startFrame=None, endFrame=None, simplifyCurve=False):
        '''
        run bake simulation on a chain of original controls
        '''
        # get start time and end time
        if startFrame == None:
            startFrame = pm.playbackOptions(q=True, min=True)
        if endFrame == None:
            endFrame = pm.playbackOptions(q=True, max=True)

        # populate controllers to be baked
        allCtrls = []
        for chainName in chainNames:
            if not chainName in self.ctrls.keys():
                om.MGlobal.displayWarning('%s does not exist in the system' %chainName)
                continue

            allCtrls.extend(self.ctrls[chainName])
        # allCtrls = list(set(allCtrls))
        # do bake
        pm.refresh(suspend=True)
        # with pipeTools.FreezeViewport() as fw:
        pm.bakeResults(allCtrls,
                    simulation=True,
                    t=(startFrame, endFrame), 
                    sampleBy=1, 
                    disableImplicitControl=True,
                    preserveOutsideKeys=True,
                    sparseAnimCurveBake=False, 
                    removeBakedAttributeFromLayer=False, 
                    removeBakedAnimFromLayer=False, 
                    bakeOnOverrideLayer=False, 
                    minimizeRotation=True,
                    controlPoints=False, 
                    shape=False)
        pm.refresh(suspend=False)
        pm.refresh(f=True)

        # clean anim curves
        pipeTools.cleanAllNaNAnimCurves(objs=allCtrls)

        # simplify curves
        if simplifyCurve:
            pm.filterCurve(allCtrls, f='simplify', timeTolerance=0.05, tolerance=0.01)

        # remove nodes
        for chainName in chainNames:
            # delete all keys on fkCtrls
            fkChainAnimCrvs = []
            for ctrl, fkCtrl in zip(self.ctrls[chainName], self.fkCtrls[chainName]):
                # copy keyrame outside of bake range from fk ctrl back to ctrls
                firstKey = pm.findKeyframe(fkCtrl, w='first')
                lastKey = pm.findKeyframe(fkCtrl, w='last')

                if startFrame - firstKey > 0.0:
                    upperRange = ((firstKey-2.0), (startFrame-1.0))
                    numCopied = pm.copyKey(fkCtrl, time=upperRange)
                    if numCopied > 0:
                        pm.pasteKey(ctrl, time=upperRange, option='replace')

                if lastKey - endFrame > 0.0:
                    lowerRange = ((endFrame + 1), (lastKey+2))
                    numCopied = pm.copyKey(fkCtrl, time=lowerRange)
                    if numCopied > 0:
                        pm.pasteKey(ctrl, time=lowerRange, option='replace')

                fkCtrlAnimCrvs = fkCtrl.inputs(type='animCurve')
                fkChainAnimCrvs.extend(fkCtrlAnimCrvs)
            pm.delete(fkChainAnimCrvs)

        # remove chain from system
        self.remove(chainNames)


