import math, sys

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kPluginNodeTypeName = "spSpace"
kPluginNodeId = OpenMaya.MTypeId(0x87005)

# Node definition
class space(OpenMayaMPx.MPxNode):
	"""
	Connect two transform nodes with frozen translations / rotations as inputs.
	These nodes are the reference positions for the spaces to be used by the output positional data.(Object 0,0,0)
	
	Connect the output to a buffer node, above the zero node that is above the control, with it's pivot at the origin. (World 0,0,0)
	
	Upon switch: Changes the coordinate system used by control. Keeps the world position by adding the delta between the spaces.
	"""
	# Static Class variables (Attributes)
	switch = OpenMaya.MObject()
	at = OpenMaya.MObject()
	ar = OpenMaya.MObject()
	bt = OpenMaya.MObject()
	br = OpenMaya.MObject()

	objAtx = OpenMaya.MObject()
	objAty = OpenMaya.MObject()
	objAtz = OpenMaya.MObject()
	objArx = OpenMaya.MObject()
	objAry = OpenMaya.MObject()
	objArz = OpenMaya.MObject()
	objBtx = OpenMaya.MObject()
	objBty = OpenMaya.MObject()
	objBtz = OpenMaya.MObject()
	objBrx = OpenMaya.MObject()
	objBry = OpenMaya.MObject()
	objBrz = OpenMaya.MObject()

	# Outputs
	to = OpenMaya.MObject()
	ro = OpenMaya.MObject()
	
	otX = OpenMaya.MObject()
	otY = OpenMaya.MObject()
	otZ = OpenMaya.MObject()
	orX = OpenMaya.MObject()
	orY = OpenMaya.MObject()
	orZ = OpenMaya.MObject()
	
	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

	def addAttr(self,ln=None,sn=None,type='MFnNumericAttribute',dataType='OpenMaya.MFnNumericData.kFloat',writable=True,keyable=True,storable=True,default=None,min=None,max=None)
		""" Create an attribute on a node. To be called in nodeInitializer( ) """
		if type == 'MFnCompoundAttribute':
			createAttr = OpenMaya.MFnCompoundAttribute()
			return createAttr.create(ln, sn)
			
		elif type == 'MFnNumericAttribute':
			createAttr = OpenMaya.MFnNumericAttribute()
		else:
			raise Exception('Invalid type. Use: MFnNumericAttribute OR MFnCompoundAttribute')
		
		attr = createAttr.create(ln, sn, type, dataType, default )
		
		if min:
			createAttr.setMn(min)
		if max:
			createAttr.setMax(max)
		if keyable:
			createAttr.setKeyable(True)
		if keyable == False::
			createAttr.setKeyable(False)
		if storable:
			createAttr.setStorable(True)
		if storable == False:
			createAttr.setStorable(False)
		if writable:
			createAttr.setWritable(True)
		if writable == False:
			createAttr.setWritable(False)
			
		return attr 
		
	def compute(self, plug, data):
		# Check that the requested recompute is one of the output values
		#if plug == space.o1t or plug == space.o1r or plug.parent() == space.o1t or plug.parent() == space.o1r or plug == space.o2t or plug == space.o2r or plug.parent() == space.o2t or plug.parent() == space.o2r:
		# Get dataBlock handles to input plugs
		atxData = data.inputValue(space.objAtx)
		atyData = data.inputValue(space.objAty)
		atzData = data.inputValue(space.objAtz)
		arxData = data.inputValue(space.objArx)
		aryData = data.inputValue(space.objAry)
		arzData = data.inputValue(space.objArz)
		btxData = data.inputValue(space.objBtx)
		btyData = data.inputValue(space.objBty)
		btzData = data.inputValue(space.objBtz)
		brxData = data.inputValue(space.objBrx)
		bryData = data.inputValue(space.objBry)
		brzData = data.inputValue(space.objBrz)
		switchData = data.inputValue(space.switch)

	       # Store values
	       aValues = [atxVal = atxData.asFloat(),
			       atyVal = atyData.asFloat(),
			       atzVal = atzData.asFloat(),
			       arxVal = arxData.asFloat(),
			       aryVal = aryData.asFloat(),
			       arzVal = arzData.asFloat()
			       ]
			       
	       bValues = [btxVal = btxData.asFloat(),
			       btyVal = btyData.asFloat(),
			       btzVal = btzData.asFloat(),
			       brxVal = brxData.asFloat(),
			       bryVal = bryData.asFloat(),
			       brzVal = brzData.asFloat()
			       ]
			       
	       switchVal  = switchData.asInt()
	       
	       # Get handles to output plugs
	       outValues = [otxHandle = data.outputValue(space.otX),
			       otyHandle = data.outputValue(space.otY),
			       otzHandle = data.outputValue(space.otZ),
			       orxHandle = data.outputValue(space.orX),
			       oryHandle = data.outputValue(space.orY),
			       orzHandle = data.outputValue(space.orZ)
			       ]

		# Get delta from old space to new space (World space calculation)
		if switchVal == 0: # delta = input2 - input1
			delta = [ (bValues[0]-aValues[0]), (bValues[1]-aValues[1]), (bValues[2]-aValues[2]) ]
		if switchVal == 1: # delta = input1 - input2
			delta = [ (aValues[0]-bValues[0]), (aValues[1]-bValues[1]), (aValues[2]-bValues[2]) ]
			
		# Add delta once to output positional values
		if switchVal == 0:
		       outValues[0].setFloat(delta[0])
		       outValues[1].setFloat(delta[1])
		       outValues[2].setFloat(delta[2])
		if switchVal == 1:
		       outValues[0].setFloat(delta[0])
		       outValues[1].setFloat(delta[1])
		       outValues[2].setFloat(delta[2])
	
	       data.setClean(plug)
	       #else:
		   #return OpenMaya.MStatus.kUnknownParameter
	
	       return OpenMaya.MStatus.kSuccess

