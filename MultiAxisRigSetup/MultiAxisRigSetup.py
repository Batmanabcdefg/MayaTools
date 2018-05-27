import logging
import math

import maya.cmds as cmds
import maya.mel as mel

class MultiAxisRigSetup(object):
    def __init__(self,version='1.0',log=False,loglevel=logging.DEBUG,logFileMode='a'):
        self.version = version
        self.logger=None
        if log:
            # Setup logging
            logging.basicConfig( level=logging.DEBUG, fileName='MultiAxisRigSetup.log',filemode=logFileMode, 
                                 format= '%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                 datefmt='%m/%d/%Y %I:%M:%S %p' )
            self.logger = logging.getLogger('MultiAxisRigSetupLog')

        # Start logging
        if self.logger: self.logger.info('MultiAxisRigSetup %s: Initialized...'%self.version)        
    
    def createRig(self, name=None,
                        baseTransform=None,
                        targetTransform=None,
                        control=None,
                        aim='y',up='z',wup='y'):
        ''' Setup multi-axis rig '''
        if self.logger: self.logger.info('createRig(): Starting...') 
        
        # Create the plane
        plane = self._createPlane(name=name,
                        baseTransform=baseTransform,
                        targetTransform=targetTransform,
                        aim=aim,up=up,wup=wup)
        
        # Create the locator
        loc = self._createLoc(name=name,
                                baseTransform=baseTransform,
                                targetTransform=targetTransform,
                                plane=plane)
        
        # Setup closestPointOnSurface
        cposNode = self._setupCPOS(name=name,plane=plane,loc=loc)      \
            
        # Setup Rig Heirarchy
        topGrp = self._setupRigHeirarchy(name=name,
                                            baseTransform=baseTransform,
                                            plane=plane,
                                            loc=loc)      
        # Create Attrs
        self._createAttrs(name=name, control=control, node=cposNode)
    
        if self.logger: self.logger.info('createRig(): End.') 
        
    def _createPlane(self,name=None,
                        baseTransform=None,
                        targetTransform=None,
                        aim=None,up=None,wup=None):
        if self.logger: self.logger.info('_createPlane(): Starting...')
        
        # Define vectors
        if aim == 'x': aimV = [1,0,0]
        if aim == 'y': aimV = [0,1,0]
        if aim == 'z': aimV = [0,0,1]
        
        if up == 'x': upV = [1,0,0]
        if up == 'y': upV = [0,1,0]
        if up == 'z': upV = [0,0,1]  
        
        if wup == 'x': wupV = [1,0,0]
        if wup == 'y': wupV = [0,1,0]
        if wup == 'z': wupV = [0,0,1]  
        
        # Get distance between base and target
        p1 = cmds.xform(baseTransform,q=1,ws=1,rp=1)
        p2 = cmds.xform(targetTransform,q=1,ws=1,rp=1)
        dist = math.sqrt( (p2[0]-p1[0])*(p2[0]-p1[0]) + \
                          (p2[1]-p1[1])*(p2[1]-p1[1]) + \
                          (p2[2]-p1[2])*(p2[2]-p1[2]) )
        
        # Create the plane
        plane = cmds.nurbsPlane(n=name+'_multiAxisRigPlane',axis=[0,90,0])[0]
        cmds.delete(plane,ch=True)
        
        # Snap/Constraint to baseTransform
        cmds.pointConstraint(baseTransform,plane,mo=False,n=name+'_multiAxisRigPlanePointConst')
        
        # Scale it so plane is twice the length of the base/target distance
        cmds.setAttr('%s.scaleX'%plane, dist*2)
        cmds.setAttr('%s.scaleY'%plane, dist*2)
        cmds.setAttr('%s.scaleZ'%plane, dist*2)
        
        # Aim at targetTransform
        cmds.delete( cmds.aimConstraint(targetTransform,plane,aim=aimV,u=upV) )
        
        if self.logger: self.logger.info('_createPlane(): End...\nReturned: %s'%plane)
        return plane
    
    def _createLoc(self,name=None,
                        baseTransform=None,
                        targetTransform=None,
                        plane=None):
        if self.logger: self.logger.info('_createLoc(): Starting...')
        
        # Create the locator
        loc = cmds.spaceLocator(n=name+'_multiAxisRigLoc')[0]
        
        # Snap to base
        cmds.delete(cmds.pointConstraint(baseTransform,loc,mo=False))
        
        # Constrain to plane
        cmds.geometryConstraint( plane, loc, n=name+'_multiAxisRigLocGeoConst' )
        
        # pointConst to target
        cmds.pointConstraint( targetTransform, loc, mo=True, n=name+'+multiAxisRigLocPointConst' )
    
        if self.logger: self.logger.info('_createLoc(): End...\nReturned: %s'%loc)
        return loc    
    
    def _setupCPOS(self,name=None,plane=None,loc=None):
        if self.logger: self.logger.info('_setupCPOS(): Starting...')
        
        # Create the node
        cposNode = cmds.createNode('closestPointOnSurface',n=name+'_multiAxisRigCPOS')

        # Connect the plane to the node
        cmds.connectAttr('%s.worldSpace[0]'%plane,'%s.inputSurface'%cposNode,f=True) 
        
        # Connect the loc to the node
        cmds.connectAttr('%s.worldPosition'%loc,'%s.inPosition'%cposNode,f=True) 
        
        if self.logger: self.logger.info('_setupCPOS(): End...\nReturned: %s'%cposNode)
        return cposNode         

    def _setupRigHeirarchy(self, name=None, baseTransform=None, plane=None, loc=None):
        if self.logger: self.logger.info('_setupRigHeirarchy(): Starting...')
        
        # Group the plane and locator
        topGrp = cmds.group(em=True,n=name+'_multiAxisRigGrp')
        
        # Snap pivot to baseTransform
        cmds.xform(topGrp,ws=1,rp=cmds.xform(baseTransform,q=1,ws=1,rp=1))
        
        # ParentConstrain to baseTransform parent
        parent = cmds.listRelatives(baseTransform,parent=True)[0]
        cmds.parentConstraint(parent,topGrp,mo=True,n=name+'_multiAxisRigGrpParentConst')
        
        # Parent plane and loc to topGrp
        cmds.parent(plane,loc,topGrp)
        
        if self.logger: self.logger.info('_setupRigHeirarchy(): End...\nReturned: %s'%topGrp)
        return topGrp
    
    def _createAttrs(self, name=None, control=None, node=None):
        if self.logger: self.logger.info('_createAttrs(): Starting...')
        
        # Add the attributes
        attrU = '%s_u'%name
        cmds.addAttr(control,ln=attrU,min=0,max=1.0,dv=0.0)
        cmds.setAttr('%s.%s'%(control,attrU),k=True,l=False)
        attrV = '%s_v'%name
        cmds.addAttr(control,ln=attrV,min=0,max=1.0,dv=0.0)
        cmds.setAttr('%s.%s'%(control,attrV),k=True,l=False)  
        
        # Connect to the cposNode
        cmds.connectAttr('%s.u'%node,'%s.%s'%(control,attrU),f=True)
        cmds.connectAttr('%s.v'%node,'%s.%s'%(control,attrV),f=True)
        
        if self.logger: self.logger.info('_createAttrs(): End...')

    #---------------------------------------------------------------------------------------------
    def ui(self):
        if cmds.window('MultiAxesRigSetupWin',exists=True):
            cmds.deleteUI('MultiAxesRigSetupWin' ,window=True)
        window = cmds.window( 'MultiAxesRigSetupWin' , title="Multi Axis Rig Setup v%s"%self.version )

        cmds.columnLayout( adjustableColumn=True )

        cmds.columnLayout( adjustableColumn=True )
        self.nameFld = cmds.textFieldGrp( label='Rig Name' )
        cmds.setParent( '..' )
        
        cmds.columnLayout( adjustableColumn=True )
        self.baseFld = cmds.textFieldButtonGrp( label='Base Object (Shoulder)', bl='Load', bc=self._loadBase )
        cmds.setParent('..')
        
        cmds.columnLayout( adjustableColumn=True )
        self.tgtFld = cmds.textFieldButtonGrp( label='Target Object (Elbow)', bl='Load', bc=self._loadTgt )
        cmds.setParent('..')
        
        cmds.columnLayout( adjustableColumn=True )
        self.controlFld = cmds.textFieldButtonGrp( label='Control to put attrs on', bl='Load', bc=self._loadControl )
        cmds.setParent('..')
        
        cmds.columnLayout( adjustableColumn=True )
        cmds.button( label='Create Rig', c=self._callCreateRig )
        cmds.setParent('..')        
        
        cmds.showWindow( window )

    def _loadBase(self,*args):
        sel = cmds.ls(sl=True)[0]
        cmds.textFieldButtonGrp(self.baseFld,e=True,text=sel)
        
    def _loadTgt(self,*args):
        sel = cmds.ls(sl=True)[0]
        cmds.textFieldButtonGrp(self.tgtFld,e=True,text=sel)
        
    def _loadControl(self,*args):
        sel = cmds.ls(sl=True)[0]
        cmds.textFieldButtonGrp(self.controlFld,e=True,text=sel) 
        
    def _callCreateRig(self,*args):
        name = cmds.textFieldGrp(self.nameFld,q=True,text=True)
        baseObj = cmds.textFieldButtonGrp(self.baseFld,q=True,text=True)
        tgtObj = cmds.textFieldButtonGrp(self.tgtFld,q=True,text=True)
        controlObj = cmds.textFieldButtonGrp(self.controlFld,q=True,text=True)
        self.createRig(name=name,baseTransform=baseObj,targetTransform=tgtObj,control=controlObj)