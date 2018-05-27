import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import shutil

from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(pm.logging.DEBUG)

libDir = os.environ['REPOSDIR']+'/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir)

from names import rigs as rig_names
reload( rig_names )
from names import assets as asset_names
reload( asset_names )
from names import cameras as cam_names
reload( cam_names )

import os
import pdb

class Export(object):
    
    def __init__(self):
        '''
        Export asset/rig/animation/camera as FBX
        to AssetLib and Unity directory.
        '''
        self.rootList = rig_names.rootList
        self.assetTypes = asset_names.types
        self.camNames = cam_names.shot_cam_names
        self.geo = 'geo'
        self.custom = 'custom'
        pymelLogger.debug('Initializing...')

    def exportAnim( self, fileName=None, assetPath=None, unityPath=None, ignore=None ):
        '''
        Export animation for each rig found in the current scene.
        Export camera with name from names.cameras.shot_cam_names list
        Rig must be referenced.
        '''
        pymelLogger.debug('exportAnim(): Starting...')
        
        # Export to directory wih animation file name
        # Assets/art/animation/anim_type/anim_name
        try:
            fName = os.path.basename(fileName)[:-3]
            typ = fName.split('_')[-2:]
            typ = typ[0] + '_' + typ[1]
            dirName = fName.split('_')[:-2]
            dName = ''
            for each in dirName:
                dName += each + '_'
            dirName = dName[:-1]
            unityPath = unityPath + '/animation/' + typ + '/' + dirName            
        except Exception,e:
            pymelLogger.error('exportAnim(): Error creating UnityPath.')
            pymelLogger.error(e)
            raise Exception(e) 
        
        pymelLogger.debug('File name: %s'%fileName)
        pymelLogger.debug('Asset path: %s'%assetPath)
        pymelLogger.debug('Unity path: %s'%unityPath)

        # Make AssetLib fbx / Unity directories if they do not exist
        try:
            if not os.path.isdir( assetPath ):
                os.makedirs( assetPath )
            if not os.path.isdir( unityPath ):
                os.makedirs( unityPath )
        except Exception,e:
            pymelLogger.error('exportAnim(): Error creating directory.')
            pymelLogger.error(e)
            raise Exception(e)        
        
        # Validation
        if not os.path.isfile(fileName):
            msg = 'exportAsset(): fileName: %s is invalid.'%fileName
            pymelLogger.debug(msg)
            raise Exception(msg)
        
        # Delete all layers (clean up process)
        self._delAllLayers()  

        # Check for known rigs.
        exportedRig = False
        results = []
        for rigL in self.rootList:
            try:
                try:
                    # Try to select root with a namespace
                    pymelLogger.debug('Trying: "*:%s" '%rigL)
                    pm.select( '*:'+ rigL, r=1)
                    roots = pm.ls(sl=1)
                except:
                    # Try to select root with two namespaces (prop referenced nto set)
                    pymelLogger.debug('Trying: "*:*:%s" '%rigL)
                    pm.select( '*:*:'+ rigL, r=1)
                    roots = pm.ls(sl=1)  
            except:
                # Skip this root
                pymelLogger.debug('Did not find "%s" in scene.'%rigL)
                continue
                
            # Export all selected roots
            ns = None
            for root in roots:
                ns = root.split(':')
                # Select the namespace just before the name if two or more are found
                if len(ns) == 2:
                    ns = ns[0]
                elif len(ns) > 2:
                    ns = ns[-2]
                pm.select(root, r=1)
                self._importRefDeleteNS()
                self._bakeAnim( root )
                if ns:
                    result = self._fbxExport( selection=root, 
                                             fileName=fileName,
                                             prefix=ns, 
                                             assetPath=assetPath, 
                                             unityPath=unityPath,
                                             anim=True )
                else:
                    msg = 'Rig has no namespace. Make sure it is referenced. Nothing exported.'
                    pymelLogger.error(msg)
                    raise Exception(msg)
                
                if result:
                    results.append(result)
                    exportedRig = True
                    pm.delete(root)
                else:
                    pymelLogger.error('FBX did not export for "%s:%s"'%(ns,root))
            
        if not exportedRig:
            msg = 'No Rigs in the scene to be exported!'
            cmds.warning( msg )
            pymelLogger.warning( msg )

        # Export camera(s)
        exportedCam = False
        for c_name in self.camNames:
            try:
                # Try to select camera
                pymelLogger.debug('Trying: "%s" '%c_name)
                pm.select( c_name, r=1)
                cameras = pm.ls(sl=1)
            except Exception,e:
                # Skip this camera name
                pymelLogger.debug('Did not find "%s" in scene.'%c_name)
                pymelLogger.debug(e)
                continue 

            # Export all cameras
            for cam in cameras:
                pm.select(cam, r=1)
                self._bakeAnim( cam )
                result = self._fbxExport( selection=cam, 
                                         fileName=fileName,
                                         prefix=cam, 
                                         assetPath=assetPath, 
                                         unityPath=unityPath,
                                         anim=True,
                                         camera=True )
                
                if result:
                    results.append(result)
                    exportedCam = True
                else:
                    pymelLogger.error('FBX did not export: "%s"'%(cam))
            
        if not exportedCam:
            msg = 'No Cameras in the scene to be exported!'
            cmds.warning( msg )
            pymelLogger.error( msg )
            
        # Log results
        for lst in results:
            for fName in lst:
                pymelLogger.debug('Exported: %s'%(fName))
                
        pm.cmds.file(newFile=1,f=1)
                
        return results
                    
    def exportRig(self):
        """ will export SH and Geo found in the geo folder """
        # rig and geo should not be referenced
        # find SH, delete constraints, parent to world
        # find geo folder parent to world
        # select SH and geo folder and export as fbx to fbx folder
        pymelLogger.debug( 'Starting rig export' )
        export = 0
        for rig in self.rootList:
            if cmds.objExists(rig): 
                # check if geo folder also exists
                if cmds.objExists(self.geo):
                    self._delConstraints(rig)  
                    cmds.parent(rig, w=1)
                    cmds.parent(self.geo, w=1)
                    cmds.select(rig,self.geo, r=1)
                    #print rig, self.geo
                    if self._fbxExport( 2 ):
                        cmds.confirmDialog(m='FBX Rig Exported', button='Ok')
                    pymelLogger.debug( 'Finished rig export' )
                    export = 1
                    break
                else: 
                    pymelLogger.error( 'No geo folder has been found' )
        if export == 0 : pymelLogger.error( 'No Rig Exported. Note: Referenced Rigs Will Not Export' )
            
    def exportAsset(self, fileName=None, assetPath=None, unityPath=None, ignore=None):
        """ Export 'custom' group geo and SH skeleton. """
        pymelLogger.debug('Starting: exportAsset()...')

        # Export to directories with type and asset file name
        print unityPath
        print assetPath
        found = False
        for typ in self.assetTypes:
            platform = sys.platform
            if 'win' in platform:
                #pathElems = assetPath.split(os.sep)
                pathElems = assetPath.split('/')
                
            else:
                if '/' in assetPath:
                    pathElems = assetPath.split('/')
                else:
                    pathElems = assetPath.split('\\')
                
            if typ in pathElems:
                pymelLogger.debug('exportAsset(): Type: %s'%typ)
                unityPath = unityPath + '/%s/'%typ + os.path.basename(assetPath[:-4])
                found = True
                break
            
        if not found:
            msg = 'exportAsset(): Asset is not in a directory named after a type.'
            pymelLogger.error(msg)
            raise Exception(msg)
        
        pymelLogger.debug('File name: %s'%fileName)
        pymelLogger.debug('Asset path: %s'%assetPath)
        pymelLogger.debug('Unity path: %s'%unityPath)
        
        # Make AssetLib fbx / Unity directories if they do not exist
        try:
            if not os.path.isdir( assetPath ):
                os.makedirs( assetPath )
            if not os.path.isdir( unityPath ):
                os.makedirs( unityPath )
        except Exception,e:
            pymelLogger.error('exportAsset(): Error creating directory.')
            pymelLogger.error(e)
            raise Exception(e)
        
        # Validation
        if not os.path.isfile(fileName):
            msg = 'exportAsset(): fileName: %s is invalid.'%fileName
            pymelLogger.debug(msg)
            raise Exception(msg)
        
        #--- Rigged to Character asset
        results = None
        for rig in self.rootList:
            pymelLogger.debug('exportAsset(): Checking for root: %s'%rig)
            try:
                try:
                    pm.select( '*:'+rig, r=1 )
                except:
                    try:
                        pm.select( rig, r=1 )
                    except Exception,e:
                        pymelLogger.error('%s'%e)
                        raise Exception(e)
                    pymelLogger.warning('%s has no Namespace'%rig)
                root = pm.ls(sl=1)[0]
                if root:
                    # Select custom group
                    try:
                        pm.select('*:custom', r=True)
                        customGrp = pm.ls(sl=1)[0]
                    except:
                        msg = 'Did not find referenced "custom" group. Nothing exported.'
                        pymelLogger.error(msg)
                        raise Exception(msg)
                    
                    # Prep SH for export
                    try:
                        pm.select(root,r=1)
                        #if root != 'Reference':
                        self._importRefDeleteNS()
                        self._delConstraints(root)
                        pm.parent( root,w=1 )
                        pymelLogger.debug('Prepared SH skeleton for export.')
                    except Exception,e:
                        msg = 'Failed to prepared "%s" for export.'%root
                        pymelLogger.error(msg)
                        pymelLogger.error(e)
                        raise Exception(msg+'\n'+e)         
                    
                    # Prep custom group for export
                    try:
                        pm.select(customGrp,r=1)
                        self._importRefDeleteNS()
                        try: pm.parent( customGrp,w=1 )
                        except: pass
                        pymelLogger.debug('Prepared "custom" group for export.')
                    except Exception,e:
                        msg = 'Failed to prepared "custom" group for export.'
                        pymelLogger.error(msg)
                        pymelLogger.error(e)
                        raise Exception(msg+'\n'+e)
                    
                    # Delete rig geo folder to avoid conflicts
                    try: 
                        if cmds.objExists(self.geo):
                            pm.delete(self.geo)
                    except: 
                        msg = 'Failed to delete rig "geo" group.'
                        pymelLogger.error(msg)
                        raise Exception(msg)
                    
                    # Select SH and custom group and export
                    pm.select(root,customGrp,r=True)
                    #pdb.set_trace()
                    sel = pm.ls(sl=1)
                    results = self._fbxExport( selection=sel, 
                                        fileName=fileName,
                                        assetPath=assetPath, 
                                        unityPath=unityPath,
                                        asset=True)
                    if results:
                        pymelLogger.debug('exportAsset(): FBX Exported: %s and %s'%(root,customGrp))
                    else:
                        msg = 'Export failed: %s: %s and %s'%(os.path.basename(fileName),root,customGrp)
                        pymelLogger.error(msg)
                        raise Exception(e)
                else:
                    pymelLogger.warning( '%s not found in scene.'%rig )
                    break
                        
            except:
                msg = 'Did not find %s in the file.'%rig
                pymelLogger.warning(msg)
        
        #--- Prop Asset
        # @todo
        
        if results:
            pm.cmds.file(newFile=1,f=1)
            msg = 'End: exportAsset(). Export complete.'
            pymelLogger.debug(msg)  
            
            return results
        else:
            msg = 'exportAsset(): Nothing exported!'
            pymelLogger.error(msg)
            raise Exception(msg)
            
    def _fbxExport(self, selection=None, 
                  fileName=None,
                  prefix=None, 
                  assetPath=None, 
                  unityPath=None,
                  rig=False,
                  asset=False,
                  anim=False,
                  camera=False):
        '''
        Selection: Names of objects to export
        prefix: prefix@filename.ma
        assetPath: Directory to export fbx in AssetLib
        unityPath: Directory to export fbx for unity
        rig/asset/anim/camera: Determine FBX options
        '''
        pymelLogger.debug('Starting: fbxExport()...' )
        pymelLogger.debug('Exporting: %s'%selection)
        pymelLogger.debug('Prefix: %s'%prefix)
        pymelLogger.debug('Asset path: %s'%assetPath)
        pymelLogger.debug('Unity path: %s'%unityPath)
        
        try:
            pm.parent(selection,w=True)
        except:
            pm.select(selection,r=1)
        
        # Determine export file name
        if prefix:
            fileN = os.path.basename(fileName)[:-3]
            fileN = prefix+'@'+fileN+'.fbx'
        else:
            fileN = os.path.basename(fileName)[:-3]
            fileN = fileN + '.fbx'
        pymelLogger.debug('fileN: %s'%fileN)
        
        # Place file in fbx folder in proper location
        # anim/typ=1 and rig have a different folder structure
        unityFile = unityPath + '/' + fileN
        assetFile = assetPath + '/' + fileN
        pymelLogger.debug('unityFile: %s'%unityFile)
        pymelLogger.debug('assetFile: %s'%assetFile)

        startFrame = int( cmds.playbackOptions(q=1, min=1) )
        endFrame = int( cmds.playbackOptions(q=1, max=1) )        
        
        # FBX OPTIONS!
        # Geometry
        mel.eval("FBXExportSmoothingGroups -v true")
        mel.eval("FBXExportHardEdges -v false")
        mel.eval("FBXExportTangents -v false")
        mel.eval("FBXExportSmoothMesh -v true")
        mel.eval("FBXExportInstances -v false")
        mel.eval("FBXExportReferencedContainersContent -v false")
        
        # Animation
        if anim:
            mel.eval("FBXExportApplyConstantKeyReducer -v true")
            mel.eval("FBXExportBakeResampleAnimation -v true")
            mel.eval("FBXExportBakeComplexAnimation -v true")
            mel.eval("FBXExportBakeComplexStart -v "+str(startFrame))
            mel.eval("FBXExportBakeComplexEnd -v "+str(endFrame))
            mel.eval("FBXExportBakeComplexStep -v 1")
            mel.eval("FBXExportUseSceneName -v false")
            mel.eval("FBXExportQuaternion -v euler")
        if asset:
            mel.eval("FBXExportShapes -v true")
            mel.eval("FBXExportSkins -v true")
            
        if camera:
            mel.eval("FBXExportCameras -v true")
        else:
            mel.eval("FBXExportCameras -v false")
            
        # Constraints
        mel.eval("FBXExportConstraints -v false")
        # Lights
        mel.eval("FBXExportLights -v false")
        # Embed Media
        mel.eval("FBXExportEmbeddedTextures -v false")
        # Connections
        mel.eval("FBXExportInputConnections -v false")
        # Axis Conversion
        mel.eval("FBXExportUpAxis y")
        # version
        mel.eval("FBXExportFileVersion FBX201100")
        # Type
        mel.eval("FBXExportInAscii -v true")
        
        # Export!
        exported = []
        mel.eval('FBXExport -f "'+ assetFile +'" -exportFormat "fbx" -s;')
        exported.append(assetFile)
        pymelLogger.debug('fbxExport(): Exported: %s'%assetFile )
        
        # Copy fbx and textures folder to unitypath
        # /fbx
        try:
            # Copy .fbx files to unity dir
            onlyfiles = [ os.path.join(assetPath+"/"+f) for f in os.listdir(assetPath) if os.path.isfile( assetPath+"/"+f) ]
            fbxs = [ f for f in onlyfiles if f.endswith('.fbx') ]
            for f in fbxs:
                fName = os.path.basename(f)
                dst = unityPath+'/fbx/'+fName
                
                dstDir = os.path.join(unityPath,'fbx')
                if not os.path.exists(dstDir):
                    print 'created!'
                    os.makedirs(dstDir)
                    
                try:
                    shutil.copy(f, dst)
                except:
                    shutil.rmtree(dst)
                    shutil.copy(f, dst)
                    
                pymelLogger.debug('fbxExport(): Copied from:%s'%f)
                pymelLogger.debug('fbxExport(): Copied to:%s'%dst)   
        except Exception,e: 
            pymelLogger.error('fbxExport(): %s'%e )
            
        # /texture      
        try:
            # Copy .fbx files to unity dir
            path = assetPath.replace('fbx','texture')
            onlyfiles = [ os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
            images = [ os.path.join(path,f) for f in onlyfiles if f[-3:] in ['png','tga'] ]

            for f in images:
                fName = os.path.basename(f)
                dst = os.path.join(unityPath,'texture',fName)
                dstDir = os.path.join(unityPath,'texture',fName)
                if not os.path.exists(dstDir):
                    os.makedirs(dstDir)
                try:
                    shutil.copyfile(f, dst)
                except:
                    shutil.rmtree(dst)
                    shutil.copyfile(f, dst)
                pymelLogger.debug('fbxExport(): Copied from:%s'%f)
                pymelLogger.debug('fbxExport(): Copied to:%s'%dst)   
                
        except Exception,e: 
            pymelLogger.error('fbxExport(): %s'%e )
        
        pymelLogger.debug('End: fbxExport().' )
        
        if len(exported):
            return exported
        return False          

    def _delAllLayers(self):
        # Get Display Layers
        layers = cmds.ls(long=True, type = 'displayLayer' )
        for layer in layers: 
            # defaultLayer can not be deleted
            if layer != 'defaultLayer':
                    try:
                        cmds.delete(layer)
                    except:
                        print 'Layer Not Deleted'  
              
    def _delConstraints(self, jnt, *args):
        pm.select(jnt, hi=1, r=1)
        sel = pm.ls(sl=1)
        consList = ['parentConstraint','scaleConstraint','orientConstraint', 'pointConstraint']
        for each in sel:
            for cons in consList: 
                if each.type() == cons: pm.delete(each)


    def _importRefDeleteNS(self):
        ''' Given a selected object, import reference and delete the namespace. '''
        # only first object selected will be considered
        pymelLogger.debug('Starting: importRefDeleteNS()...')
        sel = cmds.ls(sl=1)
        if sel:
            sel = sel[0]
            ns = sel[:sel.rfind(':')]
            # finding name of the referenced node
            try:
                refNode = cmds.referenceQuery( sel, referenceNode = True )
            except:
                refNode=None
            if refNode:
                # find out if it is a reference of a reference
                topRef = cmds.referenceQuery( sel, referenceNode=True, tr=True  )
                if refNode != topRef:
                    pymelLogger.debug('importRefDeleteNS(): %s is sub-referenced.'%sel)
                    fileNameTN = cmds.referenceQuery( topRef,filename = True  )
                    fileNameN = cmds.referenceQuery( refNode, filename = True )
                    
                    cmds.file( fileNameTN , importReference = 1 )
                    cmds.file( fileNameN, importReference = 1 )
                    
                    cmds.namespace(mv=[ns,':'], force=1)
                    pymelLogger.debug('importRefDeleteNS(): %s namespace moved to ":" namespace.'%ns)
                else:
                    fileNameN = cmds.referenceQuery( refNode, filename = True )
                    cmds.file( fileNameN, importReference = 1 )
                    cmds.namespace(mv=[ns,':'], force=1)
                        
            else: 
                cmds.warning('This is Not a reference object!' )
                pymelLogger.warning('%s is not a referenced object.'%sel)
        else: 
            pymelLogger.warning('Nothing selected! Please select a referenced object.')
        pymelLogger.debug('End: importRefDeleteNS().')
                      
    def _bakeAnim(self, root):
        '''
        Given root:
        - Bake the heirarchy animation data
        - Delete constraints
        - Reset timeline to 1 if wasn't already set to 1
        - Remove root from heirarchy
        '''
        pymelLogger.debug('Starting: bakeAnim()...')
        # Getting time range from scene
        startFrame = int( pm.playbackOptions(q=1, min=1) )
        endFrame = int( pm.playbackOptions(q=1, max=1) )

        # Bake the heirarchy
        #pm.select( root, hi=1 )
        #pm.bakeResults(simulation=1, t=( startFrame, endFrame ) )
        
        # Delete constraints
        #self._delConstraints(root)
        pm.select(root,hi=1, r=1)

        # Set timeline to start at frame 1
        if startFrame != 1:
            if startFrame < 1:
                tChange = (-(startFrame))+1
            elif startFrame > 1:
                tChange = (-(startFrame-1))
        
            pm.keyframe(e=1, time=(startFrame,endFrame),relative=1, timeChange=tChange)
            pm.playbackOptions(e=1, min=1, max=endFrame+tChange )
            
        # Remove root from it's heirarchy
        #pm.select(root, r=1)
        #try:
        #    pm.parent(root, w=1)
        #except Exception,e:
        #    pymelLogger.error('_bakeAnim(): %s'%e)
        
        pymelLogger.debug('bakeAnim(): Baked anim onto %s'%root)
        pymelLogger.debug('bakeAnim(): Range baked: %s - %s'%(startFrame,endFrame))
        pymelLogger.debug('End: bakeAnim()')