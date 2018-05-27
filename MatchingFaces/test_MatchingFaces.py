import os
import sys
    
import unittest
import pymel.core as pm

import MatchingFaces as mf
reload(mf)

class TestMatchingFaces(unittest.TestCase):
    def setUp(self):
        self.mf = mf.MatchingFaces()
        pm.newFile(f=True)
        self.res = 10
        
        # Two overlapping planes
        self.p1 = pm.polyPlane(n='plane1', sx=self.res, sy=self.res)[0]
        self.p2 = pm.polyPlane(n='plane2', sx=self.res, sy=self.res)[0]
        self.p3 = pm.polyPlane(n='plane3', sx=self.res, sy=self.res)[0]
        
        self.p1 = pm.PyNode(self.p1)
        self.p2 = pm.PyNode(self.p2)
        self.p3 = pm.PyNode(self.p3)
        
        # Non-overlapping plane
        pm.move(1, 1, 1, self.p3)

    #@unittest.skip('skipping...')
    def test_matchingFaces(self):
        v = 0 # Set to 1 for more verbose output
        expected = ['plane2Shape.f[%s]' % x for x in range(self.res*self.res)]
        
        faces = self.mf.check(self.p1, self.p2, v=v)
        for i in xrange(4):
            self.assertIn(faces[i].name(), expected)
        self.assertEqual(len(faces), len(expected))
            
    def test_nonMatchingFaces(self):
        v = 0 # Set to 1 for more verbose output
        faces = self.mf.check(self.p1, self.p3, v=v)
        self.assertEqual(faces, [])
        
    def test_almostEqual(self):
        v = 0 # Set to 1 for more verbose output
        x = pm.dt.Point(-0.5, -1.11022302463e-16, 0.5)
        y = pm.dt.Point(-0.51, -1.11022302463e-16, 0.5)
        z = pm.dt.Point(-0.52, -1.11022302463e-16, 0.5)
        
        result = self.mf._almostEqual(x, y, 0.01, v)
        self.assertTrue(result)
        
        result = self.mf._almostEqual(y, z, 0.01, v)
        self.assertTrue(result)
        
        result = self.mf._almostEqual(x, z, 0.01, v)
        self.assertFalse(result)
        
    def test_checkType(self):
        self.assertTrue(self.mf._checkType(self.p1, 'transform'))
        self.assertTrue(self.mf._checkType(self.p1.getShape(), 'mesh'))
        with self.assertRaises(Exception):
            self.mf._checkType(self.p1, 'mesh')
            
    def test_inBBox(self):
        out_faces = self.p3.f
        in_faces = self.p2.f
        
        self.assertTrue(self.mf._inBBox(self.p1, in_faces[0]))
        self.assertFalse(self.mf._inBBox(self.p1, out_faces[0]))
        
    def test_getCenters(self):
        p1 = pm.polyPlane(n='plane1', sx=1, sy=1)[0]
        p2 = pm.polyPlane(n='plane2', sx=2, sy=2)[0]
        
        expected1 = [pm.dt.Point(0,0,0)]
        expected2 = [pm.dt.Point(0.25, 0.0, 0.25),
                     pm.dt.Point(0.25, 0.0, -0.25),
                     pm.dt.Point(-0.25, 0.0, -0.25),
                     pm.dt.Point(-0.25, 0.0, 0.25)]
        
        faces1 = [p1.f]
        faces2 = p2.f
        
        centers1 = self.mf._getCenters(faces1)
        centers2 = self.mf._getCenters(faces2)
        
        self.assertListEqual(expected1, centers1)
        
        # Crappy test, but asserting points almost 
        # equal each other is a pain in the ass...
        exp2 = []
        for p in expected2:
            exp2.append(p.x)
            exp2.append(p.y)
            exp2.append(p.z)
        cent2 = []
        for p in centers2:
            cent2.append(p.x)
            cent2.append(p.y)
            cent2.append(p.z)
        exp2.sort()
        cent2.sort()
        
        for x,y in zip(exp2, cent2):
            self.assertAlmostEqual(x, y)
        
if __name__ == '__main__':
    unittest.main(verbosity=2) 