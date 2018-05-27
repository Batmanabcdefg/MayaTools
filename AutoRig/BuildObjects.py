'''
Define the elements of a rig as 3D software agnostic Python classes.
'''

class Joint(object):
    ''' Joint object used for skinning / animation '''
    def __init__(self):
        self.name = None            # String
        self.position = []          # [Float, Float, Float]
        self.orientation = []       # [Float, Float, Float]
        self.rotationOrder = None   # String
        self.parent = None          # Joint object
        self.children = []          # Joint object(s)
        
    def toXML(self):
        ''' Output data as a self contained xml string '''
        
class Control(object):
    ''' Control object to be used for animation '''
    def __init__(self):
        self.name = None            # String
        self.icon = None            # Icon object
        self.connectJoint = None    # Joint object to be driven by control
        
    def toXML(self):
        ''' Output data as a self contained xml string '''
        

class Icon(object):
    ''' 3D points to draw a control curve '''
    def __init__(self):
        self.name = None            # String
        self.points = []            # List of position Point objects
        
    def create(self):
        ''' To be overwritten by software specific inherited object '''
        
    def toXML(self):
        ''' Output data as a self contained xml string '''
        
class Point(object):
    ''' 3D point as x, y, z coordinate '''
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        
    def toXML(self):
        ''' Output data as a self contained xml string '''

class Geometry(object):
    ''' Information regarding geometry '''
    def __init__(self):
        self.name = None
        self.skinData = None        # Path to xml data file
        
    def getJoints(self):
        pass    
    
    def toXML(self):
        ''' Output data as a self contained xml string '''
    
