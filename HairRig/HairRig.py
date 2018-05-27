import maya.OpenMayaUI as apiUI
from PyQt4 import QtGui, QtCore, uic
import sip
import os
import pymel.core as pm
import pdb

cwd = os.path.dirname(os.path.abspath(__file__))
uifile = cwd+'/HairRig.ui'
form, base = uic.loadUiType(uifile)

def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QtCore.QObject)

'''
# Run the code in Maya
import sys
path = '/Users/3mo/Documents/repos/arttools/Maya/rigging'
sys.path.append(path)

from HairRig import HairRig
reload(HairRig)
HairRig.HairRig()
'''

'''
v2: 
- List rigs, select rig vs parent to joint.
- Load skin weights
- Dial per chain to determine position on circle of locators

'''
class HairRig(form, base):
    '''
    Tool for creating a hair rig.
    '''
    def __init__(self, parent = getMayaWindow()):
        super(HairRig,self).__init__(parent)
        self.setupUi(self)

        self.actionDirections.triggered.connect( self.ui_showDirections )
        self.numChainsHorizontalSlider.valueChanged.connect( self.ui_drawChains )
        self.loadPushButton.clicked.connect( self.ui_loadSelected )
        self.loadCollisionMeshPushButton.clicked.connect( self.ui_loadSelectedCollisionMesh )
        self.createLocatorsPushButton.clicked.connect( self.ui_createLocators )
        self.createRigPushButton.clicked.connect( self.ui_createRig )

        self.ui_drawChains()

    def ui_loadSelected(self):
        try:
            sel = pm.ls(sl=1)[0]
        except:
            raise Exception('Nothing selected! Please select a joint to attach hair rig.')

        if sel.type() == 'joint':
            self.parentLineEdit.setText(sel.name())
        else:
            raise Exception('Must select a joint in the single heirarchy.')

    def ui_loadSelectedCollisionMesh(self):
        try:
            sel = pm.ls(sl=1)[0]
        except:
            raise Exception('Nothing selected! Please select a collision mesh for the hair rig.')

        if sel.getShape().type() == 'mesh':
            self.collisionMeshLineEdit.setText(sel.name())
        else:
            raise Exception('Must select a collision mesh for the hair rig.')        

    def ui_drawChains(self):
        ''' Create chain entries in scroll view '''
        num = self.numChainsSpinBox.value()
        self.nameFields = []
        self.chainNumLcdFields = []

        # Clear the layout
        self.ui_clearLayout()

        for i in range(num):
            # Group box
            grpBox = QtGui.QGroupBox()
            grpBox.setMaximumHeight(80)
            title = QtCore.QString('chain_%s'%str(i+1))
            grpBox.setTitle(title)
            self.chainVBoxLayout.addWidget(grpBox)           

            # Name
            hLayout = QtGui.QHBoxLayout(grpBox)
            hLayout.addWidget(QtGui.QLabel('Name'))
            chainName = QtGui.QLineEdit(title)
            chainName.setReadOnly(True)
            self.nameFields.append(chainName)
            hLayout.addWidget(chainName)

            # Num joints
            lcd = QtGui.QLCDNumber()
            lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
            sld = QtGui.QSlider(QtCore.Qt.Horizontal) 
            sld.setRange(1,10)
            self.chainNumLcdFields.append(sld)

            hLayout.addWidget(QtGui.QLabel('Joints'))
            hLayout.addWidget(sld) 
            hLayout.addWidget(lcd)

            sld.valueChanged.connect(lcd.display)

    def ui_clearLayout(self):
        for cnt in reversed(range(self.chainVBoxLayout.count())):
            # takeAt does both the jobs of itemAt and removeWidget
            # namely it removes an item and returns it
            widget = self.chainVBoxLayout.takeAt(cnt).widget()

            if widget is not None: 
                # widget will be None if the item is a layout
                widget.deleteLater() 

    def ui_createLocators(self):
        ''' Create main control and locators for user to place '''
        yShift = 3 # Used to space chain locators below root

        parentJnt = str(self.parentLineEdit.text())
        if not parentJnt:
            raise Exception('Please select a parent joint.')

        pos = pm.xform(parentJnt, q=1, ws=1, rp=1)

        if pm.general.objExists('HairRig_MainCnt'):
            choice = pm.confirmBox(title='Hair Rig: Locators already exist', message='Delete Existing Locators?')
            if choice == 'No':
                return
            if choice == None:
                return
            pm.delete('HairRig_MainCnt')

        # Create root control
        mainCnt = pm.circle(radius=3, name='HairRig_MainCnt', 
                            c=pos, nr=(0,1,0), ch=0)[0]
        pm.mel.eval('CenterPivot;')

        # Get chain names and number of joints
        names = []
        numJnts = []
        for nameFld,numJntsFld in zip(self.nameFields,self.chainNumLcdFields):
            names.append(str(nameFld.text()))
            numJnts.append(str(numJntsFld.value()))

        poci = pm.shadingNode('pointOnCurveInfo', asUtility=True)
        pm.connectAttr('%s.ws'%mainCnt.getShape(),'%s.inputCurve'%poci,f=1) 

        increment = 1/len(names)
        for name, numJnt in zip(names,numJnts):
            locatorChains = {}            
            loc = pm.spaceLocator(n='%s_rootLoc'%name)
            locatorChains[loc] = []
            pm.mel.eval('CenterPivot;')
            pm.scale(loc,.5,.5,.5)
            # Aim in negative x to parent joint to set Up vector
            pm.select(parentJnt, loc, replace=1)
            pm.mel.eval('doCreateAimConstraintArgList 1 { "0","0","0","0","-1","0","0","0","1","0","0","1","0","1","vector","","0","0","0","","1" };')


            # Get the initial position
            pm.connectAttr('%s.position'%poci,'%s.translate'%loc,f=1)
            pm.setAttr('%s.parameter'%poci,increment)
            pos = pm.xform(loc,q=1,ws=1,t=1)
            pm.disconnectAttr('%s.position'%poci,'%s.translate'%loc)
            increment = increment + 1

            pm.setAttr('%s.translateX'%loc, pos[0])
            pm.setAttr('%s.translateY'%loc, pos[1])
            pm.setAttr('%s.translateZ'%loc, pos[2])

            pm.parent(loc,mainCnt)

            # Create the rest of the locators
            for n in range(int(numJnt)):
                if n == 0:
                    continue
                l = pm.spaceLocator(n='%s_loc%s'%(name,n))
                pm.delete(pm.parentConstraint(loc,l,mo=False))
                pm.scale(l,.5,.5,.5)
                pm.move(l,0,-(n*yShift),0,r=True)
                locatorChains[loc].append(l)
                pm.parent(l,loc)
                
    def ui_storeUiData(self):
        ''' Store Ui data in variables used by rig methods. '''
        self.parentJnt = str(self.parentLineEdit.text())
        self.collideMesh = str(self.collisionMeshLineEdit.text())

        # Get chain names and number of joints
        self.chainNames = []
        self.chainNumJnts = []
        for nameFld,numJntsFld in zip(self.nameFields,self.chainNumLcdFields):
            self.chainNames.append(str(nameFld.text()))
            self.chainNumJnts.append(str(numJntsFld.value()))

    def ui_showDirections(self):
        ''' Called by Help Menu: Directions '''
        winName = 'HairRigDirectionsWin'
        if pm.window(winName, exists=1):
            pm.deleteUI(winName, window=1)

        pm.window(winName, title='Hair Rig Directions')
        pm.columnLayout(adj=1)

        helpStr = '\n\t1. Load parent joint from Single Heirarchy (SH) joint chain.'
        helpStr = helpStr + '\n\t2. Select number of joint chains to setup.'
        helpStr = helpStr + '\n\t3. Select number of joints for each chain.'
        helpStr = helpStr + '\n\t4. Create locators and place them where you want the joint chains to be made.'
        helpStr = helpStr + '\n\t5. Create the rig.'
        helpStr = helpStr + '\n\n\t Result is a single group parented to world holding a full hair rig.'
        helpStr = helpStr + '\n\n\t SH joints will be placed under rig SH joint parent.'

        pm.text(helpStr, al='left')

        pm.showWindow(winName)

    def ui_createRig(self):
        ''' Call the build methods '''
        if not pm.general.objExists('HairRig_MainCnt'):
            raise Exception('Please create and place loctors first! "HairRig_MainCnt" not found.')
        if pm.general.objExists('HairRig'):
            choice = pm.confirmBox(title='Existing Hair Rig found', message='Delete Existing Hair Rig?')
            if choice == 'No':
                return
            if choice == None:
                return
            pm.delete('HairRig')

        self.ui_storeUiData()
        grps = self.rig_createGroups()
        self.rig_createFkChain(topNode=grps[1])
        self.rig_createDynamicChain(topNode=grps[2])
        self.rig_createShChain()
        self.rig_connectChains()
        self.rig_deleteLocators()

    #----------------------------- 
    # Build methods
    #----------------------------- 
    def rig_createGroups(self): # Returns: [topNode, fkTopNode, dynTopNode]
        topNode = pm.group( n='HairRig', em=True )
        pm.delete( pm.pointConstraint( self.parentJnt, topNode, mo=False ) )

        pm.select(clear=True)
        fkTopNode = pm.group(n='fkTopNode', parent=topNode, em=True)
        pm.select(clear=True)
        dynTopNode = pm.group(n='dynTopNode', parent=topNode, em=True)

        return [topNode, fkTopNode, dynTopNode]
    
    def rig_createShChain(self,parentJnt=None):
        ''' Create the single heirarchy joint chains '''
        for chainName, numJnts in zip(self.chainNames, self.chainNumJnts):
            # Get locator names
            locNames = ['%s_loc%s'%(chainName,num) for num in range(int(numJnts)) if num != 0]
            locNames.insert(0,'%s_rootLoc'%chainName)

            # Get locator positions
            positions = []
            for loc in locNames:
                positions.append(pm.xform(loc,q=1,ws=1,t=1))

            # Draw sh joint chain
            fkJnts = []
            pm.select(self.parentJnt,replace=True)
            for i in range(len(positions)):
                fkJnts.append(pm.joint(name=chainName+'_hr_sh_%s'%i, p=positions[i])) 

    def rig_createFkChain(self, topNode=None):
        ''' Create Fk controls and attributes and SH joint chain '''
        # Get the root locators
        rootLocs = pm.listRelatives('HairRig_MainCnt',children=True)[1:]

        # Per chain
        index = 0
        for chainName, numJnts in zip(self.chainNames, self.chainNumJnts):
            # Chain grp
            chainGrp = pm.group(n=chainName+'_hr_fk_grp', parent=topNode, em=True)
            pm.delete(pm.parentConstraint(rootLocs[index],chainGrp,mo=0))

            # Get locator names
            locNames = ['%s_loc%s'%(chainName,num) for num in range(int(numJnts)) if num != 0]
            locNames.insert(0,'%s_rootLoc'%chainName)

            # Get locator positions
            positions = []
            for loc in locNames:
                positions.append(pm.xform(loc,q=1,ws=1,t=1))

            # Draw fk joint chain
            fkJnts = []
            pm.select(chainGrp,replace=True)
            for i in range(len(positions)):
                fkJnts.append(pm.joint(name=chainName+'_hr_fkJnt_%s'%i, p=positions[i])) 
                
            index = index + 1

            # Create Fk controls and attributes
            label = chainName
            control = 'HairRig_MainCnt'
            fkControl = pm.circle( nr=(0, 0, 1), c=(0, 0, 0), ch=False )[0]

            aim = 'Z'
            twist = 'Y'
            up = 'X'

            # Create main attributes on control
            pm.select(control,r=True)
            attList = pm.attributeInfo(control,all=True)

            if(label not in attList):
                try:
                    pm.addAttr(longName=label,k=True)
                    pm.setAttr(control + '.' + label, lock=True)
                except:
                    pass #Attribute already exists

            #Get data for current limb
            startJnt = pm.listRelatives(chainGrp,children=True)[0]
            pm.select(pm.listRelatives(chainGrp,children=True)[0], hi=True)
            endJnt = pm.ls(sl=1)[-1]

            #Get full chain
            chain = []

            #Get the hierarchy of startJnt, then store it until endJnt is found
            try:
                pm.select(startJnt,r=True,hi=True)
                sel = pm.ls(sl=True,fl=True,type='joint')
                tempChain = sel

                for each in tempChain:
                    if each == endJnt:
                        chain.append(each)
                        break
                    else:
                        chain.append(each)
            except:
                pass

            #Store parent of chain
            parent = pm.listRelatives( chain[0], parent=True)

            #Unparent joints
            for each in chain:
                try:
                    pm.parent(each,w=True)
                except:
                    pass

            #Create duplicate joints above orig joints, then store duplicate joint names
            dupJoints = []
            for joint in chain:
                offName = joint + '_off'
                jnt = pm.duplicate(joint,rr=True,po=True,n=offName)
                dupJoints.append(jnt)

            #Rebuild heirarchy
            x = 0
            while x < len(chain):
                pm.parent(chain[x],dupJoints[x])
                if x != 0:
                    pm.parent(dupJoints[x],chain[x-1])
                x = x + 1

            # Add dynamic switch attribute
            pm.addAttr( control, longName=chainName + '_dynamic', k=True, min=0, max=1 )

            #Adding Curl atts on controller
            x= 0 
            while x < len(chain):
                pm.addAttr(control, longName=chainName + '_curl_' + str(x+1),k=True)
                x = x + 1

            #Adding spread atts on controller
            x= 0 
            while x < len(chain):
                pm.addAttr(control, longName=chainName + '_spread_' + str(x+1),k=True)
                x = x + 1

            #Twist
            pm.addAttr(control, longName=chainName + '_Twist',k=True)

            #Connect attributes to dupJoints rotate's ( aim = curl, up = spread )
            x = 0
            pm.connectAttr( control + '.' + chainName + '_Twist' , str(dupJoints[x][0]) + '.rotate' + twist ) 
            while x < len(chain):
                pm.connectAttr( control + '.' + chainName + '_curl_' + str(x+1) , str(dupJoints[x][0]) + '.rotate' + aim )
                pm.connectAttr( control + '.' + chainName + '_spread_' + str(x+1), str(dupJoints[x][0]) + '.rotate' + up )
                x = x + 1

            #Create fk controllers on joints
            #Duplicate FK control, parent it to chain joints, delete left over transform node
            for each in chain:
                #Duplicate control
                tempCnt = pm.duplicate(fkControl)
                #Select the shape
                tempShp = pm.pickWalk(tempCnt,direction='down')
                pm.parent(tempShp,each,r=True,s=True)
                pm.delete(tempCnt)
            
            pm.parent( dupJoints[0], chainGrp )
            pm.delete( fkControl )
            
            pm.parentConstraint( 'HairRig_MainCnt', chainGrp, mo=True )

    def rig_createDynamicChain(self, topNode=None): # Returns: [DynJoints], [DynControl], Transform(DynTopNode)
        ''' Create dynamic joint chain '''
        # Get the root locators
        rootLocs = pm.listRelatives('HairRig_MainCnt',children=True)[1:]

        # Per chain
        index = 0
        for chainName, numJnts in zip(self.chainNames, self.chainNumJnts):
            index = index + 1
            
            # Chain grp
            chainGrp = pm.group(n=chainName+'_dyn_grp', parent=topNode, em=True)
            pm.delete(pm.parentConstraint(rootLocs[index-1],chainGrp,mo=0))

            # Get locator names
            locNames = ['%s_loc%s'%(chainName,num) for num in range(int(numJnts)) if num != 0]
            locNames.insert(0,'%s_rootLoc'%chainName)

            # Get locator positions
            positions = []
            for loc in locNames:
                positions.append( pm.xform(loc,q=1,ws=1,t=1) )

            # Draw dynamic joint chain
            dynJnts = []
            pm.select(chainGrp,replace=True)
            for i in range(len(positions)):
                dynJnts.append(pm.joint(name=chainName+'_hr_dynJnt_%s'%i, p=positions[i]))
            
            # Draw curve along dynamic chain
            positions = []
            for jnt in dynJnts:
                positions.append(pm.xform(jnt,q=1,ws=1,rp=1))
            crv = pm.curve( name='chain%s_crv'%index, p=positions, d=1 )
            pm.rebuildCurve( crv, s=5 )
            pm.xform( crv, rp=positions[0], ws=True )
            pm.delete( crv, ch=True )
            pm.parent( crv, topNode )
            
            # Create root nurbs plane
            plane = pm.nurbsPlane( name='dynPlane_%s'%index, d=3, u=2, v=2, ax=[0,-1,0] )[0]
            pm.move(plane, float(positions[0][0]), float(positions[0][1]), float(positions[0][2]), a=1)
            pm.parent( plane, chainGrp )
            
            #Get data for current limb
            startJnt = pm.listRelatives( chainGrp, children=True )[0]
            pm.select(pm.listRelatives( chainGrp, children=True )[0], hi=True )
            endJnt = pm.ls(sl=1)[-1]

            # Make curve dynamic
            pm.select( plane, r=True )
            pm.select( crv, add=True )
            pm.mel.eval( 'makeCurvesDynamicHairs %d %d %d' % (1, 0, 1) )
            
            # Get names for hair system
            temp = pm.pickWalk( crv, d='up' )
            hairSystemName = 'hairSystem%s'%index
            dynCrv = pm.listRelatives( '%sOutputCurves'%hairSystemName,  children=True)[0]
            pm.rename(dynCrv,'dynCrv_%s'%index)
            dynCrv = 'dynCrv_%s'%index
            pm.parent( hairSystemName, chainGrp )
            
            # Make ik spline using dynamic curve
            handle, effector = pm.ikHandle( sj=startJnt, ee=endJnt, sol='ikSplineSolver', c=dynCrv, ccv=False )
            pm.parent( handle, chainGrp )
            
            # Clean up
            follicle = pm.listRelatives( crv, parent=True )[0]
            pm.parent( crv, 'HairRig_MainCnt' )
            pm.parent( follicle, chainGrp )
            pm.delete( '%sOutputCurves'%hairSystemName )
            
            pm.setAttr( '%s.visibility'%follicle, 0 )
            pm.setAttr( '%s.visibility'%crv, 0 )
            pm.setAttr( '%s.visibility'%dynCrv, 0 )
            pm.setAttr( '%s.visibility'%handle, 0 )
            pm.setAttr( '%s.visibility'%plane, 0 )
            pm.setAttr( '%s.visibility'%hairSystemName, 0 )
            
            # Create attributes on main control
            
        return dynJnts

    def rig_connectChains(self):
        for chain in self.chainNames:
            consts = []
            pm.select('%s_hr_sh_0'%chain, hi=True, r=True)
            shJnts = pm.ls(sl=True)
            for jnt in shJnts:
                const = pm.parentConstraint(jnt.replace('sh','dynJnt'),
                                    jnt.replace('sh','fkJnt'),
                                    jnt, mo=True) 
                pm.connectAttr('HairRig_MainCnt.%s_dynamic'%chain,'%s.%sW0'%(const,jnt.replace('sh','dynJnt')),f=True)
                pm.setDrivenKeyframe( '%s.%sW1'%(const, jnt.replace('sh','fkJnt')), cd='HairRig_MainCnt.%s_dynamic'%chain, dv=0, v=1 )
                pm.setDrivenKeyframe( '%s.%sW1'%(const, jnt.replace('sh','fkJnt')), cd='HairRig_MainCnt.%s_dynamic'%chain, dv=1, v=0 )
                
    def rig_deleteLocators(self):
        locs = [ x for x in pm.listRelatives('HairRig_MainCnt', children=True) if 'Loc' in x ]
        pm.delete(locs)

def main():
    global win
    try:
        win.close()
    except:
        pass
    win = HairRig()
    win.show()


if __name__=="HairRig.HairRig":
    main()