import sys
import logging
import pymel.core as pm

class jointsOnCurve(object):
    '''
    Description:
    Given selected joints, run.
    Joints will be attached to curve at positions on curve nearest their original position.
    
    returns: PyNode('curve')
    '''
    def __init__(self, **keywords):
        '''
        Initialize logging
        '''
        #--- Determine how much feedback in log file
        if keywords.has_key('v'):
            self.verbosity = keywords['v']
        else:
            # Default. Higher verbosity reveals more info in log file. 1 - 5
            self.verbosity = 1

        #--- Setup logging
        logging.basicConfig( filename='jointsOnCurve.log', filemode='w',
                             format= '%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                             datefmt='%m/%d/%Y %I:%M:%S %p' )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.verbosity * 10)

    def attachJointsToCurve(self, *args):
        ''' Get selection, attach joints to curve at locator positions '''
        sel = pm.ls(sl=True)

        joints = [x for x in sel if x.type() == 'joint']

        # Create curve
        positions = []
        for jnt in joints:
            positions.append(pm.xform(jnt,q=1,ws=1,t=1))

        curve = pm.curve(p=positions,d=1,n='%s_curve'%joints[0].name())      
        curveShape = curve.getShape()
        prnt = pm.listRelatives( joints[0], parent=True )
        if prnt:
            pm.parent(curve, prnt)

        if not len(joints) or not curve:
            raise Exception('Must have joints selected.')
        
        for jnt in joints:
            # Get paramU value based on current jnt position. 
            
            cpos = pm.shadingNode('closestPointOnCurve', asUtility=True)
            pm.connectAttr('%s.ws'%curveShape,'%s.inCurve'%cpos,f=1)
            pm.connectAttr('%s.translate'%jnt.name(),'%s.inPosition'%cpos,f=1)
            
            paramU = pm.getAttr(cpos.paramU)
            pm.delete(cpos)

            # Attach to curve
            poci = pm.createNode('pointOnCurveInfo',n='%s_pocinfo_node'%jnt.name())
            pm.connectAttr('%s.ws'%curveShape,'%s.inputCurve'%poci,f=1) 
            pm.connectAttr('%s.position'%poci,'%s.translate'%jnt,f=1)
            pm.setAttr('%s.parameter'%poci,paramU)
            
        return curve

if __name__ == '__main__':
    x = jointsOnCurve()
    x.attachJointsToCurve()
