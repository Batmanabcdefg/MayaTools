import pymel.core as pm
import pymel.core.datatypes as dt
from pymel.internal.plogging import pymelLogger

class ms_jointsOnNurbsPlane(object):
    '''
    Given n input locators and num joints:
    - Create ribbon along locators with num joints parented to follicles on ribbon
    '''
    def __init__(self):
        _name = '__init__'
        pymelLogger.info('Started: %s' % _name)
        self.ui()
        pymelLogger.info('Ended: %s' % _name)  
    
    def ui(self):
        '''
        Create UI
        '''
        _name = 'ui'
        pymelLogger.info('Started: %s' % _name)
        
        winName = 'ms_jointsOnNurbsPlaneWin'
        if(pm.window(winName, exists=True)):
            pm.deleteUI(winName, window=True)
        win = pm.window(winName)
        
        with pm.formLayout() as form:
            self.nameFld = pm.textFieldGrp(l='Name')
            self.numFld = pm.intFieldGrp(l='Joints (3-50)', v1=3)
            self.radFld = pm.floatFieldGrp(l='Radius (0.01 - 10)', v1=0.5, pre=2)
            self.buildFld = pm.radioButtonGrp(l='Plane Curve Duplicate', labelArray3=['x', 'y', 'z'], nrb=3, sl=3)
            pm.text('Select objects to create plane along, then press "Build"')
            pm.button(l='>> Build <<', c=self.build)
            
        form.redistribute()
        
        pm.showWindow()
        pymelLogger.info('Ended: %s' % _name)
        
    def build(self, *args):
        '''
        Call methods to build the joints on nurbs plane setup
        '''
        _name = 'build'
        pymelLogger.info('Started: %s' % _name)
        
        # Validate user input
        name = pm.textFieldGrp(self.nameFld, q=1, text=1)
        num = pm.intFieldGrp(self.numFld, q=1, v=1)[0]
        rad = pm.floatFieldGrp(self.radFld, q=1, v=1)[0]
        axis = pm.radioButtonGrp(self.buildFld, q=1, sl=1)
        objs = pm.ls(sl=1)
        
        if not name:
            pymelLogger.error('No name entered by user. Must enter a name. Exiting.')
            return            
        if num < 1 or num > 50:
            pymelLogger.error('%s is an invalid value for number of joints. Must be between 3 - 50. Exiting.' % num)
            return    
        if rad < 0.009 or rad > 10:
            pymelLogger.error('%s is an invalid value for joint radius. Must be between 0.01 - 10. Exiting.' % rad)
            return    
        if not objs:
            pymelLogger.error('No objects selected. Must select objects to build curve along. Exiting.')
            return

        # Call build methods
        crv1, crv2 = self._createCurves(objs=objs, axis=axis, num=num)
        plane = self._createPlane(name=name, crv1=crv1, crv2=crv2)
        follicles = self._createFollicles(name=name, plane=plane, num=num)
        self._createJoints(name=name, follicles=follicles, rad=rad)
        
        pm.delete(crv1, crv2)

        pymelLogger.info('Ended: %s' % _name)
        pymelLogger.info('Build successful!')
        
    def _createJoints(self, name=None, follicles=None, rad=None):
        '''
        Create a joint parented to each follicle
        '''
        _name = '_createJoints'
        pymelLogger.info('Started: %s' % _name)        
        
        count = 1
        for f in follicles:
            j = pm.joint(name='%s_jnt_%s' % (name, count), rad=rad)
            pm.parent(j, f)
            j.setTranslation(0)
            count += 1
            
        pymelLogger.info('Ended: %s' % _name) 
            
    def _createPlane(self, name=None, crv1=None, crv2=None):
        '''
        Plane made by lofting two curves
        '''
        _name = '_createPlane'
        pymelLogger.info('Started: %s' % _name)
        
        plane = pm.loft( crv1, crv2, ch=False, rn=True)[0]
        plane.rename('%s_plane' % name)
        
        pymelLogger.info('Ended: %s' % _name)        
        return plane
    
    def _createFollicles(self, name=None, plane=None, num=None):
        '''
        Create num follicles evenly spaced along nurbs plane
        '''
        _name = '_createFollicles'
        pymelLogger.info('Started: %s' % _name) 
        
        #--- Create the follicles
        pm.select(clear=True)
        follicles = []
        for i in range(0, num):
            follicles.append( self._create_follicle( obj=plane, name=name, count=i+1, uPos=0.5, vPos=i/(num-1.00)) )
            
        grp = pm.group(n=name+'_rbbnFollicles_grp', em=True)
        for each in follicles:
            pm.parent(pm.listRelatives(each, parent=True)[0], grp)

        pymelLogger.info('Ended: %s' % _name)        
        return follicles    
    
    def _create_follicle(self, obj, name, count=1, uPos=0.0, vPos=0.0):
        ''' 
        Manually place and connect a follicle onto a nurbs surface. 
        '''
        shape = obj.getShape()
        
        # create a name with frame padding
        fName = '_'.join([name, 'ShapeFollicle', str(count).zfill(2)])
        oFoll = pm.createNode('follicle', name=fName)
        shape.local.connect(oFoll.inputSurface)
        
        p = oFoll.getParent().name()
        tName = '_'.join([name, 'Follicle', str(count).zfill(2)])
        pm.rename(p,tName)
        # if using a polygon mesh, use this line instead.
        # (The polygons will need to have UVs in order to work.)
        #oMesh.outMesh.connect(oFoll.inMesh)
    
        shape.worldMatrix[0] >> oFoll.inputWorldMatrix
        oFoll.outRotate >> oFoll.getParent().rotate
        oFoll.outTranslate >> oFoll.getParent().translate
        oFoll.parameterU.set(uPos)
        oFoll.parameterV.set(vPos)
        oFoll.getParent().t.lock()
        oFoll.getParent().r.lock()
    
        return oFoll
        
    def _createCurves(self, objs=None, axis=None, num=None):
        '''
        Create two curves using .getTranslation() of passed in objects
        '''
        _name = '_createCurves'
        pymelLogger.info('Started: %s' % _name)
        
        positions = []
        for obj in objs:
            loc = pm.spaceLocator()
            pm.parentConstraint(obj, loc, mo=0)
            positions.append(pm.PyNode(loc).getTranslation())
            pm.delete(loc)
        crv1 = pm.PyNode(pm.curve(p=positions, d=1))
        crv2 = pm.PyNode(pm.curve(p=positions, d=1))
        
        move = 0.05
        if axis == 1:
            pm.move(crv1, move, r=1, moveX=1)
            pm.move(crv2, -move, r=1, moveX=1)
        elif axis == 2:
            pm.move(crv1, move, r=1, moveY=1)
            pm.move(crv2, -move, r=1, moveY=1)
        elif axis == 3:
            pm.move(crv1, move, r=1, moveZ=1)
            pm.move(crv2, -move, r=1, moveZ=1)

        pm.rebuildCurve( crv1, rt=0, s=num )
        pm.rebuildCurve( crv2, rt=0, s=num )
    
        pymelLogger.info('Ended: %s' % _name)       
        return crv1, crv2
    
    def _organize(self):
        '''
        Setup hierarchy for setup
        '''
        _name = '_organize'
        pymelLogger.info('Started: %s' % _name)
        
        
        pymelLogger.info('Ended: %s' % _name)