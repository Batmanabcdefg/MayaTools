import maya.cmds as cmds
import shapes

class ui(object):
	r"""
	Interface to create / edit a cluster control.
	"""
	def __init__(self,**kwargs):
		try:
			self.create_ui(kwargs)
		except Exception,e:
			print 'Error: ',e
	
	def create_ui(self,kwargs):
		r""" 
		Draw the interface
		"""
		status = 0
		
		return status
		
	def build(self,data):
		r"""
		Invoke build method and pass ui data
		"""
		status = 0
		ClusterControl(data)
		return status
		
	def getUiData(self):
		r"""
		Return a dict: {arg : data}
		"""
		status = 0
		return status
	
class ClusterControl(object):
	r"""
	Build Cluster Control process.
	"""	
	def build(self, data):
		r""" Call all the build methods. """
		self.buildControl( name=data['control_options']['name'],
							   shape=data['control_options']['shape'],
							   color=data['control_options']['color'],
							   parent=data['control_options']['control_grp'],
							   scale=data['control_options']['scale'] )
		
	def buildControl(self,name=None,shape='circle',color='blue',parent=None,scale=1):
		r"""
		Create control curve and place it in heirarchy
		"""
		if not name:
			raise Exception('Need to specify a name.')
		
		for attr in [name,shape,color,parent]:
			if not isinstance(attr,str):
				raise Exception('Input value error: Expecting type string, got: ',attr) 
		if parent:
			if not cmds.objExists(parent): raise Exception('Parent does not exist: ',parent)
			
		status = 0
		crv = 
		
		return status
			
		
					
					
					
					
					
					
					
					
					
					
