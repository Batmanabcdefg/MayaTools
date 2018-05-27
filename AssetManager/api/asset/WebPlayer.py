import os
import logging
from tempfile import mkstemp
from shutil import move

  
class WebPlayer(object):
    '''
       Description:
       Modifies a webplayer template html that will
       import the bundle called

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
        fh = logging.FileHandler(os.path.join(cwd,'WebPlayer.log'),'w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh) 
        
        self.logger.debug('WebPlayer(): __init__()')

        # path to webplayer html template
        self.webPlayerDir = os.path.join( os.environ['REPOSDIR'], 'artpipeline', 'templates', 'unity', 'web' )
        self.reposDir = os.environ['REPOSDIR']
        

    def _open_replace_template(self, textToReplace=None, relativePath=None, webPlayerTemplate=None, webPlayerIndex=None):
        """ opens file, writes path to bundle and saves
        """
        self.logger.debug('WebPlayer(): _open_replace_template(): Opening and writing to file...')
    
        newFile = open( webPlayerIndex,'w')
        templateFile = open( webPlayerTemplate )
        for line in templateFile:
            newFile.write(line.replace( textToReplace, relativePath ))
        newFile.close()
        templateFile.close()

        return True
    
    def _check_bundle_exists(self, pathToBundle=None):
        """ Checks if bundle exists """
        pathToFile = os.path.join( self.reposDir, pathToBundle )
        if os.path.exists(pathToFile):
            return True
        else: 
            return False
        
    def createHtmlIndex( self, pathToBundle = True ):
        """
            User needs to pass the path to the bundle from the assetlib
            example 'AssetLib/startrek/clothing/outfit_cadet_male_01/bundle/bundleName.assetBundle'
        """
        self.logger.debug('WebPlayer(): Start ...')
        textToReplace = 'REPLACEME'
        relativePath = '../../../../' + pathToBundle

        webPlayerTemplate = os.path.join( self.webPlayerDir,'template.html' )
        webPlayerIndex = os.path.join( self.webPlayerDir,'index.html' )
        
        if self._check_bundle_exists( pathToBundle ):
            
            if self._open_replace_template(textToReplace = textToReplace, relativePath = relativePath, webPlayerTemplate=webPlayerTemplate,webPlayerIndex=webPlayerIndex):
                return webPlayerIndex
                self.logger.debug('WebPlayer(): createHtmlIndex(): HTML file created ...')
            else:
                return False
                self.logger.debug('WebPlayer(): createHtmlIndex(): Problem Creating HTML file ...')
        else:
            return False
            self.logger.debug('WebPlayer(): createHtmlIndex(): Path to bundle not correct ...')
   