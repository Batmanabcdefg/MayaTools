from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui 
import pymel.core as pm


from PySide.QtUiTools import *
from PySide import QtCore, QtGui
import shiboken
Signal = QtCore.Signal

def _getcls(name):
    result = getattr(QtGui, name, None)
    if result is None:
        result = getattr(QtCore, name, None)
    return result

def wrapInstance(ptr):
    """Converts a pointer (int or long) into the concrete
    PyQt/PySide object it represents."""
    ptr = long(ptr)
    qobj = shiboken.wrapInstance(ptr, QtCore.QObject)
    metaobj = qobj.metaObject()
    realcls = None
    while realcls is None:
        realcls = _getcls(metaobj.className())
        metaobj = metaobj.superClass()
    return shiboken.wrapInstance(ptr, realcls)

from functools import partial
import logging
import re
import os

cwd = os.path.dirname(os.path.abspath(__file__))

mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(long(mayaMainWindowPtr)) 

class NoRollSetup(QtGui.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(NoRollSetup, self).__init__(*args, **kwargs)
        
        #Parent widget under Maya main window        
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Tool)
        
        logging.basicConfig( filename=cwd+'/NoRollSetup.log', filemode='w',
                             format= '%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                             datefmt='%m/%d/%Y %I:%M:%S %p' )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info('Initializing...')  
        
        self.initUI()
        
        # Load selected buttons
        self.ui.loadShldrJointPushButton.clicked.connect( partial(self.loadSel, self.ui.shldrJointLineEdit) )
        self.ui.loadElbowJointPushButton.clicked.connect( partial(self.loadSel, self.ui.elbowJointLineEdit) )
        self.ui.loadWristJointPushButton.clicked.connect( partial(self.loadSel, self.ui.wristJointLineEdit) )
        self.ui.jointChainPushButton.clicked.connect( partial(self.loadSel, self.ui.jointChainLineEdit) )
        
        # Create Button
        self.ui.createPushButton.clicked.connect(self.build)
        
        self.ui.show()
        
    def initUI(self):        
        loader = QUiLoader()        
        currentDir = os.path.dirname(__file__)        
        file = QtCore.QFile(currentDir+"/NoRollSetup.ui")        
        file.open(QtCore.QFile.ReadOnly)        
        self.ui = loader.load(file, parentWidget=self)        
        file.close()        
    
    def loadSel(self, fld=None):
        fld.setText(str(pm.ls(sl=1)[0]))
        
    def build(self):
        ''' Get the UI data, call build methods '''
        #--- Create no roll setup
        self.logger.info('build(): Starting...') 
        
        self.buildShoulderNoRoll()
        self.buildForearmNoRoll()
            
        self.logger.info('build(): End.') 
            
    def buildShoulderNoRoll(self):
        ''' Setup no roll shoulder. Assumes Elbow is child of Shoulder. '''
        self.logger.info('buildShoulderNoRoll(): Starting...') 
        # Get the shoulder / elbow / wrist joint
        shldrJ = str(self.ui.shldrJointLineEdit.text())
        elbowJ = str(self.ui.elbowJointLineEdit.text())
        wristJ = str(self.ui.wristJointLineEdit.text())
        parentJ = str(self.ui.jointChainLineEdit.text())
        
        # Get as PyNodes
        pm.select(elbowJ,r=1)
        elbowJ = pm.ls(sl=1)[0]
        pm.select(shldrJ,r=1)
        shldrJ = pm.ls(sl=1)[0]   
        pm.select(wristJ,r=1)
        wristJ = pm.ls(sl=1)[0]        
            
        #--- No roll rig
        nfShldr = self.noRollRig( startJnt=shldrJ )
        
        # Get the nfWrist joint
        for each in pm.listRelatives( nfShldr, children=1 ):
            if each.type() == 'joint':
                nfWrist = each
                self.logger.info('buildShoulderNoRoll(): Selected noroll wrist: %s'%nfWrist)
                break    
            
        #--- Create the spline joint chain
        numJoints = self.ui.clavJointLcdNumber.value()
        startJ, endJ = self.createJoints( startJnt=shldrJ, endJnt=elbowJ, numJoints=numJoints )
        
        #--- Setup the Ik Spline with Advanced Twist
        ikHandle, ikCurve = self.advancedSplineIK( startJ=startJ, endJ=endJ, start=shldrJ, 
                               nfStart=nfShldr )
        pm.parentConstraint(shldrJ, ikCurve, mo=True)
        
        #--- Create twist result joint
        twistJnt = self.createTwistJnt(jnt=elbowJ, nfJnt=nfShldr, ikHandle=ikHandle)
        
        #--- Create rig grp
        grp = pm.group(em=True, name='%s_noroll_grp'%shldrJ)
        pm.delete(pm.parentConstraint(shldrJ, grp, mo=False))
        pm.parent(nfShldr, grp)
        pm.parent(ikHandle, grp)
        pm.parent(ikCurve, grp)
        
        clavJ = pm.listRelatives(shldrJ, parent=True)
        pm.parentConstraint(clavJ, grp, mo=True)
        
        pm.pointConstraint(shldrJ,nfShldr,mo=True)
        
        pm.parent(startJ, parentJ)
        
        self.logger.info('buildShoulderNoRoll(): End.') 
        
    def buildForearmNoRoll(self):
        ''' Setup no roll shoulder. Assumes Palm is child of Wrist '''
        self.logger.info('buildForearmNoRoll(): Starting...') 
        # Get the joints
        elbowJ = str(self.ui.elbowJointLineEdit.text())
        wristJ = str(self.ui.wristJointLineEdit.text())
        parentJ = str(self.ui.jointChainLineEdit.text())
        
        # Get them as PyNode objects
        pm.select(elbowJ,r=1)
        elbowJ = pm.ls(sl=1)[0]
        pm.select(wristJ,r=1)
        wristJ = pm.ls(sl=1)[0]        
        
        #--- No roll rig
        nfWrist = self.noRollRig( startJnt=wristJ ) 
            
        #--- Create the spline joint chain
        numJoints = self.ui.elbowJointLcdNumber.value()
        startJ, endJ = self.createJoints( startJnt=elbowJ, endJnt=wristJ, numJoints=numJoints )
        
        #--- Setup the Ik Spline with Advanced Twist
        ikHandle, ikCurve = self.advancedSplineIK( startJ=startJ, endJ=endJ, start=elbowJ, 
                               nfStart=nfWrist )
        #--- Create twist result joint
        twistJnt = self.createTwistJnt(jnt=wristJ, nfJnt=nfWrist, ikHandle=ikHandle)
        
        #--- Create rig grp
        grp = pm.group(em=True, name='%s_noroll_grp'%elbowJ)
        pm.delete(pm.parentConstraint(elbowJ, grp, mo=False))
        pm.parent(nfWrist, grp)
        pm.parent(ikHandle, grp)
        pm.parent(ikCurve, grp)
        
        pm.parentConstraint(elbowJ, grp, mo=True)
        
        pm.pointConstraint(elbowJ,nfWrist,mo=True)
        
        pm.parent(startJ, parentJ)
        self.logger.info('buildForearmNoRoll(): End.') 
    
    def createTwistJnt(self, jnt=None, nfJnt=None, ikHandle=None):
        ''' Setup twist joint to use as angular diff object from no_roll jnt '''
        twistJnt =pm.duplicate(jnt, n=jnt.name()+'_twistResult')[0]
        pm.delete(pm.listRelatives(twistJnt))
        nfEnd = [x for x in pm.listRelatives(nfJnt, children=True) if x.type()=='joint'][0] 
        pm.parent(twistJnt, nfJnt)
        pm.aimConstraint(nfEnd, twistJnt, 
                         aimVector=(1,0,0),
                         worldUpVector=(0,1,0),
                         wuo=jnt, wut='objectrotation')
        
        #--- Connect twist result to ikSpline twist
        pm.connectAttr('%s.rotateX'%twistJnt, '%s.twist'%ikHandle, f=True) 
        
        return twistJnt
        
    def noRollRig(self, startJnt=None):
        ''' Create no flip start / end joint with ik handle '''
        self.logger.info('noRollRig(): Starting...')
        # Duplicate startJnt joint
        nfStart = pm.duplicate(startJnt, n=startJnt.name()+'_NoRoll')[0]
                    
        # Delete everything except the elbow, wrist or palm under the nfStart
        for each in pm.listRelatives(nfStart, children=True):
            if each.type() == 'joint':
                if re.search(r'Elbow|Palm|Wrist', each.name().split('|')[-1]):
                    self.logger.info('noRollRig(): Skip duplicate child delete: %s' % each)
                    continue
            pm.delete(each)
            self.logger.info('noRollRig(): Deleted child of duplicate: %s' % each)
            
        nfEnd = None
        # Select elbow, wrist or palm
        for each in pm.listRelatives(nfStart, children=True):
            if each.type() == 'joint':
                if 'Palm' or 'WristJ' or 'ElbowJ' in each.split('|')[-1]:
                    self.logger.info('noRollRig(): nfEnd: %s' % each.split('|')[-1])
                    nfEnd = each
                
        if nfEnd:
            nfEnd.rename(nfEnd.name()+'_NoRollEnd')
        else:
            raise Exception('No Elbow or Palm joint found.')
        
        # Delete everything below the nfEnd joint
        pm.delete( pm.listRelatives(nfEnd, children=True) )
        
        # Create the ikHandle
        ikHandle = pm.ikHandle( sj=nfStart, ee=nfEnd, 
                                n=nfStart.name()+'_IkHandle',
                                solver='ikRPsolver')[0]
        
        # Parent handle
        pm.parent(ikHandle, startJnt)
        
        # Set polevector to 0, 0, 0
        pm.setAttr('%s.poleVectorX'%ikHandle, 0)
        pm.setAttr('%s.poleVectorY'%ikHandle, 0)
        pm.setAttr('%s.poleVectorZ'%ikHandle, 0)
        
        self.logger.info('noRollRig(): End.')
        return nfStart
    
    def createJoints(self, startJnt=None, endJnt=None, numJoints=None):
        ''' Create the twist joint chain along the shoulder and elbow '''
        # Get joint positions
        positions = []
        for jnt in [startJnt, endJnt]:
            positions.append(pm.xform(jnt.name(), q=1, ws=1, t=1))   
        
        # Create the curve
        curve = pm.curve(p=positions, d=1, n='%s_curve'%startJnt.name()) 
        curveShape = curve.getShape()

        # Create joints on the curve
        increment = 1/(numJoints-1)
        cI = increment
        joints = []
        positions = []
        
        pm.select(clear=True)
        for i in range(int(numJoints)):
            # Create joint
            jnt = pm.joint(n=startJnt+'_bind_%s'%(i+1))
            joints.append(jnt)
            
            # Attach to curve
            poci = pm.shadingNode('pointOnCurveInfo', n='%s_pocinfo_node'%jnt.name(), asUtility=True)
            pm.connectAttr('%s.ws'%curveShape, '%s.inputCurve'%poci, f=1)
            pm.connectAttr('%s.position'%poci, '%s.translate'%jnt, f=1)
            
            if i == 0:
                pm.setAttr('%s.parameter'%poci, 0)
                # Store position
                positions.append(pm.xform(jnt, q=1, ws=1, rp=1))
                # Delete poci
                pm.delete(poci)  
                continue
            
            elif i == (numJoints-1):
                pm.setAttr('%s.parameter'%poci, 1)  
                # Store position
                positions.append(pm.xform(jnt, q=1, ws=1, rp=1))                
                # Delete poci
                pm.delete(poci)                
                continue
            
            pm.setAttr('%s.parameter'%poci, cI) 
            # Store position
            positions.append(pm.xform(jnt, q=1, ws=1, rp=1))            
            # Delete poci
            pm.delete(poci)            
            cI = cI + increment
            
        # Delete the curve
        pm.delete(curve)
            
        # Place joints at their positions
        for j,p in zip(joints, positions):
            pm.move(j, p, a=1)
            
        # Parent joints to create the chain    
        for j in joints:
            if j.endswith('1'):
                continue
            num = j.split('_')[-1]
            pm.parent(j,j.replace(num,str(int(num)-1)))
            
        # Orient the joints aiming up in Y and Along X
        for jnt in joints:
            if jnt == joints[-1]:
                pm.joint( jnt, e=True, zso=True, oj='none' )
                break
            pm.joint( jnt, e=True, sao='yup', zso=True, oj='xyz' )
            
        return joints[0], joints[-1]

    def advancedSplineIK(self, startJ=None, endJ=None, start=None, nfStart=None):
        ''' 
        Create spline Ik and setup advanced twist
        
        startJ: First joint in spline ik joint chain
        endJ: Last joint in spline ik joint chain
        start: Moving joint (Elbow / Wrist)
        nfStart: Non-Roll joint (Elbow / Wrist)
        '''
        # Create spline IK
        ikHandle = pm.ikHandle( sj=startJ, ee=endJ, 
                                n=startJ.name()+'_IkHandle',
                                solver='ikSplineSolver')
        
        # Setup advanced twist
        pm.setAttr("%s.dTwistControlEnable"%ikHandle[0], 1)
        pm.setAttr("%s.dWorldUpType"%ikHandle[0], 4)
        pm.connectAttr('%s.worldMatrix[0]'%nfStart,'%s.dWorldUpMatrix'%ikHandle[0], f=1)
        pm.connectAttr('%s.worldMatrix[0]'%start,'%s.dWorldUpMatrixEnd'%ikHandle[0], f=1)
        
        # Rename and parent curve to moving joint (Shoulder / Wrist)
        ikHandle[2].rename('%s_splineIkCrv'%nfStart)
        
        return ikHandle[0], ikHandle[2]    

if __name__=="NoRollSetup.NoRollSetup":
    NoRollSetup()