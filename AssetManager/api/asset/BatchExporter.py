from functools import partial
import os
import shutil
import sys
import logging
import pymel.core as pm
from itertools import chain
import pdb

# /Applications/Autodesk/maya2011/Maya.app/Contents/bin/mayapy

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

cwd = os.path.dirname(os.path.abspath(__file__))

if cwd not in sys.path:
    sys.path.append(cwd)

import Export as Export
reload( Export )

class BatchExporter(object):
    '''
    Export entire Asset directory of:
    - Animations
    - Outfits
    - Cameras
    - Rigs
    
    Export to AssetLib FBX directory
    Export to given Unity path
    '''
    def __init__(self, **keywords):
        pymelLogger.debug('BatchExporter(): Initialized.')
        
    def exportAnim(self, fileName=None, assetPath=None, unityPath=None, ignore=None):
        ''' Export rig and/or prop animation from a .ma animation file as .fbx. '''
        pymelLogger.debug('exportAnim(): Starting...')
        exporter = Export.Export()
        #pdb.set_trace()
        if not os.path.isfile(fileName):
            msg = 'File does not exist: %s'%fileName
            pymelLogger.error(msg)
            raise Exception(msg)
        
        # Open the file
        pm.openFile(fileName, f=True)
        pymelLogger.debug('exportAnim(): Opened file: %s'%fileName)
        
        # Export the animation
        results = exporter.exportAnim(fileName=fileName, 
                                      assetPath=assetPath, 
                                      unityPath=unityPath,
                                      ignore=ignore)
        
        pymelLogger.debug('exportAnim(): End.')        
        return results
    
    def batchExportAnims(self, directory=None, unityPath=None):
        ''' Export rig and/or prop animation from a directories .ma files as .fbx. '''
        pymelLogger.debug('batchExportAnims(): Starting...')
        
        if not os.path.isdir(directory):
            msg ='batchExportAnims(): %s is not a valid directory'%directory
            pymelLogger.debug(msg)
            raise Exception(msg)
        
        results = []
        for root,dirs,files in os.walk(directory):
            for f in files:
                if '.svn' in root: 
                    #pymelLogger.debug('batchExportAsset(): Skipping directory: %s'%root)                
                    continue
                if 'incrementalSave' in root: 
                    #pymelLogger.debug('batchExportAsset(): Skipping directory: %s'%root)                 
                    continue
                if f.endswith('.ma'):
                    fileName = os.path.join(root,f)
                    results.append( self.exportAnim(fileName=fileName, assetPath=os.path.dirname(fileName)+'/fbx',unityPath=unityPath) )
        pymelLogger.debug('batchExportAnims(): End.')
        results = list(chain.from_iterable(results))
        results = list(chain.from_iterable(results))
        
        for each in results:
            pymelLogger.debug('Batch Exported: %s'%os.path.basename(each))
            
        return results
    
    def exportAsset(self, fileName=None, assetPath=None, unityPath=None, ignore=None):
        ''' Export Assets from a .ma animation file as .fbx. '''
        pymelLogger.debug('exportAsset(): Starting...')
        
        exporter = Export.Export()
        
        if not os.path.isfile(fileName):
            msg = 'File does not exist: %s'%fileName
            pymelLogger.error(msg)
            raise Exception(msg)
        
        # Open the file
        pm.openFile(fileName, f=True)
        pymelLogger.debug('exportAsset(): Opened file: %s'%fileName)
        
        # Export the Asset
        results = None
        results = exporter.exportAsset(fileName=fileName, 
                                       assetPath=assetPath, 
                                       unityPath=unityPath,
                                       ignore=ignore)
           
        if not results:
            msg = 'exportAsset(): Nothing exported!'
            pymelLogger.error(msg)
            raise Exception(e)
        for each in results:
            pymelLogger.debug('Exported: %s'%os.path.basename(each))
            
        pymelLogger.debug('exportAsset(): End.')        
        return results
    
    def batchExportAssets(self, directory=None, unityPath=None):
        ''' Export all assets found in the given directory. '''
        pymelLogger.debug('batchExportAsset(): Starting...')
        
        if not os.path.isdir(directory):
            msg ='batchExportAsset(): %s is not a valid directory'%directory
            pymelLogger.debug(msg)
            raise Exception(msg)
        
        results = []
        for root,dirs,files in os.walk(directory):
            if '.svn' in root: 
                #pymelLogger.debug('batchExportAsset(): Skipping directory: %s'%root)                
                continue
            if 'incrementalSave' in root: 
                #pymelLogger.debug('batchExportAsset(): Skipping directory: %s'%root)                 
                continue
            if 'rig' in root:
                for f in files:
                    if f.endswith('.ma'):
                        results.append( self.exportAsset(fileName = os.path.join(root,f), 
                                                         assetPath = root.replace('rig','fbx'),
                                                         unityPath = unityPath) )
        
        pymelLogger.debug('batchExportAsset(): End.')
            
        return results

    