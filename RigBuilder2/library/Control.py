import pymel.core as pm
import logging
import os

import Names
reload( Names )
import RegisterControl
reload(RegisterControl)
import Switch
reload(Switch)

#--- Add cwd and lib
#rootd = os.path.abspath(os.path.abspath(__file__),'..')
rootd = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))
#templates = rootd + '/templates/controls'
templates = rootd + '/controls/'

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

#--- Exceptions
invalidFile = Exception('Curve File Could not be found.')

def create( name=None, offsets=2, shape=None,
            size=None, color=None, switch=None,
            pos=None, parent=None, typ=None,
            rot=None):
    '''
    name: String: Control name. Ex: "LeftUpLeg_ctrl"
    offsets: Int: Number of offset groups
    shape: String: Name of control curve .ma file. Ex: 'arrow_01'
    size: [x,y,z]: Scale for control
    color: Int: Index of color in Names.controls_color.
    pos: [x,y,z]: Final translational offset added to top group of control
    parent: String: Name of parent object for control
    typ: String: Control type: "body", "head"
    switch: [ [objects], [names], type ]: objects: List of objects to constrain to, names: Name of weight switching attributes, title: "space" or "orient"
    '''
    
    pymelLogger.debug('Starting: create()...')
    
    # Import
    crv = importCurve( shape )
    if not crv: return False
    
    # rename (verify name?)
    crv.rename(name)
    
    # Color
    try: cID = Names.controls_color[color]
    except: cID = 17 # yellow
    crv.setAttr('overrideEnabled', 1)
    crv.setAttr('overrideColor', cID)
  
    # Position, Group, Parent # pos = [x,y,z]
    grpList = []
    if offsets:
        
        index = 0
        for offsetName in Names.offset_names:
            if index == offsets:
                continue
            grp = pm.group(em=1, name=crv.name() + '_' + offsetName)
            grpList.append(grp)
            index += 1
            
        # parent groups
        grpList.reverse()
        last = ''
        for element in grpList:
            if last:
                last.setParent(element)
            last = element
            
        # position top grp null
        #if pos:
        #    last.setTranslation(pos)
            
        # parent curve to last grp
        crv.setParent( grpList[0] )
    
    # Parent
    if parent:
        pm.delete( pm.parentConstraint(parent,grpList[-1]))
        pm.parent(grpList[-1],parent)
    
    # pos = [x,y,z]
    if pos:
        if not len(grpList) == 0: grpList[-1].setTranslation(pos,space='world')
        else: crv.setTranslation(pos,space='world')  
        
    if rot:
        if not len(grpList) == 0: grpList[-1].setRotation(rot,space='world')
        else: crv.setRotation(rot,space='world') 

    if size:
        if not isinstance(size, list):
            size = [size,size,size]
        if not len(grpList) == 0: grpList[-1].setScale(size)
        else: crv.setScale(size)
            
    # Register
    RegisterControl.register(control=crv, name=name, typ=typ)
    
    # Switch
    if switch:
        if offsets < 2:
            raise Exception("Need to use at least two offsets to use space switching.")
        Switch.create( control=crv, constObj=grpList[-2], objects=switch[0], names=switch[1], typ=switch[2] )
    
    pymelLogger.debug('End: create()...')
    
    if len(grpList) == 0: return crv
    else: return grpList[-1]
    
def importCurve(crvName):
    ''' Import curve '''
    pymelLogger.debug('Starting: importCurve()...')
    
    # checkfile exists
    # import file into scene
    path = templates + crvName + '.ma'
    if os.path.exists( path ): 
        pm.importFile( path ) 
        # return crv pm obj
        crv = pm.ls(crvName,r=1)[0]
        pymelLogger.debug('End: importCurve()...')
        return crv
    else: return invalidFile
        
    

    
    