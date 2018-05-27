import unittest
import pymel.core as pm
import os
import sys

cwd = os.path.dirname(os.path.abspath(__file__).replace('tests', ''))
devDir = cwd.replace('FollowRibbon', '')
testDir = os.path.dirname(os.path.abspath(__file__))
if cwd not in sys.path:
    sys.path.append(cwd)
if devDir not in sys.path:
    sys.path.append(devDir)

from UnittestLib import UnittestLib
reload( UnittestLib )
import FollowRibbon
reload( FollowRibbon )

class test_FollowRibbon(unittest.TestCase):
    def setUp(self):
        self.testLib = UnittestLib.UnittestLib()
        pm.newFile(f=True)
    
    def tearDown(self):
        pass
    
    def test_clusterPlane(self):
        fr = FollowRibbon.FollowRibbon(name='blah')
        plane = pm.nurbsPlane(axis=[0,1,0],patchesU=8,patchesV=1,lengthRatio=.1,ch=0)[0]
        ctrls = []
        ctrls.append(pm.circle(n='blah_ctrl_01')[0].name())
        ctrls.append(pm.circle(n='blah_ctrl_02')[0].name())
        mainGrp = pm.group(em=1, name='main')
        
        result = fr._clusterPlane(plane=plane, controls=ctrls, mainGrp='main')
        
        self.testLib.assertListEqual(result,['blah_cluster_01Handle','blah_cluster_02Handle'])
        self.assertTrue(pm.objExists('blah_cluster_01'))
        self.assertTrue(pm.objExists('blah_cluster_02'))
        
        self.assertTrue(pm.listRelatives(result[0],parent=True), 'main')
        self.assertTrue(pm.listRelatives(result[1],parent=True), 'main')
        
        self.assertTrue(pm.listRelatives(result[0], parent=1)[0], 'blah_ctrlsGrp')
        self.assertTrue(pm.listRelatives(result[1], parent=1)[0], 'blah_ctrlsGrp')
        
        hist = pm.listHistory(plane)
        hitA = 0
        hitB = 0
        for each in hist:
            if each.name() == 'blah_cluster_01':
                hitA = 1
            if each.name() == 'blah_cluster_02':
                hitB = 1
        self.assertTrue(hitA)
        self.assertTrue(hitB)
        
        self.assertTrue(pm.isConnected('blah_ctrl_01.translate', 'blah_cluster_01Handle.translate'))
        self.assertTrue(pm.isConnected('blah_ctrl_02.translate', 'blah_cluster_02Handle.translate'))
    
    def test_notPassingInName(self):
        self.assertRaises(Exception, FollowRibbon.FollowRibbon)
    
    def test_createPlaneControls(self):
        fr = FollowRibbon.FollowRibbon(name='blah')
        plane = pm.nurbsPlane(axis=[0,1,0],patchesU=8,patchesV=1,lengthRatio=.1,ch=0)[0]
        
        grps, jnts, cposNodes = fr._createPlaneControls( plane=plane, direction='u', number=6 )
        
        self.testLib.assertListEqual(cposNodes, ['blah_drvCPOS_01', 
                                                 'blah_drvCPOS_02', 
                                                 'blah_drvCPOS_03',
                                                 'blah_drvCPOS_04',
                                                 'blah_drvCPOS_05',
                                                 'blah_drvCPOS_06'])
        
        self.assertEqual(grps[0].name(), 'blah_drvGrp_01')
        self.assertEqual(grps[1].name(), 'blah_drvGrp_02')
        self.assertEqual(grps[2].name(), 'blah_drvGrp_03')
        self.assertEqual(grps[3].name(), 'blah_drvGrp_04')
        self.assertEqual(grps[4].name(), 'blah_drvGrp_05')
        self.assertEqual(grps[5].name(), 'blah_drvGrp_06')        
        
        self.assertEqual(jnts[0].name(), 'blah_drvJnt_01')
        self.assertEqual(jnts[1].name(), 'blah_drvJnt_02')
        self.assertEqual(jnts[2].name(), 'blah_drvJnt_03')
        self.assertEqual(jnts[3].name(), 'blah_drvJnt_04') 
        self.assertEqual(jnts[4].name(), 'blah_drvJnt_05')
        self.assertEqual(jnts[5].name(), 'blah_drvJnt_06')        
        
        self.assertTrue(pm.objExists('blah_drvCPOS_01'))
        self.assertTrue(pm.objExists('blah_drvCPOS_02'))
        self.assertTrue(pm.objExists('blah_drvCPOS_03'))
        self.assertTrue(pm.objExists('blah_drvCPOS_04')) 
        self.assertTrue(pm.objExists('blah_drvCPOS_05'))
        self.assertTrue(pm.objExists('blah_drvCPOS_06'))         
        
        self.assertEqual(pm.getAttr('blah_drvCPOS_01.turnOnPercentage'), 1)
        
        self.assertEqual(pm.getAttr('blah_drvCPOS_01.parameterV'), .5)
        self.assertEqual(pm.getAttr('blah_drvCPOS_02.parameterV'), .5)
        self.assertEqual(pm.getAttr('blah_drvCPOS_03.parameterV'), .5)
        self.assertEqual(pm.getAttr('blah_drvCPOS_04.parameterV'), .5)
        self.assertEqual(pm.getAttr('blah_drvCPOS_05.parameterV'), .5)
        self.assertEqual(pm.getAttr('blah_drvCPOS_06.parameterV'), .5)
        
        self.assertAlmostEquals(pm.getAttr('blah_drvCPOS_01.parameterU'), 0)
        self.assertAlmostEquals(pm.getAttr('blah_drvCPOS_02.parameterU'), .2, 2)
        self.assertAlmostEquals(pm.getAttr('blah_drvCPOS_03.parameterU'), .4, 2)
        self.assertAlmostEquals(pm.getAttr('blah_drvCPOS_04.parameterU'), .6, 2)
        self.assertAlmostEquals(pm.getAttr('blah_drvCPOS_05.parameterU'), .8, 2)
        self.assertAlmostEquals(pm.getAttr('blah_drvCPOS_06.parameterU'), 1)

        self.assertTrue(pm.objExists('blah_drvGrp_01'))
        self.assertTrue(pm.objExists('blah_drvGrp_02'))
        self.assertTrue(pm.objExists('blah_drvGrp_03'))
        self.assertTrue(pm.objExists('blah_drvGrp_04'))
        self.assertTrue(pm.objExists('blah_drvGrp_05'))
        self.assertTrue(pm.objExists('blah_drvGrp_06'))
        
        self.assertTrue(pm.isConnected('blah_drvCPOS_01.position','blah_drvGrp_01.translate'))
        self.assertTrue(pm.isConnected('blah_drvCPOS_02.position','blah_drvGrp_02.translate'))
        self.assertTrue(pm.isConnected('blah_drvCPOS_03.position','blah_drvGrp_03.translate'))
        self.assertTrue(pm.isConnected('blah_drvCPOS_04.position','blah_drvGrp_04.translate'))    
        self.assertTrue(pm.isConnected('blah_drvCPOS_05.position','blah_drvGrp_05.translate')) 
        self.assertTrue(pm.isConnected('blah_drvCPOS_06.position','blah_drvGrp_06.translate')) 
        
        self.assertTrue(pm.objExists('blah_drvJnt_01'))
        self.assertTrue(pm.objExists('blah_drvJnt_02'))
        self.assertTrue(pm.objExists('blah_drvJnt_03'))
        self.assertTrue(pm.objExists('blah_drvJnt_04'))  
        self.assertTrue(pm.objExists('blah_drvJnt_05')) 
        self.assertTrue(pm.objExists('blah_drvJnt_06')) 
        
        self.assertEqual(pm.listRelatives('blah_drvJnt_01', parent=1)[0],'blah_drvGrp_01')
        self.assertEqual(pm.listRelatives('blah_drvJnt_02', parent=1)[0],'blah_drvGrp_02')
        self.assertEqual(pm.listRelatives('blah_drvJnt_03', parent=1)[0],'blah_drvGrp_03')
        self.assertEqual(pm.listRelatives('blah_drvJnt_04', parent=1)[0],'blah_drvGrp_04')
        self.assertEqual(pm.listRelatives('blah_drvJnt_05', parent=1)[0],'blah_drvGrp_05')
        self.assertEqual(pm.listRelatives('blah_drvJnt_06', parent=1)[0],'blah_drvGrp_06')
        
    def test_createDriveControls(self):
        fr = FollowRibbon.FollowRibbon(name='blah')
        plane = pm.nurbsPlane(axis=[0,1,0],patchesU=8,patchesV=1,lengthRatio=.1,ch=0)[0]
        grps, jnts, cposNodes = fr._createPlaneControls( plane=plane, direction='u', number=4 )
        
        mainGrp, ctrls = fr._createDriveControls( grps=grps, cposNodes=cposNodes )
        
        self.assertEqual(mainGrp, 'blah_ctrlsGrp')
        self.testLib.assertListEqual(ctrls, ['blah_ctrl_01', 'blah_ctrl_02', 'blah_ctrl_03', 'blah_ctrl_04'])
        
        for index in range(4):
            self.assertTrue(pm.objExists('blah_ctrlTopGrp_%s'%str(index+1).zfill(2)))
            self.assertTrue(pm.objExists('blah_ctrlMidGrp_%s'%str(index+1).zfill(2)))
            self.assertTrue(pm.objExists('blah_ctrlBtmGrp_%s'%str(index+1).zfill(2)))
            self.assertTrue(pm.objExists('blah_InvertMdNode_%s'%str(index+1).zfill(2)))
            self.assertTrue(pm.objExists('blah_ctrl_%s'%str(index+1).zfill(2)))
            
            self.assertEqual(pm.listRelatives('blah_ctrlTopGrp_%s'%str(index+1).zfill(2),parent=1)[0].name(),
                             'blah_ctrlsGrp')
            
            self.testLib.assertConstrained(grps[index].name(), 'blah_ctrlTopGrp_%s'%str(index+1).zfill(2), type='parent')
            
            self.assertTrue(pm.isConnected('blah_ctrl_%s.translate'%str(index+1).zfill(2), 
                                           'blah_InvertMdNode_%s.input1'%str(index+1).zfill(2)))        
            self.assertTrue(pm.isConnected('blah_InvertMdNode_%s.output'%str(index+1).zfill(2),
                                           'blah_ctrlBtmGrp_%s.translate'%str(index+1).zfill(2)))
            
            self.assertTrue(pm.objExists('blah_ctrl_%s.uParam'%str(index+1).zfill(2)))
            self.assertTrue(pm.objExists('blah_ctrl_%s.vParam'%str(index+1).zfill(2)))
            
            self.assertTrue(pm.isConnected('blah_ctrl_%s.uParam'%str(index+1).zfill(2),'blah_drvCPOS_%s.parameterU'%str(index+1).zfill(2)))
            self.assertTrue(pm.isConnected('blah_ctrl_%s.vParam'%str(index+1).zfill(2),'blah_drvCPOS_%s.parameterV'%str(index+1).zfill(2)))   
            