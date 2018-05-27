import logging
import math
import sys
from re import search
import os

from pymel import core as pm
import maya.cmds as cmds
import maya.mel as mel

class RibbonRig(object):
    def __init__(self,version='1.0',log=False,loglevel=logging.DEBUG,logFileMode='a'):
        ''' Set version and initialize logging '''
        self.version = version
        self.logger=None
        if log:
            # Setup logging
            logging.basicConfig( level=logging.DEBUG, fileName='RibbonRig.log',filemode=logFileMode, 
                                 format= '%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                 datefmt='%m/%d/%Y %I:%M:%S %p' )
            self.logger = logging.getLogger('RibbonRigLog')

        # Start logging
        if self.logger: 
            self.logger.info('RibbonRig %s: Initialized...'%self.version)        
    
    def createRig(self, name=None, startObj=None, endObj=None, startUpObj=None,
                  normal=None, up=None, aim=None, numJnts=None):        
        ''' 
        Create a ribbon rig based on user input. 
        
        name -- Prefix used for naming the rig
        startObj -- Start transform that rig will be parented to.
        endObj -- End transform that rig will be parented to.
        normal -- Plane normal. Example: [1,0,0]
        up -- Plane up vector
        aim -- Aim plane at endObj vector
        numJnts -- Number of joints to make that follow the nurbs plane
        '''
        if self.logger:
            self.logger.info('createRig(): Starting...')  
            
        if cmds.objExists(name+'_rbbnTopNode'):
            raise Exception('"%s" is not a unique name. "%s_rbbnTopNode" already exists.'%(name,name))
            
        plane = self._createPlane(name=name,
                                  start=startObj,
                                  end=endObj,
                                  normal=normal,
                                  up=up,
                                  aim=aim,
                                  spans=numJnts)
        locators = self._createLocators(name=name, start=startObj, end=endObj, startUpObj=startUpObj)
        follicles = self._createFollicles(name=name, plane=plane, num=numJnts)
        self._constrainLocators(locators=locators)
        bindJnts = self._createBindJoints(name=name, parents=follicles)
        rbbnJnts = self._createPlaneJoints(locs=[locators['topLocs'][1][0],
                                                     locators['midLocs'][3][0],
                                                     locators['btmLocs'][1][0]])
        skinCluster = self._skinPlane(plane=plane, joints=rbbnJnts)
        fGrp = cmds.listRelatives(cmds.listRelatives(follicles[0], parent=True)[0],parent=True)[0]
        locGrp = cmds.listRelatives(locators['topLocs'][0][0], parent=True)[0]
        self._setupHeirarchy(name=name, startObj=startObj, endObj=endObj,
                             locGrp=locGrp, plane=plane, follicleGrp=fGrp)
        
        if self.logger:
            self.logger.info('createRig(): End.')         
    
    def _createPlane(self, name=None, start=None,
                    end=None, normal=[0,1,0], up=[1,0,0], 
                    spans=None, aim=[1,0,0]):
        ''' 
        Create the plane for the ribbon rig.
        Returns: 'name_rbbnPlane'
        
        name -- Name for the plane.
        start -- Name of transform to use as start position.
        end -- Name of transform to use as end position.
        normal -- Normal of the plane.
        spans -- Number of spans in V.
        up -- World up vector.
        aim -- Axis used to aim plane at end transform.
        '''
        if self.logger:
            self.logger.info('_createPlane(): Starting...')    
            
        #--- Make sure all needed arguments provided by caller
        if not name:
            if self.logger:
                self.logger.error('_createPlane(): No name passed in by caller.')
            raise Exception('No name passed in by caller.')
        if not start:
            if self.logger:
                self.logger.error('_createPlane(): No start transform name passed in by caller.')
            raise Exception('No start transform name passed in by caller.')        
        if not end:
            if self.logger:
                self.logger.error('_createPlane(): No end transform name passed in by caller.')
            raise Exception('No end transform name passed in by caller.') 
        if not spans:
            if self.logger:
                self.logger.error('_createPlane(): Number of spans not passed in by caller.')
            raise Exception('Number of spans not passed in by caller.') 
        
        #--- Calculate distance between start and end transforms. Used for the plane length.
        try:
            startPos = cmds.xform(start,q=1,ws=1,rp=1)
            endPos = cmds.xform(end,q=1,ws=1,rp=1)
            dist = math.sqrt( ((endPos[0]) - (startPos[0])) * ((endPos[0]) - (startPos[0])) +\
                              ((endPos[1]) - (startPos[1])) * ((endPos[1]) - (startPos[1])) +\
                              ((endPos[2]) - (startPos[2])) * ((endPos[2]) - (startPos[2])) )
        except Exception,e:
            if self.logger:
                self.logger.error('_createPlane(): Error getting distance from start to end transforms: %s'%e)
            raise Exception(e)  
        
        #--- Create the plane
        try:
            plane = cmds.nurbsPlane(name=name+'_rbbnPlane', w=1, lengthRatio=dist, d=3, u=1, v=spans, ax=normal)[0]
            if self.logger:
                self.logger.info('_createPlane(): Created plane: %s'%plane)            
        except Exception,e:
            if self.logger:
                self.logger.error('_createPlane(): Error creating plane: %s'%e)
            raise Exception(e)
        
        #--- Rebuild the plane
        try:
            cmds.rebuildSurface(plane,rt=1,du=1,dv=3)
            cmds.rebuildSurface(plane,rt=0,su=1,sv=spans,du=1,dv=3)
            if self.logger:
                self.logger.info('_createPlane(): Rebuilt surface.')           
        except Exception,e:
            if self.logger:
                self.logger.error('_createPlane(): Error creating plane: %s'%e)     
            raise Exception(e)
        
        #--- Delete history
        try:
            cmds.select(plane,r=True)
            mel.eval('DeleteHistory;')
            cmds.select(clear=True)
            if self.logger:
                self.logger.info('_createPlane(): Deleted surface history.')           
        except Exception,e:
            if self.logger:
                self.logger.error('_createPlane(): Error deleting plane history: %s'%e)     
            raise Exception(e)
        
        #--- Transform the plane
        try:
            # Point constraint to start & end transforms
            cmds.delete(cmds.pointConstraint(start,end,plane,mo=False))
        except Exception,e:
            if self.logger:
                self.logger.error('_createPlane(): Error point constraining plane: %s'%e)     
            raise Exception(e)        
        
        # Aim constraint to end
        try:
            cmds.delete(cmds.aimConstraint(end,plane,aim=aim,u=up,mo=False))
        except Exception,e:
            if self.logger:
                self.logger.error('_createPlane(): Error aim constraining plane: %s'%e)     
            raise Exception(e)
        
        #--- Return the name of the plane
        if self.logger:
            self.logger.info('_createPlane(): Done: Returned: %s'%plane)   
        return plane
        
    def _createLocators(self, name=None, start=None, end=None, startUpObj=None, dist=10):
        ''' 
        Create top, mid, btm locators 
        
        name -- Name to use as prefix
        start -- Start transform in scene
        end --- End transform in scene
        startUpObj -- Transform used to define up vector: start -> startUpObj
        dist -- Distance to move up locator
        '''
        if self.logger:
            self.logger.info('_createLocators(): Starting...')         

        if not name:
            if self.logger:
                self.logger.error('_createLocators(): No name passed in by caller.')
            raise Exception('No name passed in by caller.')
        if not startUpObj:
            if self.logger:
                self.logger.error('_createLocators(): No up object passed in by caller.')
            raise Exception('No up object passed in by caller.')
        if not start:
            if self.logger:
                self.logger.error('_createLocators(): No start transform name passed in by caller.')
            raise Exception('No start transform name passed in by caller.')        
        if not end:
            if self.logger:
                self.logger.error('_createLocators(): No end transform name passed in by caller.')
            raise Exception('No end transform name passed in by caller.') 
        
        #--- Get position of start and end
        startPos = cmds.xform(start, q=1, ws=1, rp=1)
        endPos = cmds.xform(end, q=1, ws=1, rp=1)
        
        #--- Create the locators
        topLocs = []
        topLocs.append(cmds.spaceLocator(n='%s_topLoc_pos'%name))
        topLocs.append(cmds.spaceLocator(n='%s_topLoc_aim'%name))
        topLocs.append(cmds.spaceLocator(n='%s_topLoc_up'%name))
        for each in topLocs:
            cmds.select(each,r=True)
            mel.eval('CenterPivot;')
            cmds.select(clear=True)            
            cmds.move(endPos[0], endPos[1], endPos[2], each, r=True) 
            
        midLocs = []
        midPos = [ (endPos[0]+startPos[0])/2.0, (endPos[1]+startPos[1])/2.0, (endPos[2]+startPos[2])/2.0 ]
        midLocs.append(cmds.spaceLocator(n='%s_midLoc_pos'%name))
        midLocs.append(cmds.spaceLocator(n='%s_midLoc_aim'%name))
        midLocs.append(cmds.spaceLocator(n='%s_midLoc_up'%name))   
        midLocs.append(cmds.spaceLocator(n='%s_midLoc_off'%name))
        for each in midLocs:
            cmds.select(each,r=True)
            mel.eval('CenterPivot;')
            cmds.select(clear=True)            
            cmds.move(midPos[0], midPos[1], midPos[2], each, r=True)         
            
        btmLocs = []
        btmLocs.append(cmds.spaceLocator(n='%s_btmLoc_pos'%name))
        btmLocs.append(cmds.spaceLocator(n='%s_btmLoc_aim'%name))
        btmLocs.append(cmds.spaceLocator(n='%s_btmLoc_up'%name))
        for each in btmLocs:
            cmds.select(each,r=True)
            mel.eval('CenterPivot;')
            cmds.select(clear=True)            
            cmds.move(startPos[0], startPos[1], startPos[2], each, r=True)         
            
        #--- Get up vector
        upObjPos = cmds.xform(startUpObj, q=1, ws=1, rp=1)
        up = pm.dt.Vector((upObjPos[0]-startPos[0]), (upObjPos[1]-startPos[1]), (upObjPos[2]-startPos[2]))
        up.normalize()
        
        objVector = [abs(endPos[0]-startPos[0]), abs(endPos[1]-startPos[1]), abs(endPos[2]-startPos[2])]
        diff_x = self._angleBetween(objVector, [1, 0, 0])
        diff_y = self._angleBetween(objVector, [0, 1, 0])
        diff_z = self._angleBetween(objVector, [0, 0, 1])
        
        if diff_x >= diff_y and diff_x >= diff_z:
            aim=[0, 1, 0]
            
        if diff_y >= diff_x and diff_y >= diff_z:
            aim=[1, 0, 0]
            
        if diff_z >= diff_y and diff_z >= diff_x:
            aim=[0, 1, 0]
            
        if self.logger:
            self.logger.info('_createLocators(): Local up vector: %s'%up)    

        #--- Aim the top/btm pos locators
        temp = cmds.aimConstraint(btmLocs[0][0], 
                                  topLocs[0][0], 
                                  aim=aim, u=up, 
                                  worldUpType='object', 
                                  worldUpObject=topLocs[2][0],
                                  mo=False)
        cmds.delete(temp)        
        
        temp = cmds.aimConstraint(topLocs[0][0], 
                                  btmLocs[0][0], 
                                  aim=aim, u=up, 
                                  worldUpType='object', 
                                  worldUpObject=btmLocs[2][0],
                                  mo=False)
        cmds.delete(temp)
        
        #--- Parent the locators
        cmds.parent(topLocs[1], topLocs[2], topLocs[0])
        cmds.parent(midLocs[1], midLocs[2], midLocs[0])
        cmds.parent(midLocs[3], midLocs[1])
        cmds.parent(btmLocs[1], btmLocs[2], btmLocs[0])
        
        #--- Move the up locators by up vector       
        cmds.move(10*up[0]+endPos[0], 10*up[1]+endPos[1], 10*up[2]+endPos[2], topLocs[2], wd=True, ws=1)
        cmds.move(10*up[0]+midPos[0], 10*up[1]+midPos[1], 10*up[2]+midPos[2], midLocs[2], wd=True, ws=1)
        cmds.move(10*up[0]+startPos[0], 10*up[1]+startPos[1], 10*up[2]+startPos[2], btmLocs[2], wd=True, ws=1)  
        
        topGrp = cmds.group(n=name+'_rbbnLocatorsGrp',em=True)
        cmds.parent(topLocs[0], midLocs[0], btmLocs[0], topGrp)
        
        if self.logger:
            self.logger.info('_createLocators(): End.') 
        
        return {'topLocs':topLocs, 'midLocs':midLocs, 'btmLocs':btmLocs, 'topGrp':topGrp}
    
    def _createFollicles(self, name=None, plane=None, num=None):
        ''' 
        Create the plane for the ribbon rig.
        Returns: 'name_rbbnPlane'
        
        name -- Name for the plane.
        plane -- Nurbs plane to place follicles
        num -- Number of follicles to create
        '''
        if self.logger:
            self.logger.info('_createFollicles(): Starting...')        
        #--- Make sure all needed arguments provided by caller
        if not name:
            if self.logger:
                self.logger.error('_createFollicles(): No name passed in by caller.')
            raise Exception('No name passed in by caller.')
        if not plane:
            if self.logger:
                self.logger.error('_createFollicles(): No plane name passed in by caller.')
            raise Exception('No plane name passed in by caller.')        
        if not num:
            if self.logger:
                self.logger.error('_createFollicles(): No number of follicles passed in by caller.')
            raise Exception('No number of follicles passed in by caller.') 
        
        #--- Create the follicles
        cmds.select(plane, r=True)
        planeObj = pm.selected()[0]
        cmds.select(clear=True)
        follicles = []
        for i in range(0,num):
            follicles.append( self.create_follicle( obj=planeObj, name=name, count=i+1, uPos=0.5, vPos=i/(num-1.00)) )
            
        grp = cmds.group(n=name+'_rbbnFollicles_grp',em=True)
        for each in follicles:
            cmds.parent(cmds.listRelatives(each,parent=True)[0], grp)
            
        if self.logger:
            self.logger.info('_createFollicles(): End.')    
            
        return follicles
    
    def create_follicle(self, obj, name, count=1, uPos=0.0, vPos=0.0):
        ''' Manually place and connect a follicle onto a nurbs surface. '''
        if obj.type() == 'transform':
            shape = obj.getShape()
        elif obj.type() == 'nurbsSurface':
            shape = obj.getShape()
        else:
            'Warning: Input must be a nurbs surface.'
            return False
        
        # create a name with frame padding
        #pName = '_'.join([name, obj.name(), str(count).zfill(2)])
        fName = '_'.join([name, (obj.name()+'ShapeFollicle'), str(count).zfill(2)])
        oFoll = pm.createNode('follicle', name=fName)
        shape.local.connect(oFoll.inputSurface)
        
        p = oFoll.getParent().name()
        tName = '_'.join([name, (obj.name()+'Follicle'), str(count).zfill(2)])
        cmds.rename(p,tName)
        # if using a polygon mesh, use this line instead.
        # (The polygons will need to have UVs in order to work.)
        #oMesh.outMesh.connect(oFoll.inMesh)
    
        shape.worldMatrix[0].connect(oFoll.inputWorldMatrix)
        oFoll.outRotate.connect(oFoll.getParent().rotate)
        oFoll.outTranslate.connect(oFoll.getParent().translate)
        oFoll.parameterU.set(uPos)
        oFoll.parameterV.set(vPos)
        oFoll.getParent().t.lock()
        oFoll.getParent().r.lock()
    
        return oFoll.name()    
    
    def _constrainLocators(self,locators=None):
        '''
        Constrain locators for stretch / aim / twist behaviour.
        
        locators * -- Locators to constrain: { 'topLocs':[['name_topLoc_pos'], ['name_topLoc_aim'], ['name_topLoc_up']],
                                             'midLocs':[['name_midLoc_pos'], ['name_midLoc_aim'], ['name_midLoc_up'], ['name_midLoc_off']],
                                             'btmLocs':[['name_btmLoc_pos'], ['name_btmLoc_aim'], ['name_btmLoc_up']]  }
        
        * This is the return value of _createLocators()
        '''
        if self.logger:
            self.logger.info('_constrainLocators(): Starting...')  
            
        if not locators:
            if self.logger:
                self.logger.error('_constrainLocators(): No locators passed in by caller.')
            raise Exception('No locators passed in by caller.')

        cmds.aimConstraint(locators['btmLocs'][0][0], locators['topLocs'][1][0], aim=[0,-1,0], u=[1,0,0], worldUpType='object', worldUpObject=locators['topLocs'][2][0],mo=False)
        cmds.aimConstraint(locators['topLocs'][0][0], locators['btmLocs'][1][0], aim=[0,1,0], u=[1,0,0], worldUpType='object', worldUpObject=locators['btmLocs'][2][0],mo=False)
        cmds.aimConstraint(locators['topLocs'][0][0], locators['midLocs'][1][0], aim=[0,1,0], u=[1,0,0], worldUpType='object', worldUpObject=locators['midLocs'][2][0],mo=False)
        
        cmds.pointConstraint(locators['topLocs'][0][0], locators['btmLocs'][0][0], locators['midLocs'][0][0], mo=True)
        cmds.pointConstraint(locators['topLocs'][2][0], locators['btmLocs'][2][0], locators['midLocs'][2][0], mo=True)

        if self.logger:
            self.logger.info('_constrainLocators(): End.')        
            
    def _createBindJoints(self,name,parents=None):
        '''
        Given list of parent objects, create a joint per parent that
        is a child of the parent, with zerod transforms.
        
        parents -- List of trasforms to create joints underneath of.
        '''
        if self.logger:
            self.logger.info('_createBindJoints(): Starting...')
            
        if not name:
            if self.logger:
                self.logger.error('_createBindJoints(): No name passed in by caller.')
            raise Exception('No name passed in by caller.')
            
        if not parents:
            if self.logger:
                self.logger.error('_createBindJoints(): No parents passed in by caller.')
            raise Exception('No parents passed in by caller.')   
        
        joints = []
        for p in parents:
            j = cmds.joint(n=name+'_'+p.split('_')[-1]+'_jnt_deform',p=cmds.xform(cmds.listRelatives(p,parent=1)[0],q=1,ws=1,rp=1))
            cmds.parent(j,p)
            joints.append(j)

        if self.logger:
            self.logger.info('_createBindJoints(): End.') 
        return joints
    
    def _createPlaneJoints(self,locs=None):
        '''
        Given list ['btm_aim','mid_off','top_aim'] locators, create a joint per locator that
        is a child of the locator, with zerod transforms.
        
        locs -- Top, mid, btm aim locators for the ribbon setup.
        '''
        if self.logger:
            self.logger.info('_createPlaneJoints(): Starting...')  
            
        if not locs:
            if self.logger:
                self.logger.error('_createPlaneJoints(): No locs passed in by caller.')
            raise Exception('No locs passed in by caller.') 
        
        joints = []
        for l in locs:
            j = cmds.joint(n=l+'_rbbn_jnt',p=cmds.xform(l,q=1,ws=1,rp=1))
            cmds.parent(j,l)
            joints.append(j)

        if self.logger:
            self.logger.info('_createPlaneJoints(): End.') 
        return joints
    
    def _skinPlane(self,plane=None, joints=None):
        '''
        Given list with three aim locators, create a joint per locator that
        is a child of the locator, with zerod transforms.
        
        locs -- Top, mid, btm aim locators for the ribbon setup.
        '''
        if self.logger:
            self.logger.info('_skinPlane(): Starting...')  
            
        if not plane:
            if self.logger:
                self.logger.error('_skinPlane(): No plane passed in by caller.')
            raise Exception('No plane passed in by caller.')
        if not joints:
            if self.logger:
                self.logger.error('_skinPlane(): No joints passed in by caller.')
            raise Exception('No joints passed in by caller.')        
        
        sc = cmds.skinCluster(joints,plane,dr=10)

        if self.logger:
            self.logger.info('_skinPlane(): End.') 
            
        return sc
    
    def _setupHeirarchy(self, name=None, startObj=None, endObj=None, 
                        locGrp=None, plane=None, follicleGrp=None):
        '''
        Finalize the ribbon rig setup. Organize the nodes and constrain to objects
        
        name -- Name to be used for naming the top node.
        startObj -- Object to constrain btm pos locator to.
        endObj -- Object to constrain top pos locator to.
        topLocs -- Btm, Mid, Top pos locators for the ribbon setup.
        plane -- Plane used for rbbn setup
        follicleGrp -- Group with follicles / bind jnts in it
        '''
        if self.logger:
            self.logger.info('_setupHeirarchy(): Starting...')         
        
        topGrp = cmds.group(plane, follicleGrp, locGrp, n=name+'_rbbnTopNode')
        children = cmds.listRelatives(locGrp,children=True)
        top = None
        btm = None
        for each in children:
            if 'topLoc_pos' in each:
                top = each
            if 'btmLoc_pos' in each:
                btm = each
        cmds.parentConstraint(startObj, btm, mo=True)
        cmds.parentConstraint(endObj, top, mo=True)

        if self.logger:
            self.logger.info('_setupHeirarchy(): End.') 
            
        return topGrp
    
    def _angleBetween(self, v1, v2):
        ''' Return angular diff of the two vectors in degrees. '''
        if self.logger:
            self.logger.info('_angleBetween(): Starting...')  
            
        v1_mag = math.sqrt( (v1[0]**2)+(v1[1]**2)+(v1[2]**2) )
        v2_mag = math.sqrt( (v2[0]**2)+(v2[1]**2)+(v2[2]**2) )
        
        dot = (v1[0]*v2[0]) + (v1[1]*v2[1]) + (v1[2]*v2[2])
        
        if self.logger:
            self.logger.info('_angleBetween(): End.')         
        
        return math.acos(dot/(v1_mag*v2_mag)) * 57.296
    
    def _zeroNode(self,node):
        ''' Group node, zero node attrs by flushing to group.'''
        if self.logger:
            self.logger.info('_zeroNode(): Starting...')         

        if not isinstance(node, pm.PyNode):
            obj = pm.select(node)
        else:
            obj = node
            
        grp = pm.group(em=True,n=obj.name()+'_zero_grp')
        pm.parent(obj,grp)
        grp.centerPivots()
        
        grp.t.set(obj.t.get())
        grp.r.set(obj.r.get())
        grp.s.set(obj.s.get())
        
        obj.t.set(0,0,0)
        obj.r.set(0,0,0)
        obj.s.set(0,0,0)

        if self.logger:
            self.logger.info('_zeroNode(): End.') 
    
    def _lockAndHide(self, node, attrs=['t','r','s'], lock=True):
        ''' Lock and hide.'''
        if self.logger:
            self.logger.info('_lockAndHide(): Starting...')         

        if not isinstance(node, pm.PyNode):
            obj = pm.select(node)
        else:
            obj = node
        
        if 't' in attrs:
            for attr in ['tx','ty','tz']:
                obj.attr(attr).setLocked(lock)
                
        if 'r' in attrs:
            for attr in ['rx','ry','rz']:
                obj.attr(attr).setLocked(lock)

        if 's' in attrs:
            for attr in ['sx','sy','sz']:
                obj.attr(attr).setLocked(lock)
                
        if self.logger:
            self.logger.info('_lockAndHide(): End.')    
        