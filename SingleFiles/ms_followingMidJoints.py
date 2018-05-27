from functools import partial
import pymel.core as pm

class ms_followingMidJoints():
    '''
    Given source namespace and target namespace,
    copy all animation from control ns to target ns on all transform nodes.
    '''
    def __init__(self):
        version = "1.0"
        if pm.window( 'ms_followingMidJointsWin', exists=True ):
            pm.deleteUI( 'ms_followingMidJointsWin', window=True )
        self.window = pm.window( 'ms_followingMidJointsWin', title="Following Mid Joints v%s" % version, iconName='ms_followingMidJointsWin' )

        with pm.columnLayout( adj=1 ):
            self.mainLO = pm.columnLayout( adjustableColumn=True )
	    
            self.numFld = pm.textFieldGrp( label='How many mid joints?', text='1' )
	    self.axisFld = pm.optionMenu( label='Up Vector' )
	    pm.menuItem( label='X' )
	    pm.menuItem( label='Y' ) 
	    pm.menuItem( label='Z' ) 
            
            self.aFld = pm.textFieldButtonGrp( label='Joint A', buttonLabel='<<<' )
            pm.textFieldButtonGrp( self.aFld, e=1, bc=partial( self.loadJnt, self.aFld ))
            
            self.bFld = pm.textFieldButtonGrp( label='Joint B', buttonLabel='<<<' )
            pm.textFieldButtonGrp( self.bFld, e=1, bc=partial( self.loadJnt, self.bFld ))
            
            pm.button( l='Create Mid Joints', c=self.create )
            
        pm.showWindow( self.window )
	
    def create(self, *args):
	a = pm.PyNode(pm.textFieldButtonGrp(self.aFld, q=1, text=1))
	b = pm.PyNode(pm.textFieldButtonGrp(self.bFld, q=1, text=1))
	name = a+'midJnt'
	num = pm.textFieldGrp(self.numFld, q=1, text=1)
	
	jnts, crv = self.makeJoints(a=a, b=b, name=name, num=num)
	self.constrainJoints(a=a, b=b, jnts=jnts)
	pm.delete(crv)
	
    def loadJnt(self, fld=None):
	sel = pm.ls(sl=True)
	pm.textFieldButtonGrp(fld, e=True, text=sel[0])
	
    def makeJoints(self, a=None, b=None, name=None, num=None):
	pa = a.getTranslation(space='world')
	pd = b.getTranslation(space='world')
	pc = [ (pa[0]+pd[0])/2, (pa[1]+pd[1])/2, (pa[2]+pd[2])/2 ]
	pb = [ (pa[0]+pc[0])/2, (pa[1]+pc[1])/2, (pa[2]+pc[2])/2 ]
	
	crv = pm.curve(name=name+'_crv', p=[pa, pb, pc, pd])
	jnts = self.jointsOnCurve(crv=crv, num=num, name=name)
	return jnts, crv
	
    def constrainJoints(self, a=None, b=None, jnts=None):
	# Select two end joints, creates mid joint.
	# Constrains mid joint to follow and aim at second end joint.
	
	# Setup up locator
	loc = pm.spaceLocator(name='%s_upLoc' % a)
	pm.delete(pm.pointConstraint(b, loc, mo=0))
	
	# Adjust placement of Up object here
	moveAxis = pm.optionMenu(self.axisFld, q=1, value=1)
	if moveAxis == 'X': pm.move(20, loc, moveX=1)
	if moveAxis == 'Y': pm.move(20, loc, moveY=1)
	if moveAxis == 'Z': pm.move(20, loc, moveZ=1)
	pm.parent(loc, a)
	
	# Constrain joint
	for j in jnts:
	    pm.pointConstraint(a, b, j, mo=1)
	    pm.aimConstraint(b, j, wut='object', wuo=loc.name(), mo=1)

    def jointsOnCurve(self, crv=None, num=None, name=None):
	# Create n joint along selected curve
	if not crv: return
	if not num: return
	if not name: return
	if num < 1: return
	jnts = []
	param_increment = 1.0/float(int(num)+1)
	param = param_increment
	curveShape = pm.PyNode(crv).getShape()
	prnt = []
	for i in range(int(num)):
	    pm.select(clear=1)
	    # Create joint
	    jnt = pm.joint(n=name+'_'+str(i).zfill(2))
	    # Attach to curve
	    poci = pm.createNode('pointOnCurveInfo')
	    pm.connectAttr('%s.ws'%curveShape,'%s.inputCurve'%poci,f=1)
	    pm.connectAttr('%s.position'%poci,'%s.translate'%jnt,f=1)
	    pm.setAttr('%s.parameter'%poci,param)
	    pm.setAttr('%s.turnOnPercentage'%poci,1)
	
	    pm.disconnectAttr('%s.position'%poci,'%s.translate'%jnt)
	    pm.delete(poci)
	
	    if len(prnt):
		pm.parent(jnt,prnt[-1])
	
	    prnt.append(jnt)
	    param += param_increment
	    jnts.append(jnt)
	return jnts
    

