import unittest
import maya.standalone as standalone
import maya.cmds as cmds

import ClusterControl

class TestClusterControl(unittest.TestCase):

	def setUp(self):
		# Start Maya
		standalone.initialize(name='python')
	
		# Initial preset values
		self.input = {}
		self.input['control_options'] =	 {'name':'cnt1', 'shape':'circle', 'color':'red', 'control_grp':'controls_grp', 'scale':1}
		self.input['cluster_options'] = {'relative':True, 'resolution':'Full','angle_interp':'Closest'}
		self.input['parentConstraint_options'] = {'interp_type':'Average', 'buffer_node':'cnt1_buffer', 'follow':'back_jnt_2'}
		self.input['geo_options'] = { 'name':'pSphere01', 'vertices':'pSphere01Shape.vtx[0:100]', 'radius':5 }	

	def test_buildControl(self):
		# Initialize test scene
		self._initializeScene()
		
		# Get object instance
		reload( ClusterControl )
		cc = ClusterControl.ClusterControl()
		
		# Create a control
		status = cc.buildControl( name=self.input['control_options']['name'],
							   shape=self.input['control_options']['shape'],
							   color=self.input['control_options']['color'],
							   parent=self.input['control_options']['control_grp'],
							   scale=self.input['control_options']['scale'] )
		
		self.assertFalse( cmds.objExists( self.input['control_options']['name'] ) )
		self.assertEquals( status, 0 )
	
	def _initializeScene(self):
		r""" Create initial scene setup for testing cluster control creation. """
		# Open a new scene
		cmds.file(new=True,f=True)
	
		cmds.group(em=True, n=self.input['control_options']['control_grp'])
		
		# Create mesh
		cmds.polySphere(n=self.input['geo_options']['name'],radius=self.input['geo_options']['radius'])
		
		# Create joint chain
		joints = [ 'back_jnt_'+str(x+1).zfill(2) for x in range(5) ]
		pos = [ 0,0,0 ]
		for jnt in joints:
			cmds.joint( n=jnt,position=( pos[0],pos[1],pos[2] ) )
			pos = [pos[0],pos[1]+1,pos[2]]
			
		# Skin mesh to joints
		cmds.skinCluster(joints[:-1],self.input['geo_options']['name'])
			
if __name__ == '__main__':
	unittest.main()

