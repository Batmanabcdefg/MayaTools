import maya.cmds as cmds
import maya.mel as mel

class transformations():			
	def copySelectedPositions(self):
		""" Copy selected point positions. {1 : [0, 2.345, 1.324] } , onto selected mesh. Based on point order. """
		self.clipBoard = {}
		sel = cmds.ls(sl=True,fl=True)
		for src in sel:		
			pointNum = src.split("[")[1]
			pointNum = pointNum.split("]")[0]
			pos = cmds.xform('%s'%(src),query=True,ws=True,t=True)
			self.clipBoard[pointNum] = pos
				
	def pastePositionsOntoMesh(self):
		""" Paste values from self.clipBoard onto selected mesh. Assumes same point order. """
		mesh = cmds.ls(sl=True)[0]
		for point in self.clipBoard.keys():
			cmds.xform('%s.vtx[%s]'%(mesh,point),ws=True,t=self.clipBoard[point])
			
def transferPositions():
	""" Transfer point positions from src to tgt. Based on current selected meshes."""
	sel = cmds.ls(sl=True)
	for src in sel:
		# Go to start frame
		sTime = cmds.playbackOptions( query=True,min=True)
		eTime = cmds.playbackOptions( query=True,max=True)
		cmds.currentTime(sTime)
				
		# Setup top grp for duplicate geo
		if not cmds.objExists('MatchedGeoGrp'):
			grp = cmds.group(em=True,n='MatchedGeoGrp',w=True)
		else:
			grp = 'MatchedGeoGrp'
			
		# Duplicate
		tgt = cmds.duplicate(src,renameChildren=True)[0]
		
		cmds.parent(tgt,grp)
		
		# Per frame in time slider
		timeRange = eTime - sTime
		for key in range(timeRange):
			# Match the duplicate geo to the deforming original for each vert
			numVerts = cmds.polyEvaluate(src,v=True)
			for index in range(numVerts):
				a_pos = cmds.xform('%s.vtx[%s]'%(src,index),query=True,ws=True,t=True)
				cmds.xform('%s.vtx[%s]'%(tgt,index),ws=True,t=a_pos)
	
				# Key the position
				cmds.setKeyframe('%s.pt[%s].px'%(tgt,index))
				cmds.setKeyframe('%s.pt[%s].py'%(tgt,index))
				cmds.setKeyframe('%s.pt[%s].pz'%(tgt,index))
				
			# Increment time
			cmds.currentTime( cmds.currentTime(query=True)+1 )
def setup():
	""" 	Duplicate and constrain to original mesh.
		Operates on all selected geo with no skinCluster"""
	sel = cmds.ls(sl=True)
	
	setupGeo = []
	for mesh in sel:
		if mel.eval('findRelatedSkinCluster( "%s");'%mesh):
			print "Skipping: ",mesh
			continue
			
		elif cmds.listConnections(mesh,type="lattice"):
			print "Skipping: ",mesh
			continue
			
		# Setup top grp for duplicate geo
		if not cmds.objExists('BakedGeoGrp'):
			grp = cmds.group(em=True,n='BakedGeoGrp',w=True)
		else:
			grp = 'BakedGeoGrp'
			
		# Dupilcate
		dup = cmds.duplicate(mesh,renameChildren=True)
		
		# Hide original geo
		try:
			cmds.setAttr('%s.visibility'%mesh,0)
		except Exception, e:
			print e
			
		# Parent to BakedGeoGrp
		cmds.parent(dup,grp)
	
		# ParentConstrain to orig geo
		cmds.parentConstraint(mesh,dup,mo=True)
		
		print "Setup: ",mesh
		setupGeo.append(mesh)
		
	for each in setupGeo:
		print each
		
def cache():
	""" Cache the constrained duplicate geo """
	# GeoCache selected
	sel = cmds.ls(sl=True)
	grp = cmds.group(em=True,n='CachedGeoGrp')
	for mesh in sel:
		if cmds.objectType(mesh) == 'transform':
			try:
				shape = cmds.listRelatives(mesh,shapes=True)[0]
				if cmds.objectType(shape) == 'mesh':
					if mel.eval('findRelatedSkinCluster( "%s");'%mesh):
						cacheFiles = cmds.cacheFile( st=290, et=344, points=shape,dir='/Users/mauricioptkvp/Desktop/21_July_2010_scarecrow_rig - Copy/CleanedUp/geoCaches')
						cmds.parent(mesh,grp)
						print 'Cached: ',shape
			except Exception,e:
				print e

