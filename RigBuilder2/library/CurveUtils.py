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
rootd = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))
curvesFolder = rootd + '/curves/'

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

#--- Exceptions
invalidFile = Exception('Curve File Could not be found.')

def _importFile():
        ''' Import a maya scene into the current scene using UI dialog'''
        try:
            pm.importFile( pm.fileDialog() )
        except Exception,e:
            raise Exception(e)

def importCrvs():
    pymelLogger.debug('Starting: importCrvs()...') 
    
    _importFile()
    _applyCurves()
    
    pymelLogger.debug('End: importCrvs()...') 

def mirrorCurves(side=None, mirrorPlane='YZ'):

    pymelLogger.debug('Starting: mirrorCurves()...') 
    
    if not side: side = Names.prefixes['left']

    if side == Names.prefixes['left']: 
        mSign = 0
        newSide = Names.prefixes['right']
    else: 
        side == Names.prefixes['right']
        mSign = 1
        newSide = Names.prefixes['left']
    
    if mirrorPlane == 'YZ': axis = 'X'
    elif mirrorPlane == 'XY': axis = 'Z'
    elif mirrorPlane == 'XZ': axis = 'Y'
    else : raise 'Incorrect Mirroring Plane'
    
    ctrlList = _getCharNodeCurves()
    
    
    
    if mSign == 0: scale = [-1,1,1]
    else: scale=[1,1,1]
    #mirrorList = []
    for ctrl in ctrlList:
        if side in str(ctrl):
            
            otherSideCtrl = ctrl.replace( side , newSide )

            crvsMirrorGrp = pm.group(em=1, name='curvesMirror')

            newCnt = ctrl.duplicate()[0]
            
            if len( newCnt.getChildren() ) > 1:
                shapeNode = newCnt.getShape()
                print shapeNode, newCnt.getChildren()
                for child in newCnt.getChildren():
                    if child != shapeNode:
                        pm.delete(child) 
                        
            newCnt.setParent(crvsMirrorGrp)
            newCnt.rename(name=str(otherSideCtrl)+'_mirror')
            crvsMirrorGrp.setScale( scale )

            newCrvShape = newCnt.getShape()
            print newCrvShape
 
            # get cv position before parenting it 
            cvPos = []
            index = 0
            while index < newCrvShape.numCVs():
                cvPos.append( pm.xform( newCrvShape+'.cv['+ str(index) +']', q=1, ws=1,t=1 ) )
                index = index + 1

            # get old shape of transform if it exists and delete it 
            otherSideCtrl = pm.ls(otherSideCtrl)[0]
            print otherSideCtrl.getChildren()
            ctrlShapeNode = otherSideCtrl.getShape()
            pm.delete(ctrlShapeNode)
            
            newShapeName = newCrvShape.setParent( otherSideCtrl, shape=True, add=True ) 
        
            pm.delete( newCnt )
            pm.delete( crvsMirrorGrp )
            
            # rename new curve without _mirror
            finalName = newShapeName.name()[:newShapeName.name().find('_mirror')]
            newShapeName.rename( finalName+'Shape' )
            
            
            
            # position cvs in the right place
            index = 0
            while index < newShapeName.numCVs():
                pm.xform( newShapeName + '.cv['+ str(index) +']', ws=1,t=cvPos[index] )
                index = index + 1
            
            
            
         
    
  
        
    pymelLogger.debug('End: mirrorCurves()...') 
    

def _applyCurves():
    pymelLogger.debug('Starting: _applyCurves()...') 
    
    ctrlList = _getCharNodeCurves()
    
    crvExportGrp = pm.ls('curvesExport')[0]
    
    for crv in crvExportGrp.getChildren():
        if crv[:crv.rfind('_export')] in ctrlList:
            
            newCrvShape = crv.getShape()
            finalName = crv[:crv.rfind('_export')]
            
            oldCrvTrans = pm.ls( crv[:crv.rfind('_export')] )[0]
            oldCrvShape = oldCrvTrans.getShape() 
        
            paCrv = newCrvShape.setParent( oldCrvTrans,shape=True, add=True ) 
            pm.delete( oldCrvShape )
            # delete export from the new name
            paCrv.rename( finalName+'Shape' )
    
    pm.delete(crvExportGrp)
    pymelLogger.debug('End: _applyCurves()...')
    

def exportCrvs():
    pymelLogger.debug('Starting: exportCrvs()...') 
    
    ctrlList = _getCharNodeCurves()
    _extractCurves( ctrlList )
    _exportCurvesFile()
    
    pymelLogger.debug('End: exportCrvs()...') 
        
def _getCharNodeCurves():
    
    pymelLogger.debug('Starting: getCharNodeCurves()...') 
    # get characterNodes Curves
    charNodes = pm.ls(Names.character_nodes)
    controlList = []
    for cn in charNodes:
        cnAttrs = cn.listAttr(ud=1) # listing only user defined attrs
        for attr in cnAttrs:
            attrCon = attr.listConnections()
            if attrCon:
                controlList.append(attrCon[0])
    
    pymelLogger.debug('End: getCharNodeCurves()...') 
    return controlList

def _extractCurves( controlList ):
    
    pymelLogger.debug('Starting: _extractCurves()...') 
    # create grp to place curves
    crvsExpGrp = pm.group(em=1, name='curvesExport')
    for cnt in controlList:
        nameori = cnt.name()
        newCnt = cnt.duplicate()[0]
        if len( newCnt.getChildren() ) > 1:
            for child in newCnt.getChildren():
                if not child == newCnt.getShape():
                    pm.delete(child)
        newCnt.setParent(crvsExpGrp)
        newCnt.rename(name=nameori+'_export')
    pymelLogger.debug('End: _extractCurves()...') 

def _exportCurvesFile():
    
    pymelLogger.debug('Starting: _exportCurvesFile()...') 
    result = pm.promptDialog(title='Curves Files Name',message='Enter Name:',button=['OK', 'Cancel'],
                                defaultButton='OK',cancelButton='Cancel',dismissString='Cancel')
    if result == 'OK': fileName = pm.promptDialog(query=True, text=True)
    else: raise 'Curves not exported because No name was passed'             
    
    if os.path.exists(curvesFolder):
        pm.select('curvesExport', r=1)
        pm.exportSelected(curvesFolder + fileName, type='mayaAscii', f=1)
        pm.delete('curvesExport')
    else: raise 'Path to curves folder does no exist!'
    pymelLogger.debug('Starting: _exportCurvesFile()...') 

    
    