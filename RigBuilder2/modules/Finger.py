import pymel.core as pm
import logging
import os
import sys


#--- Add cwd and lib
cwd = os.path.dirname(os.path.abspath(__file__))
lib = cwd.replace('modules','library')
if cwd not in sys.path:
    sys.path.append(cwd)
if lib not in sys.path:
    sys.path.append(lib)
    
import Names
reload( Names )
import Control
reload(Control)

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

    
"""
Description: 
    Given:
        Controller
        start + end joint for each finger
        Names for each finger
        
        Create attributes to drive the fingers on the controller, and FK controls
        on the finger joints.
    
Additional Notes: 

Example call:
lib = "/Users/msantos/Documents/repos/artpipeline/maya/RigBuilder/modules"
if lib not in sys.path:
    sys.path.append(lib)
    
import Finger
reload( Finger )

Finger.build(label="Finger",
                control='nurbsCircle1',
                attNames=['index','middle'],
                startJnts=['joint1','joint5'],
                endJnts=['joint4','joint9'])
             
Requires:

Development notes:

    @todo - Curl all, spread
    
"""

def build( side=None, label='Fingers',control=None, parentJnt=None,
          curl='Z',twist='X',spread='Y',
          fkNormal=(1.0, 0.0, 0.0), radius=0.3):


    pymelLogger.debug('Starting: build()...') 
    
    if side == None: raise Exception('Make sure side: %s is valid '%side) 
    if side == Names.prefixes['left']: fingerJnts = Names.joints_leftFingers_list
    elif side == Names.prefixes['right']: fingerJnts = Names.joints_rightFingers_list
    else: raise Exception('Make sure side: %s is valid '%side)
    

    # Is the last joint of the chain going to be skinned ? hasEndJnt = 0
    # or last joint should not be considered ? hasEndJnt = 1
    hasEndJnt = 1 # hard coding it, by default last joint will not be considered
    
    rList = createJnts( side, fingerJnts, hasEndJnt ) # [ startJnts, endJnts, attNames, newJnts, originalJnts ]
    startJnts = rList[0]
    endJnts = rList[1]
    attNames = rList[2]
    newJnts = rList[3]
    originalJnts = rList[4]

    # Create main attributes on control
    pm.select(control,r=True)
    attList = pm.attributeInfo(control,all=True)

    if(label not in attList):
        try:
            pm.addAttr(longName=label,k=True)
            pm.setAttr(control + '.' + label, lock=True)
        except:
            pass #Attribute already exists @ todo - Catch specific exemption
        
    # Create controller vis switch
    pm.addAttr(longName='Control_Vis',k=True, min=0, max=1,dv=1)
    
    # Create spread all
    pm.addAttr(longName='spread_all',k=True, min=-10.0, max=10.0)
    
    # Create tenson all
    pm.addAttr(longName='tension_all',k=True, min=0.0, max=10.0)
    
    # Create tenson all
    pm.addAttr(longName='curl_all',k=True)

    chainParent = ''
    
    offsetGrpsLists = []
    
    ######################################################## 
    ######################################################## 
    ######################################################## 
    # spread hard coded calculation #
    jntLen = len(startJnts)
    startValue=-50
    endValue=50
    range = -(startValue) + endValue
    increment = range / jntLen
    startV = startValue
    endV = endValue
    
    spreadList=[]
    if jntLen%2==0:
        centerIndex = jntLen/2
        index=1
        while index < jntLen+1:
            if index < centerIndex:
                spreadList.append( [startV,endV] )
                startV = startV + increment
                endV = endV - increment
            if index > centerIndex:
                spreadList.append( [startV,endV] )
                startV = startV + increment
                endV = endV - increment
            index = index + 1
    else:
        centerIndex = (jntLen+1)/2
        index=1
        while index < jntLen+1:
            if index < centerIndex:
                spreadList.append( [startV,endV] )
                startV = startV + increment
                endV = endV - increment
            if index == centerIndex:
                spreadList.append([0,0])
                startV = 0 + increment
                endV = 0 - increment
            if index > centerIndex:
                spreadList.append( [startV,endV] )
                startV = startV + increment
                endV = endV - increment
            index = index + 1
    ########################################################           
    ######################################################## 
    ########################################################  
     
     
    print 'spread list ', spreadList
    # Iterate the attNames, startJnts, endJnts at the same time.
    for (name,startJnt,endJnt,spr) in zip(attNames,startJnts,endJnts,spreadList):
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
    
        #Store parent of chain if it has one
        try:
            chainParent = pm.listRelatives(chain[0],parent=True)
        except:
            pass
 
        
            
        offsetGrps = ['_crv_jnt','_cntrl_jnt','_tension_jnt','_curl_jnt','_all_jnt','offsetGrp']
        offsetGrpList = []
        
        for joint in chain:
            # create offset groups for finger controls
            ctrlName = joint.replace( '_' + Names.suffixes['fk'], '_' + Names.suffixes['control'] )
            ctrlPos = pm.xform(joint, query = True, translation = True, ws=1)
            ctrlRot = pm.xform(joint, query = True, ro = True, ws=1)
           
            offsetGrp = Control.create( name=ctrlName, offsets=len(offsetGrps), shape='circle_01', 
                            size=radius, color=getSideColor(side), 
                            pos=ctrlPos, parent=None,rot=ctrlRot, typ='body' ) 
            
            offsetGrpList.append(offsetGrp)
            
            # parent contraint ctrl to fk jnt
            pm.parentConstraint( offsetGrp.listRelatives(ad=1)[0].getParent(), joint, mo=True )
            
            
            # set Control_Vis attr!!!
            
            pm.connectAttr(control +'.'+ 'Control_Vis', offsetGrp.listRelatives(ad=1)[0].getParent() + '.visibility') 
            
 
        
        ### hard coding it for now! until better solution and more time
        cntrlJoints = [] 
        curlJoints = [] 
        tensionJoints = [] 
        allJoints = [] 
        
       
        for off in offsetGrpList:   
            for elem in off.listRelatives(ad=1):
                if '_offsetE' in str(elem): cntrlJoints.append(elem)
                elif '_offsetB' in str(elem): allJoints.append(elem)
                elif '_offsetD' in str(elem): curlJoints.append(elem)
                elif '_offsetC' in str(elem): tensionJoints.append(elem)
                
                
                
                

        print cntrlJoints
        print curlJoints
        print tensionJoints
        print allJoints

        
        offsetGrpList.reverse()
        index = 0
        for grp in offsetGrpList:
            if index+1 == len(offsetGrpList): break
            grp.setParent(offsetGrpList[index+1].listRelatives(ad=1)[0].getParent())
            index = index + 1
            
        offsetGrpList.reverse() 
        offsetGrpsLists.append( offsetGrpList )
        
       
         
         
            
        # Adding Curl attrs on controller
        x= 0 
        while x < len(chain):
            pm.addAttr(control, longName=name + '_curl_' + str(x+1),k=True)
            x = x + 1
    
        # Adding spread attr on controller
        pm.addAttr(control, longName=name + '_spread',k=True)
    
        # Twist
        pm.addAttr(control, longName= name + '_twist',k=True)
        
        # Tension
        pm.addAttr(control, longName= name + '_tension',k=True)
    
        
        
        
        
        
        
        # Connect attributes to cntrlJoints rotate's ( aim = curl, up = spread )
        x = 0
        pm.connectAttr( control + '.' + name + '_twist' , str(cntrlJoints[0]) + '.rotate' + twist ) 
        pm.connectAttr( control + '.' + name + '_spread', str(cntrlJoints[0]) + '.rotate' + spread )
        
        while x < len(chain):
            pm.connectAttr( control + '.' + name + '_curl_' + str(x+1) , str(cntrlJoints[x]) + '.rotate' + curl )
            x = x + 1
            
        #SDK attributes to curl All
        x = 0
        while x < len(curlJoints):
            pm.connectAttr( control + '.curl_all', str(curlJoints[x]) + '.rotate' + curl )
            x = x + 1
 
        
        #SDK attributes to tensionJoints rotate's ( aim = curl )
        x = 0
        while x < len(tensionJoints):
            # Root joint curls back
            if x == 0:
                pm.setDrivenKeyframe( tensionJoints[x], 
                                cd=control + '.' + name + '_tension',
                                at= "rotate%s"%curl,
                                dv = 0,
                                v = 0 )
                pm.setDrivenKeyframe( tensionJoints[x], 
                                cd=control + '.' + name + '_tension',
                                at= "rotate%s"%curl,
                                dv = 10,
                                v = 60 )
                x += 1
                continue
            
            # All oher joints curl forword
            pm.setDrivenKeyframe( tensionJoints[x], 
                            cd=control + '.' + name + '_tension',
                            at= "rotate%s"%curl,
                            dv = 0,
                            v = 0 )
            pm.setDrivenKeyframe( tensionJoints[x], 
                            cd=control + '.' + name + '_tension',
                            at= "rotate%s"%curl,
                            dv = 10,
                            v = -50 )
                
            x = x + 1
        
        # SDK All tension
        x = 0
        while x < len(allJoints):
            # all_tension
            if x == 0:
                pm.setDrivenKeyframe( allJoints[x], 
                                cd=control + '.tension_all',
                                at= "rotate%s"%curl,
                                dv = 0,
                                v = 0 )
                pm.setDrivenKeyframe( allJoints[x], 
                                cd=control + '.tension_all',
                                at= "rotate%s"%curl,
                                dv = 10,
                                v = 60 )
                x += 1
                continue
            
            # All other joints curl forward
            pm.setDrivenKeyframe( allJoints[x], 
                            cd=control + '.tension_all',
                            at= "rotate%s"%curl,
                            dv = 0,
                            v = 0 )
            pm.setDrivenKeyframe( allJoints[x], 
                            cd=control + '.tension_all',
                            at= "rotate%s"%curl,
                            dv = 10,
                            v = -50 )
            x += 1
        
        
        
        # SDK All spread
        #pm.connectAttr( control + '.spread_all', str(allJoints[0]) + '.rotate' + spread )
        
        x = 0
        while x < len(allJoints):
            # spread_all
            if x == 0:
                pm.setDrivenKeyframe( allJoints[x], 
                                cd=control + '.spread_all',
                                at= "rotate%s"%spread,
                                dv = -10,
                                v = spr[0] )
                pm.setDrivenKeyframe( allJoints[x], 
                                cd=control + '.spread_all',
                                at= "rotate%s"%spread,
                                dv = 10,
                                v = spr[1] )
                x += 1
                continue
            """
            # All other joints curl forward
            pm.setDrivenKeyframe( allJoints[x], 
                            cd=control + '.spread_all',
                            at= "rotate%s"%spread,
                            dv = 0,
                            v = 0 )
            pm.setDrivenKeyframe( allJoints[x], 
                            cd=control + '.spread_all',
                            at= "rotate%s"%spread,
                            dv = 10,
                            v = 50 )
            """
            x += 1 
             
         
        
        
        
        
        
        
        
        
        
        pm.select(clear=True) 
        
    _connectToSH( newJnts, originalJnts )
    
    # connecting to hand jnt if passed
    if parentJnt:
        _connectToHandJnt( parentJnt, newJnts, offsetGrpsLists)
    
    pymelLogger.debug('End: build()...')


