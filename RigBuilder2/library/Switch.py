import logging
import pymel.core as pm

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

#--- Exceptions
invalidParameters = Exception('Invalid parameters passed in by caller.')
invalidName = Exception('Invalid name passed in by caller.')

def create( control=None, constObj=None, objects=None, names=None, typ='Space' ):
    ''' 
    Create a space switch on given control.
    Method: Attributes drive weight values of a parent or orient constraint.
    
    Example:
    
    import Switch as s
    reload( s )
    
    constObj = 'leftArmIk_offC'
    control='leftArmIk_ctrl'
    objects = ['head_ctrl','hip_ctrl','main_ctrl','world_ctrl']
    names = ['head','hip','main','world']
    
    s.create( control=control, constObj=constObj, objects=objects, names=names, typ='space' )
    '''
    pymelLogger.debug('Starting: create()...')
    
    if not control or not constObj or not objects or not names or not typ: 
        raise invalidParameters
    if typ not in ['space','orient']:
        raise Exception('Invalid type specified by caller')
    
    # Create title attribute on control
    pm.select( control, r=True )
    pm.addAttr( longName=typ, k=True )
    pm.setAttr( control + '.' + typ, lock=True )
    
    if typ == 'space':
        const = pm.parentConstraint( objects, constObj, mo=True )
    if typ == 'orient':
        const = pm.orientConstraint( objects, constObj, mo=True )        

    index = 0
    for obj,name in zip(objects,names):
        # make attribute
        pm.addAttr(control,longName=name,k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        # make direct connection
        pm.connectAttr( control + '.' + name, const + '.' + obj + 'W%s'%index )
        index += 1
    pymelLogger.debug('Created %s switch on %s.'%(typ,control))
    pymelLogger.debug('End: create()...')

        