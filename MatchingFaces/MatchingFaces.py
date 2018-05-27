import time
import sets
import pymel.core as pm

class MatchingFaces():
    '''
    Given mesh1 and mesh2, check if any face in mesh1 overlaps a face in mesh2
    
    Example:
        
    import MatchingFaces as mfs
    mf = mfs.MatchingFaces()
    
    sel = pm.ls(sl=1)
    a = sel[0]
    b = sel[1]
    
    faces = mf.check(a, b)

    '''
    def _almostEqual(self, point1, point2, tolerance=0.1, v=0):
        '''
        if type(point1) != pm.dt.Point:
            raise Exception('%s not of type dt.Point' % point1)
        elif type(point2) != pm.dt.Point:
            raise Exception('%s not of type dt.Point' % point2)        
        '''
        vec = pm.dt.Vector(point1 - point2)
        if vec.length() > (tolerance + 0.00000001):
            if v: print str(v.length()), "not within", tolerance, "tolerance."
            return False
        if v: print str(v.length()), "is within", tolerance, "tolerance."
        return True
            
    def _checkType(self, obj, typ):
        '''
        Return true if obj is of type typ, false otherwise
        '''
        if not pm.objectType(obj, isType=typ):
            raise Exception(str(obj) + " not of type: " + str(typ))
        return True
    
    def _inBBox(self, obj, face, v=0):
        '''
        True if face is within bounding box of obj
        '''
        self._checkType(obj, 'transform')
        self._checkType(face, 'mesh')
        
        # Get face center
        center = self._getCenters([face])[0]
        
        bb = obj.getBoundingBox()
        if bb.contains(center):
            return True
        return False
    
    def _getCenters(self, faces):
        '''
        Given list of Faces,
        return list of Points representing centers of faces
        '''
        centers = []
        for f in faces:
            points = f.getPoints(space='world')
            center = pm.dt.Point()
            for p in points:
                center += p
            center = pm.dt.Point(center.x/4.0,
                                 center.y/4.0,
                                 center.z/4.0)
            centers.append(center)
        return centers
        
    
    def check(self, mesh1, mesh2, tolerance=0.1, v=0):
        '''
        Returns list of mesh2 faces that overlap mesh1 faces.
        Return: [ MeshFace(u'pPlaneShape2.f[0]'), ... ]
        '''
        start_time = time.time()
        self._checkType(mesh1, 'transform')
        self._checkType(mesh2, 'transform')
        self._checkType(mesh1.getShape(), 'mesh')
        self._checkType(mesh2.getShape(), 'mesh')        
        
        tgt_faces = []
        overlapping = []
        
        if v: print '\nChecking: ', mesh1, ', ', mesh2
                    
        for face1 in mesh1.f:
            center = self._getCenters([face1])[0]
            
            temp = mesh2.getClosestPoint(center, space='world')
            face2 = pm.PyNode("%s.f[%s]" % (mesh2.name(), temp[1]))  
            
            if v: print '\nChecking face: ', face1
            if v: print 'Against face: ', face2
            
            if face2 in overlapping:
                continue
            
            count = 0
            p1s = face1.getPoints(space='world')
            p2s = face2.getPoints(space='world')
            for p1 in p1s:
                if v: print 'Checking point: ', p1
                for p2 in p2s: 
                    if v: print 'Against point: ', p2
                    if self._almostEqual(p1, p2, tolerance):
                        count += 1
                        if v: print 'Match ', count, ': ', p1, ' | ', p2
                        if count == 4:
                            if v: print 'Adding face: ', face2
                            overlapping.append(face2)
                        break
                               
        print("\n--- Runtime: %s seconds ---" % (time.time() - start_time))
        return overlapping

'''        
path = '/pipeline_folder/GoogleDrive/MSH_Maya/MatchingFaces'
import sys
import pymel.core as pm
if path not in sys.path:
    sys.path.append(path)

import MatchingFaces as mfs
mf = mfs.MatchingFaces()

sel = pm.ls(sl=1)
a = sel[0]
b = sel[1]

faces = mf.check(a, b)
pm.select(faces, r=1)       

'''