def getSideColor(side=None):
    
    if side == Names.prefixes['left']: crv_color='red'
    elif side == Names.prefixes['right']: crv_color='midBlue'
    else: crv_color='white'
    return crv_color        
    
def createJnts( side=None, fingerJnts=None, hasEndJnt=None):
   
    pymelLogger.debug('Starting: createJnts()...') 

    startJnts = []
    endJnts = []
    attNames = []
    
    originalJnts = []
    newJnts = []
    
    for jnt in fingerJnts:
        # if jnt exists on the scene save it on list otherwise continue searching
        if pm.objExists( jnt[0] ):
            topJnt = pm.ls(jnt[0],r=1)[0]
            newJntChain = pm.duplicate(topJnt,rr=True,po=False, name= topJnt + '_' + Names.suffixes['fk'] )[0]
            newJntChain.setParent(world=1)
            
            startJnts.append( newJntChain )
            
            # getting name for attr "index, thumb ..."
            noSuf = newJntChain.split('_' + Names.suffixes['fk'])[0]
            endPart = noSuf[noSuf.rfind(side + Names.joints_hf[0]):]  # if more than 9 jnts,  it will break!!!!!
            endPre = len( side + Names.joints_hf[0] )
            attNames.append( endPart[endPre: -1 ].replace('|','') )
            
            newChildJnts = newJntChain.listRelatives(ad=1)
            end = newChildJnts[0]

            
            # rename all the new jnts!
            for nJnt in newChildJnts:
                nJnt.rename(nJnt+'_'+Names.suffixes['fk'])
                
            newChildJnts.append( newJntChain )
            newJnts.append(newChildJnts)
            
            
            oldChildJnts = topJnt.listRelatives(ad=1)
            oldChildJnts.append( topJnt )
            originalJnts.append(oldChildJnts)


            # if no child will break!!!!
            if hasEndJnt == 1:endJnts.append( end.getParent() )
            else: endJnts.append( end )
           
        else: continue
    
    newJnts.reverse()
    originalJnts.reverse()
        
    rList = [ startJnts, endJnts, attNames, newJnts, originalJnts ]
    pymelLogger.debug('End: createJnts()...') 
    return rList


def _connectToSH( newJnts, originalJnts  ):
    
    pymelLogger.debug('Starting: connectToSH()...')
    for nJnts, oriJnts in zip(newJnts,originalJnts):
        for jntS,jntT in zip(nJnts, oriJnts):
            try: pm.parentConstraint( jntS, jntT, mo=1 )
            except: print 'Could not constraint: ' + jntS,jntT
        
    pymelLogger.debug('End: connectToSH()...')

def _connectToHandJnt( handJnt, newJnts, offsetGrps ): 
    
    pymelLogger.debug('Starting: _connectToHandJnt()...')

    print offsetGrps
    for nJnts,oGrps in zip(newJnts,offsetGrps):
        nJnts[-1].setParent( handJnt )
        oGrps[0].setParent( handJnt )
    
 
        
    # for now we will be parentconstraining sh jnt to handjnt
    # later on it should be attached to the follow 
    handJntSH = handJnt[:handJnt.rfind('_'+Names.suffixes['attach'])]
    pm.parentConstraint( handJntSH, handJnt, mo=1 )
    
        
   
    pymelLogger.debug('End: _connectToHandJnt()...')