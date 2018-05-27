import sys
import os
import logging
import xml.dom.minidom as xml
import shutil

#--- Import library modules
libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir)
    
from names import assets as asset_names
reload( asset_names )

#--- Import settings
import projects
reload( projects )

import users
reload( users )

class Create(object):
    '''
    Create an Asset:
    - Add name to proj_names.xml
    - Create Directories
    - Create Stub files
    - Create MataData xml files
    '''
    def __init__(self, **keywords):
        '''
        Initialize
        '''
        #--- Determine how much feedback in log file
        if keywords.has_key('v'):
            self.verbosity = keywords['v']
        else:
            # Default. Higher verbosity reveals more info in log file. 1 - 5
            self.verbosity = 1

        #--- Setup logging
        self.logger = logging.getLogger(__name__)
        cwd = os.path.dirname(__file__)
        fh = logging.FileHandler(os.path.join(cwd,'Create.log'),'w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        self.successMsg = 'Created asset successfully.'
        self.failMsg = 'Failed to create asset.'
        
        self.logger.debug('Create(): __init__()')
        
    def main(self, **keywords):
        '''
        Create an Asset:
        - AssetLib stub files
        - Unity stub files
        - MetaData files
        '''
        self.logger.debug('_main(): Starting...')
        
        # Define return data status as fail initially
        rData = {'AssetLibStubs':self.failMsg,
                'UnityLibStubs':self.failMsg,
                'MetaData':self.failMsg}
        
        # Get data from caller
        expectedKeywords = ['project',
                            'unityPath',
                            'assetLibPath',
                            'user',
                            'name', 
                            'description', 
                            'typ', 
                            'subType']
        
        for word in expectedKeywords:
            if not keywords.has_key(word):
                self.logger.error( '_main(): %s'%self.failMsg )
                return rData

        # Store keywords data
        project = keywords[expectedKeywords[0]]
        unityPath = keywords[expectedKeywords[1]]
        assetLibPath = keywords[expectedKeywords[2]]
        user = keywords[expectedKeywords[3]]
        name = keywords[expectedKeywords[4]]
        description = keywords[expectedKeywords[5]]
        typ = keywords[expectedKeywords[6]]
        subType = keywords[expectedKeywords[7]]
        
        # Validate input
        if project not in projects.projects.keys():
            self.logger.error( '_main(): Invalid project: %s'%project )
            return rData
        if user not in users.users:
            self.logger.error( '_main(): Invalid user: %s'%user )
            return rData
        if typ not in asset_names.types:
            self.logger.error( '_main(): Invalid type: %s'%typ )
            return rData
        
        # Set intial statuses to fail
        lib_stubs_status = False
        unity_stubs_status = False
        meta_status = False
        
        #-- Create AssetLib stub files
        lib_stubs_status = self.createAssetLibStubFiles( project,
                                                     assetLibPath,
                                                     name,
                                                     typ )
        
        #-- Create Unity stub files
        unity_stubs_status = self.createUnityStubFiles( project,
                                                     unityPath,
                                                     name,
                                                     typ)
        
        #-- Create MetaData stub files
        meta_status = self.createMetaDataFiles( project,
                                                assetLibPath,
                                                name,
                                                typ )
        
        # Set return status values
        if lib_stubs_status:
            rData['AssetLibStubs'] = self.successMsg
        if unity_stubs_status:
            rData['UnityLibStubs'] = self.successMsg
        if meta_status:
            rData['MetaData'] = self.successMsg
        
        # Fin!
        self.logger.debug('_main(): End.')
        return rData
    
    def createAssetLibStubFiles(self, project, assetPath, name, typ):
        '''
        Make directories and create stub files for an animation or asset 
        '''
        
        path = os.path.join(assetPath, typ, name)
        
        if os.path.isdir(path):
            self.logger.error('Directory already exists: %s'%path)
            raise Exception('Directory already exists: %s'%path)
       
        #--- Make directories
        try:
            if '$ASSETLIB' in path:
                path = path.replace('$ASSETLIB',os.environ['ASSETLIB'])
            elif '$REPOSDIR' in path:
                path = path.replace('$REPOSDIR',os.environ['REPOSDIR'])

            animPath = None
            if 'anim' in typ:
                # Animation
                animPath = self._getAnimDir(project=project, path = assetPath, name = name, typ = typ)
                shutil.os.makedirs(animPath)
                self.logger.info('Created Directory: %s'%animPath)
                
                self._makeDir(path=animPath,dirName='fbx' )
                self._makeDir(path=animPath,dirName='meta' )
                self._makeDir(path=animPath,dirName='playblasts' )
                self._makeDir(path=animPath,dirName='notes' )
                self._makeDir(path=animPath,dirName='reference' )
                
            else:
                self._makeDir(path=path,dirName='model' )
                self._makeDir(path=path,dirName='rig' )
                self._makeDir(path=path,dirName='texture' )
                self._makeDir(path=path,dirName='concept' )
                self._makeDir(path=path,dirName='fbx' )
                self._makeDir(path=path,dirName='meta' )
                self._makeDir(path=path,dirName='reference' )
                self._makeDir(path=path,dirName='notes' )
                self._makeDir(path=path,dirName='reports' )
                self._makeDir(path=path,dirName='unity_proj' )
                
        except Exception,e:
            if animPath:
                self.logger.error('Error creating animation asset directories: %s'%path)
                self.logger.error(e)  
            else:
                self.logger.error('Error creating asset directories: %s'%path)
                self.logger.error(e)
            raise Exception(e) 
        
        #--- Create stub files
        stubsPath = os.path.join(os.environ['REPOSDIR'], '/artpipeline/library/stub_files')
        try:
            if animPath:
                shutil.copyfile(os.path.join(stubsPath,'anim_stub.ma'),
                                os.path.join(animPath, '%s_%s.ma'%(name,typ)))
            else:
                shutil.copyfile(os.path.join(stubsPath,'model_stub.ma'),
                                os.path.join(path,typ,name,'texture','%s.ma'%name))
                
                shutil.copyfile(os.path.join(stubsPath,'texture.png'),
                                os.path.join(path,typ,name,'texture','%s_diffuse.png'%name))
                shutil.copyfile(os.path.join(stubsPath,'texture.png'),
                                os.path.join(path,typ,name,'texture','%s_normal.png'%name))
                shutil.copyfile(os.path.join(stubsPath,'texture.png'),
                                os.path.join(path,typ,name,'texture','%s_specular.png'%name))
                shutil.copyfile(os.path.join(stubsPath,'texture.psd'),
                                os.path.join(path,typ,name,'texture','%s_texture.psd'%name))                
                
                shutil.copyfile(os.path.join(stubsPath,'stub.xml'),
                                os.path.join(path,typ,name,'meta','concept_info.xml'))
                shutil.copyfile(os.path.join(stubsPath,'stub.xml'),
                                os.path.join(path,typ,name,'meta','model_info.xml'))
                shutil.copyfile(os.path.join(stubsPath,'stub.xml'),
                                os.path.join(path,typ,name,'meta','texture_info.xml'))
                shutil.copyfile(os.path.join(stubsPath,'stub.xml'),
                                os.path.join(path,typ,name,'meta','rig_info.xml'))      
                shutil.copyfile(os.path.join(stubsPath,'stub.xml'),
                                os.path.join(path,typ,name,'meta','export_info.xml'))
        except Exception,e:
            self.logger.error('Error creating asset files: %s'%path)
            self.logger.error(e)
            raise Exception(e)
        
        return True
                
    def _makeDir(self,path=None,dirName=None ):
        try:
            shutil.os.makedirs(os.path.join(path,dirName))
            self.logger.info('Created Directory: %s'%(os.path.join(path,dirName)))
        except Exception,e:
            self.logger.error('Failed to create directory: %s'%(os.path.join(path,dirName)))
            raise Exception(e)
            
        
    def createUnityStubFiles(self, project, unityPath, name, typ):
        ''' Create unity stub files '''
        self.logger.debug('createUnityStubFiles(): Starting...')
        
        if 'anim' in typ:
            anim_stub = os.path.join(os.environ['REPOSDIR'],'artpipeline/library/stub_files/anim_stub.fbx')
            anim_path = self._getAnimDir(unity=True,
                                         project=project,
                                         path=unityPath,
                                         typ=typ,
                                         name=name)
            
            shutil.os.makedirs(anim_path)
            self.logger.debug('Created Directory: %s'%anim_path)   
            
            shutil.copyfile(anim_stub, os.path.join(anim_path, name + '_' + typ + '.fbx'))
            self.logger.debug('Created File: %s'%anim_path) 
            self.logger.debug('createUnityStubFiles(): End.')
            return True
        
        asset_stub = os.path.join(os.environ['REPOSDIR'],'artpipeline/library/stub_files/asset_stub.fbx')
        asset_path = os.path.join(unityPath,name)+'_rig'
        
        shutil.os.makedirs(asset_path)
        self.logger.debug('Created Directory: %s'%asset_path)   
        
        shutil.copyfile(asset_stub, os.path.join(asset_path, name + '.fbx'))
        self.logger.debug('Created File: %s'%asset_path) 
        self.logger.debug('createUnityStubFiles(): End.')
        return True
    
    def createMetaDataFiles(self,
                            project,
                            assetLibPath,
                            name,
                            typ ):
        '''
        Create asset meta directory and files for tracking the asset meta data.
        Only exist in assetLibPath, not unityPath.
        '''
        self.logger.debug('createMetaDataFiles(): Starting...')
  
        if 'anim' not in typ:
            # Create _info.xml file
            for component in ['concept','model','texture','rig']:
                try:
                    self._createFile( os.path.join(assetLibPath,typ,name,'meta'), '%s_info.xml'%component )
                    self.logger.debug('createMetaDataFiles(): End: Created: %s_info.xml'%component)
                except:
                    self.logger.error('createMetaDataFiles(): End: Failed creating: %s_info.xml'%component)
                    return False
            return True
        else:
            # Create anim_info.xml
            try:
                self._createFile( self._getAnimDir(project,assetLibPath,typ,name),'meta', 'anim_info.xml' )  
                self.logger.debug('createMetaDataFiles(): End: Created: anim_info.xml')
                return True
            except:
                self.logger.error('createMetaDataFiles(): End: Failed creating: anim_info.xml')
                return False
        self.logger.debug('createMetaDataFiles(): Did not create any xml files.')
        return False
            
    def _getAnimDir(self,
                    unity=False,
                    project=None,
                    path=None,
                    typ=None,
                    name=None):
        '''
        Given args, return the path for the animation asset.
        unity: If True, returns Unity project path. False returns AssetLib path.
        '''
        self.logger.debug('_getAnimDir(): Starting...')
        
        if not unity:
            if typ == 'biped_animclip':
                return os.path.join(path,project,'animation/biped/library/clip',name)
            if typ == 'biped_animcycle':
                return os.path.join(path,project,'animation/biped/library/cycle',name)
            if typ == 'biped_animpose':
                return os.path.join(path,project,'animation/biped/library/pose',name)
            
            if typ == 'quad_animclip':
                return os.path.join(path,project,'animation/quad/library/clip',name)
            if typ == 'quad_animcycle':
                return os.path.join(path,project,'animation/quad/library/cycle',name)
            if typ == 'quad_animpose':
                return os.path.join(path,project,'animation/quad/library/pose',name)
            
            if typ == 'object_animclip':
                return os.path.join(path,project,'animation/object/library/clip',name)
            if typ == 'object_animcycle':
                return os.path.join(path,project,'animation/object/library/cycle',name)
            if typ == 'object_animpose':
                return os.path.join(path,project,'animation/object/library/pose',name)
        else:
            return os.path.join(path,'animation',name)
        
        self.logger.debug('_getAnimDir(): End.')
        
    def _createFile(self, assetLibPath, name):
        ''' Only create file if it doesn't exist '''
        self.logger.debug('_createFile(): Starting...')
        
        fileName = os.join(assetLibPath,name)
        if not os.path.isfile(fileName):
            f = open( fileName, 'w')
            f.write()
            f.close()
            
        self.logger.debug('_createFile(): End.')
    