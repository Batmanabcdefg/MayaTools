import pymel.core as pm
import logging
import Names
reload( Names )

'''
- Create Character Node with message attributes that represent all possible rig controls
- Register a control to a Character Node: Connect a control to it's cooresponding message attribute.
'''

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

#--- Character Node Names 
nodeNames = {'body':'BodyCharacterNode',
             'head':'HeadCharacterNode'}

#--- Exceptions
invalidParameters = Exception('Invalid parameters passed in by caller.')
invalidName = Exception('Invalid name passed in by caller.')

def register(control=None, name=None, typ=None):
    ''' Connect a control to a message attribute on a Character Node '''
    pymelLogger.debug('Starting: register()...')
    
    # Input validation
    if name not in Names.controls_head: 
        if name not in Names.controls_body: 
            if name not in Names.controls_neck: 
                if name not in Names.controls_face:
                    raise Exception('%s : Invalid control name.'%name)
    if not control or not name or not typ: raise invalidParameters
    
    if typ == 'body':
        if not pm.objExists(nodeNames['body']):
            createNode(typ='body')
        connectControl(typ='body',control=control,name=name)
        
    if typ == 'head':
        if not pm.objExists(nodeNames['head']):
            createNode(typ='head')
        connectControl(typ='head',control=control,name=name)
        
    pymelLogger.debug('End: register()...')
    
def createNode(typ=None):
    ''' Create Character Node with message attributes named after controls. '''
    pymelLogger.debug('Starting: createNode()...')
    
    # Input validation
    if not typ: raise invalidParameters
    if typ not in nodeNames.keys(): raise invalidParameters
    
    if typ == 'head':
        node = pm.group( name=nodeNames['head'], em=True )
        for name in Names.controls_head:
            pm.addAttr( node, longName=name, attributeType='message' )
        for name in Names.controls_neck:
            pm.addAttr( node, longName=name, attributeType='message' )
        for name in Names.controls_face:
            pm.addAttr( node, longName=name, attributeType='message' )
        
            
    if typ == 'body':
        node = pm.group( name=nodeNames['body'], em=True )
        for name in Names.controls_body:
            pm.addAttr( node, longName=name, attributeType='message' )
        
    pymelLogger.debug('End: createNode()...')

def connectControl(typ=None, control=None, name=None):
    ''' Connect control to name attribute on Character node '''
    if not control or not name or not typ: raise invalidParameters
    
    if typ == 'head':
        pm.connectAttr('%s.message'%control, '%s.%s'%(nodeNames['head'],name), f=1)
        
    if typ == 'body':
        pm.connectAttr('%s.message'%control, '%s.%s'%(nodeNames['body'],name), f=1)