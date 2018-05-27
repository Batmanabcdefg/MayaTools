import sys
import os
import logging

libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir) 
    
# Set the env to english
os.environ['LANG'] = 'en_US'

# Setup logging
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
for handler in LOGGER.handlers:
    LOGGER.removeHandler(handler)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s: %(message)s')
ch.setFormatter(formatter)
LOGGER.addHandler(ch)
      
import tmxml.tmxml as tmXml
 

class GetData(object):
    '''
    Description:
    Gets requested data from asset.xml file.
    
    Things user can do ask for:
        - GetAssetNames from project names file
        - GetAssetSummary return dict with info
        
        - GetFiles {'concept':[], model,texture,rig}
        - GetLastCommit ?? svn command
        - GetIcon project /  assetname  
        
        - GetAssignee
        - GetNotes
        - GetStatus
        - GetLastExported

    '''
    def __init__(self, **keywords):
        '''
        Initialize
        '''
        #--- Setup logging
        self.logger = LOGGER
        self.logger.debug('GetData(): __init__()')

        # xml object
        self.xmlObj = tmXml.tmXml()
        
    def allData(self, xmlFile = None):
        ''' return all data for asset as dictionary '''
        data = {}
        data['notes'] = self.getValue(typ='note', filePath=xmlFile)
        data['status'] = self.getValue(typ='status', filePath=xmlFile)
        data['assignee'] = self.getValue(typ='assignee', filePath=xmlFile)
        data['lastExported'] = self.getValue(typ='lastExported', filePath=xmlFile)
        data['project'] = self.getValue(typ='project', filePath=xmlFile)
        data['name'] = self.getValue(typ='name', filePath=xmlFile)
        data['type'] = self.getValue(typ='type', filePath=xmlFile)
        return data

    def _check_metaFile_exists(self, filePath=None):
        """ checks if file exists in the 
            system before performing any operation 
        """
        self.logger.debug('GetData(): _check_metaFile_exists(): Checking if file exists...')
        if os.path.exists( filePath ): return True
        else: return False
    
    def getValue(self, typ=None, filePath=None):
        """ """
        if self._check_metaFile_exists( filePath ):

            # getting xmlFile
            xmlFile = self.xmlObj.readXml( filePath )
            
            # check if user wants to get assignee, status, lastExported or notes
            if typ == 'assignee' or typ == 'status' or typ == 'lastExported' or typ == 'project' or typ=='name' or typ=='type':
                # open xml
                
                currentNodeValue = xmlFile.getElementsByTagName( typ )[0]
                currentValue = self.xmlObj.getTagValue( currentNodeValue ) 
                
                return currentValue
            
            elif typ == 'note':
                notes = self._get_notes_from_xml( xmlFile )
                if notes:
                    msg = 'Got notes from xml file'
                    #self.logger.error(msg)
                    #self.logger.debug('GetData(): getValue(): Got Notes from xml.')
                    return True

            else: 
                msg = 'Value passed is not valid'
                #self.logger.error(msg)
                return False

        msg = 'File: %s does not exist'%filePath
        self.logger.error(msg)
        self.logger.debug('GetData(): getValue(): End.')
        return False

    
    def _get_notes_from_xml(self, xmlFile = None):
        """ gets notes from xml """
        notesList = []
        notes = xmlFile.getElementsByTagName('note')
        for note in notes:
            notesDict = {}
            dateCreated = note.attributes['dateCreated'].value
            createdBy = note.attributes['createdBy'].value
            noteTxt = self.xmlObj.getTagValue( note )
            notesDict['dateCreated'] = dateCreated
            notesDict['createdBy'] = createdBy
            notesDict['note'] = noteTxt
                    
            notesList.append(notesDict)
        self.logger.debug('GetData(): _get_note_from_xml(): Got notes from xml ...')
        return notesList