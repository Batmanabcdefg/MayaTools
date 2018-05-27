import logging
import math

import maya.cmds as cmds
import maya.mel as mel

class UnittestLib(object):
    def __init__(self,version='1.0',log=False,loglevel=logging.DEBUG,logFileMode='a'):
        ''' Set version and initialize logging '''
        self.version = version
        self.logger=None
        if log:
            # Setup logging
            logging.basicConfig( level=logging.DEBUG, fileName='UnittestLib.log',filemode=logFileMode, 
                                 format= '%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                 datefmt='%m/%d/%Y %I:%M:%S %p' )
            self.logger = logging.getLogger('UnittestLib')

        # Start logging
        if self.logger: 
            self.logger.info('UnittestLib %s: Initialized...'%self.version) 
            
    def assertListEqual(self, l1=None, l2=None):
        ''' Assert two list are equal '''
        if self.logger: 
            self.logger.info('assertListEqual(): Start...')     
            
        if len(l1) != len(l2):
            if self.logger: 
                self.logger.error('Assertion False. Lists are of unequal lengths.')             
            raise AssertionError('Assertion False. Lists are of unequal lengths.')
        
        for a,b in zip(l1,l2):
            if a != b:
                if self.logger: 
                    self.logger.error('Assertion False. "%s" is not equal to "%s".'%(a,b))                
                raise AssertionError('Assertion False. "%s" is not equal to "%s".'%(a,b))
            
        if self.logger: 
            self.logger.info('assertListEqual(): End...')       
            
        return True
    
    def assertFloatListAlmostEqual(self, l1=None, l2=None, tolerance=0.01):
        ''' Assert two list are equal within tolerance'''
        if self.logger: 
            self.logger.info('assertFloatListAlmostEqual(): Start...')     
            
        if len(l1) != len(l2):
            if self.logger: 
                self.logger.error('Assertion False. Lists are of unequal lengths.')             
            raise AssertionError('Assertion False. Lists are of unequal lengths.')
        
        for a,b in zip(l1,l2):
            # 0.00000001 needed to account for float run off in subtraction: 1.1 - 1.09 = 0.010000000000000009
            if (a - b) > (tolerance+0.00000001) :
                if self.logger: 
                    self.logger.error('Assertion False. "%s" is not equal to "%s" within tolerance of: %s.'%(a,b,tolerance))                
                raise AssertionError('Assertion False. "%s" is not equal to "%s" within tolerance of: %s.'%(a,b,tolerance))
            
        if self.logger: 
            self.logger.info('assertFloatListAlmostEqual(): End...')       
            
        return True
            
    def assertConstrained(self, parent=None, child=None, type=None):
        ''' 
        Check if child is constrained to parent in Maya scene. 
        
        parent -- Parent transform in scene.
        child -- Child transform in scene.
        type -- parent|point|orient|scale|aim|geometry
        '''
        if self.logger: 
            self.logger.info('assertConstrained(): Start...') 
        
        const = None
        cons = cmds.listConnections(child)
        
        if not cons:
            if self.logger: 
                self.logger.error('%s not %s constrained to %s'%(child,type,parent))           
            raise AssertionError('%s not %s constrained to %s'%(child,type,parent))  
        
        for each in cons:
            if cmds.objectType(each) == type+'Constraint':
                const = each
                break
            
        cons = cmds.listConnections(const)
        for each in cons:
            if each == parent:
                if self.logger: 
                    self.logger.info('assertConstrained(): End.')                
                return True  
            
        if self.logger: 
            self.logger.error('%s not %s constrained to %s'%(child,type,parent))           
        raise AssertionError('%s not %s constrained to %s'%(child,type,parent))