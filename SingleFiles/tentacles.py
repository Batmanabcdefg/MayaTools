import maya.cmds as mc

class tentacles():
	"""
	Given a selected joint:
	-Select control, then joint
	-Associate numJoints children joint rotations to controller
	"""
	def __init__(self,*args):
		if(mc.window("ms_ConnectControlWin",exists=True)):
			mc.deleteUI("ms_ConnectControlWin",window=True)
		mc.window("ms_ConnectControlWin",title="Connect Control v1.0",rtf=True)

		#main window
		mc.columnLayout()

		self.controlField = mc.textFieldButtonGrp( label="Control", buttonLabel="Load", bc = self.loadControl)
		self.jointField = mc.textFieldButtonGrp( label="Joint", buttonLabel="Load", bc = self.loadJoint)
		mc.text("Number of joints to connect:")
		self.numField = mc.intField( )

		mc.button(label="Connect",c=self.connect)
		
		mc.showWindow("ms_ConnectControlWin")
	
	def connect(self,*args):
		#number of child joints from selection to associate 
		control =  mc.textFieldButtonGrp( self.controlField,query=True,text=True)
		joint =  mc.textFieldButtonGrp( self.jointField,query=True,text=True)
		numJoints = mc.intField(self.numField, query=True,v=True)
		
		#get the hierarchy of joints below the selected one
		mc.select(joint,hi=True,r=True)
		joints  = mc.ls(sl=True)

		#only connect the buffer groups to the controller
		counter = 0
		for each in joints:
			if(counter==(numJoints*3)): #*2 because traversing 2 nodes per joint
				break
			if(mc.nodeType(each) == "transform"):#Only connect the buffer nodes
				#print "Inside: %i"%counter
				mc.connectAttr("%s.rotateX"%(control), "%s.rotateX"%each,f=True)
				mc.connectAttr("%s.rotateY"%(control), "%s.rotateY"%each,f=True)
				mc.connectAttr("%s.rotateZ"%(control), "%s.rotateZ"%each,f=True)	
			counter = counter + 1

	def loadControl(self,*args):
		sel = mc.ls(sl=1)
		mc.textFieldButtonGrp(self.controlField,edit=True,text=sel[0])

	def loadJoint(self,*args):
		sel = mc.ls(sl=1)
		mc.textFieldButtonGrp(self.jointField,edit=True,text=sel[0])
		

	

