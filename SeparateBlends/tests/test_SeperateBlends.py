import unittest
import os
import sys

from mock import MagicMock, patch, call

cwd = os.path.dirname(os.path.abspath(__file__).replace('tests',''))
if cwd not in sys.path:
    sys.path.append(cwd)

libDir = os.environ['REPOSDIR']+'/arttools/Libraries'
if libDir not in sys.path:
    sys.path.append(libDir)
    
from UnittestLib import UnittestLib
ulib = UnittestLib.UnittestLib()

import SeparateBlends
reload( SeparateBlends )

# Testing SeparateBlends

class test_getShaders(unittest.TestCase):
    @patch('SeparateBlends.pm')
    def test_getShaders(self,pymel):
        shaderStub = MagicMock(name='shaderMock')
        shaderStub.name.return_value = 'A_SB'
        badShaderStub = MagicMock(name='badShaderMock')
        badShaderStub.name.return_value = 'shader1'
        pymel.ls.return_value = [shaderStub,shaderStub,badShaderStub]
        returnValue = SeparateBlends._getShaders()
        
        ulib.assertListEqual(l1=returnValue, l2=[shaderStub,shaderStub])
        
class test_createSets(unittest.TestCase):
    @patch.object(SeparateBlends, '_vertsFromShader')
    @patch('SeparateBlends.pm')
    def test_createSets(self,pymel,vertsFromShader):
        pymel.partition.return_value = 'part'
        pymel.sets.return_value = 'set'
        
        SeparateBlends._createSets(shaders=['A_SB','B_SB','C_SB'])
        
        pmCalls = pymel.mock_calls
        shaderCalls = vertsFromShader.mock_calls
        
        assert call.sets(n='A_SB_set') in pmCalls
        assert call(shader='C_SB') in shaderCalls
        
class test_vertsFromShader(unittest.TestCase):
    @patch('SeparateBlends.pm')
    def test_vertsFromShader(self,pymel):
        shader = MagicMock(name='shader')
        SeparateBlends._vertsFromShader(shader=shader)
        
        # Can't think of what's useful to test... :(
        
class test_createVertShaderMap(unittest.TestCase):
    @patch('SeparateBlends.pm')
    def test_createVertShaderMap(self,pymel):
        mesh = MagicMock(name='mesh')
        sets = MagicMock(name='sets')
        
        SeparateBlends._createVertShaderMap(mesh=mesh,sets=sets) 
        
        
        
    
class test_floodWeightsOnSelected(unittest.TestCase):
    @patch('SeparateBlends.pm')
    def test_flood_1(self, pymel):
        v = MagicMock(name = 'VertexMock')
        v.name.return_value = 'mesh.vtx[34]' 
        pymel.ls.return_value = [v]
        blend = MagicMock(name='blendNodeMock')
        blend.name.return_value = 'blendNode'
        
        SeparateBlends._floodWeightsOnSelected(blendNode=blend,value=1)
        
        pymel.setAttr.assert_called_with('blendNode.inputTarget[0].inputTargetGroup[0].targetWeights[34]', 1)
        
class test_createTarget(unittest.TestCase):
    @patch('SeparateBlends.pm')
    def test_(self,pymel):
        SeparateBlends._createTarget(name='A',mesh='B')
        assert call.duplicate('B',n='A') in pymel.method_calls
    
class test_main(unittest.TestCase):
    @patch('SeparateBlends.pm')
    @patch.object(SeparateBlends, '_getShaders', side_effect=[MagicMock(name='shader')])
    @patch.object(SeparateBlends, '_createSets', side_effect=[ [MagicMock(name='set')] ])
    @patch.object(SeparateBlends, '_floodWeightsOnSelected')
    @patch.object(SeparateBlends, '_createTarget')
    def test_main(self, createTarget, floodWeights, createSets, getShaders, pm ):
        
        blendMock = MagicMock(name='blendShapeMock')
        pm.blendShape.side_effect = blendMock
        n = MagicMock(name='neutralMock')
        n.name.return_value = 'name'
        n.numVertices.return_value = 2
        t = MagicMock(name='targetMock')
        
        SeparateBlends.main(neutral=n, target=t)
        
        pm.mel.eval.assert_called_with("select -r name.vtx[0:1]")
        floodWeights.assert_called_with(blendNode=blendMock().__getitem__(),value=0)
        assert createSets.called
        assert getShaders.called
        assert createTarget.called        
        assert pm.sceneName.called
        
        
        
        
        