# creator
def nodeCreator():
	return OpenMayaMPx.asMPxPtr( space() )

# initializer
def nodeInitializer():
	""" Define attributes. Store them in the static class variables (MObjects). """
	# Setup the input attributes
	space.switch = self.addAttr(ln="switch",sn="sw",type='MFnNumericAttribute',dataType='OpenMaya.MFnNumericData.kInt',default=0,min=0,max=1)

	# Define input child attributes
	space.objAtx = self.addAttr(ln="objA_translateX",sn="oatx",default=0)
	space.objAty = self.addAttr(ln="objA_translateX",sn="oatx",default=0)
	space.objAtz = self.addAttr(ln="objA_translateX",sn="oatx",default=0)
	space.objArx = self.addAttr(ln="objA_translateX",sn="oatx",default=0)
	space.objAry = self.addAttr(ln="objA_translateX",sn="oatx",default=0)
	space.objArz = self.addAttr(ln="objA_translateX",sn="oatx",default=0)
	
	space.objBtx = self.addAttr(ln="objB_translateX",sn="oatx",default=0)
	space.objBty = self.addAttr(ln="objB_translateX",sn="oatx",default=0)
	space.objBtz = self.addAttr(ln="objB_translateX",sn="oatx",default=0)
	space.objBrx = self.addAttr(ln="objB_translateX",sn="oatx",default=0)
	space.objBry = self.addAttr(ln="objB_translateX",sn="oatx",default=0)
	space.objBrz = self.addAttr(ln="objB_translateX",sn="oatx",default=0)

	# Define output child attributes
	space.otX = self.addAttr( ln="output_translateX", sn="otx", default=0, writeable=False, storeable=False )
	space.otY = self.addAttr( ln="output_translateY", sn="oty", default=0, writeable=False, storeable=False )
	space.otZ = self.addAttr( ln="output_translateX", sn="otz", default=0, writeable=False, storeable=False )
	space.orX = self.addAttr( ln="output_rotateX", sn="orx", default=0, writeable=False, storeable=False )
	space.orY = self.addAttr( ln="output_rotateY", sn="ory", default=0, writeable=False, storeable=False )
	space.orZ = self.addAttr( ln="output_rotateZ", sn="orz", default=0, writeable=False, storeable=False )
	
	# Define input  compound attributes
	space.at = cAttr.create("A_Translations", "at")
	cAttr.addChild(space.objAtx)
	cAttr.addChild(space.objAty)
	cAttr.addChild(space.objAtz)
	space.ar = cAttr.create("A_Rotations", "ar")
	cAttr.addChild(space.objArx)
	cAttr.addChild(space.objAry)
	cAttr.addChild(space.objArz)
	space.bt = cAttr.create("B_Translations", "bt")
	cAttr.addChild(space.objBtx)
	cAttr.addChild(space.objBty)
	cAttr.addChild(space.objBtz)
	space.br = cAttr.create("B_Rotations", "br")
	cAttr.addChild(space.objBrx)
	cAttr.addChild(space.objBry)
	cAttr.addChild(space.objBrz)

	# Define output  compound attributes
	space.to = cAttr.create("outTranslations", "ot")
	cAttr.addChild(space.otX)
	cAttr.addChild(space.otY)
	cAttr.addChild(space.otZ)
	space.ro = cAttr.create("outRotations", "or")
	cAttr.addChild(space.orX)
	cAttr.addChild(space.orY)
	cAttr.addChild(space.orZ)

	# Add the attributes to the node
	space.addAttribute(space.switch)
	
	# Compound attrs
	space.addAttribute(space.at)
	space.addAttribute(space.ar)
	space.addAttribute(space.bt)
	space.addAttribute(space.br)
	space.addAttribute(space.to)
	space.addAttribute(space.ro)
	
	# Set the attribute dependencies
	space.attributeAffects(space.switch, space.to)
	space.attributeAffects(space.switch, space.ro)
	space.attributeAffects(space.at, space.to)
	space.attributeAffects(space.ar, space.ro)
	space.attributeAffects(space.bt, space.to)
	space.attributeAffects(space.br, space.ro)
	
   # initialize the script plug-in
def initializePlugin(mobject):
   mplugin = OpenMayaMPx.MFnPlugin(mobject, "MS", "1.0", "2010")
   try:
       mplugin.registerNode( kPluginNodeTypeName, kPluginNodeId, nodeCreator, nodeInitializer )
   except:
       sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )
       raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
   mplugin = OpenMayaMPx.MFnPlugin(mobject)
   try:
       mplugin.deregisterNode( kPluginNodeId )
   except:
       sys.stderr.write( "Failed to deregister node: %s" % kPluginNodeTypeName )
       raise