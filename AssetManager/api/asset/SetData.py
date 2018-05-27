import sys
import os
import logging
from datetime import datetime

libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir) 
      
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

import tmxml.tmxml as tmxml
 

class SetData(object):
    '''
    Description:
    Sets/Adds Passed Data to asset.xml file.
    
    Things user can pass:
        - SetAssignee
        - SetNote
        - SetStatus
        - SetLastExport

    '''
    def __init__(self, **keywords):
        '''
        Initialize
        '''
        #--- Setup logging
        self.logger = LOGGER
        
        self.logger.debug('SetData(): __init__()')

        # xml object
        self.xmlObj = tmxml.tmXml()

    def _check_metaFile_exists(self, filePath=None):
        """ checks if file exists in the 
            system before performing any operation 
        """
        self.logger.debug('SetData(): _check_metaFile_exists(): Checking if file exists...')
        if os.path.exists( filePath ): return True
        else: return False
        
    
    def _check_existing_value(self, currentValue = None, value = None):
        """ checks if user is trying to assign the same value 
        """ 
        self.logger.debug('SetData(): _check_existing_value(): Starting...') 
        if currentValue != value:
            return True
        else: return False
        self.logger.debug('SetData(): _check_existing_value(): End.') 
      
          
    def setValue(self, typ = None, value = None, filePath = None, userName = None ):
        """ verifies and calls the method to write to the xml """
        self.logger.debug('SetData(): setValue(): Starting...')
        
        if userName == None: 
            self.logger.error('SetData(): setValue(): No userName passed in.')
            return False
        
        if self._check_metaFile_exists( filePath ):
            self.logger.debug('SetData(): setValue(): _check_metaFile_exists == True')
            # check if user wants to modify/add assignee, status, lastExported or notes
            if typ == 'assignee' or typ == 'status' or typ == 'lastExported' or typ == 'project' or typ=='name' or typ=='type':
                # open xml
                xmlFile = self.xmlObj.readXml( filePath )
                currentNodeValue = xmlFile.getElementsByTagName( typ )[0]
                currentValue = self.xmlObj.getTagValue( currentNodeValue ) 
    
                if self._check_existing_value( currentValue, value ):
                    
                    if self._set_value_to_xml( typ, value, filePath ):
                        
                        msg = 'Added %s:%s to meta file'%(typ,value)
                        self.logger.debug(msg)
                        self.logger.debug('SetData(): setValue(): End.')
                        return msg         
                
                msg = 'New value equals Current value, will not write to file'
                self.logger.error(msg)
                self.logger.debug('SetData(): setValue(): End.')
                return False
            
            
            elif typ == 'note':
                if self._add_note_to_xml(value, filePath, userName):
                    msg = 'Added %s:%s to meta file'%(typ,value)
                    self.logger.error(msg)
                    self.logger.debug('SetData(): _check_metaFile_exists(): Added note to xml.')
                    return True

            else: 
                msg = 'Value passed is not valid'
                self.logger.error(msg)
                return False

        msg = 'File: %s does not exist'%filePath
        self.logger.error(msg)
        self.logger.debug('SetData(): _check_metaFile_exists(): End.')
        return False
    
    
    def _set_value_to_xml(self, typ = None, value = None, filePath = None ):
        """ writes to xml """
        xmlFile = self.xmlObj.readXml( filePath )
        
        # we need to replace the old assignee for the new one
        # we will do a basic string operation
        xmlStr = xmlFile.toxml()
        # if empty nodes will appear like <nodename/> instead of <nodename></nodename>
        if '<%s/>'%typ not in xmlStr:
            front = xmlStr.split('<%s>'%typ)[0]
            back = xmlStr.split('</%s>'%typ)[1]
            newTag = '<%s>%s</%s>'%(typ,value,typ)
            
        else:
            spl = xmlStr.split('<%s/>'%typ)
            front = spl[0]
            back = spl[1]
            newTag = '<%s>%s</%s>'%(typ,value,typ)
        
        newXml = front + newTag  + back

        # write to xml
        xmlDoc = self.xmlObj.saveXml( filePath, newXml )
        self.logger.debug('SetData(): _set_value_to_xml(): Saved to Xml File...')
        return True
    
    
    def _add_note_to_xml(self, value = None, filePath = None, userName = None ):
        """ writes to xml """
        xmlFile = self.xmlObj.readXml( filePath )
        
        dateObj = datetime.now()
        date = str(dateObj.day) + '-' + str(dateObj.month) + '-' + str(dateObj.year)
        
        nodeName = 'note'
        attrDict = { 'dateCreated':date, 'createdBy':userName }
        noteNode = self.xmlObj.createNodeWithAttrAndText( xmlFile, nodeName, attrDict, value )
 
        notesNode = xmlFile.getElementsByTagName('notes')[0] 
        notesNode.appendChild( noteNode )

        # write to xml
        xmlDoc = self.xmlObj.saveXml( filePath, xmlFile )
        self.logger.debug('SetData(): _add_note_to_xml(): Saved to Xml File...')
        return True