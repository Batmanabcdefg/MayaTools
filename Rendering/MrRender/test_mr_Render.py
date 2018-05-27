import unittest
import tempfile
import os

import mr_render as mr
reload(mr)

class Test_mr_render(unittest.TestCase):
    def setUp(self):
        self.mr = mr
    
    def tearDown(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_Job_preRun(self):
        pass
    
    
    def test_Job_run(self):
        job = mr.Job(statVar, cmd)
    
    def test_Job_infanticide(self):
        pass
    
    def test_CpuMonitor_run(self):
        pass
    
    def test_CpuMonitor_averageCPU(self):
        pass
    
    def test_CpuMonitor_checkCPU(self):
        pass
    
    def test_render(self):
        pass
         
        
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_mr_render)