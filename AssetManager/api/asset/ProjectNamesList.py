import sys
import os
import logging
import xml.dom.minidom as xml

class ProjectNamesList(object):
    '''
    Description:
    Add a name to a projects proj_names.xml file.
    Remove name from projects proj_names.xml file.
    
    Fail if name is not unique
    Fail if name less than five characters
    Fail if name is greater then twenty characters
    Fail if name does not exist

    Add Returns:
    Pass: 'Added %s to proj_names.xml'%asset_name
    Fail: False
    
    remove Returns:
    Pass: 'Removed %s from proj_names.xml'%asset_name
    Fail: False
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
        fh = logging.FileHandler(os.path.join(cwd,'ProjectNamesList.log'),'w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh) 
        
        self.logger.debug('ProjectNamesList(): __init__()')
        
    def add(self, assetName=None, fileName=None):
            self.logger.debug('addToNames(): add(): Starting...')
            
            if self._check_unique( name=assetName, fileName=fileName ):
                if self._check_length( name=assetName ):
                    if self._add_to_xml_names( name=assetName, fileName=fileName ):
                        msg = 'Added %s to proj_names.xml'%assetName
                        self.logger.debug(msg)
                        self.logger.debug('addToNames(): add(): End.')
                        return msg
                    
                    msg = 'Name length is invalid: %s. Min=5, max=20 characters.'%assetName
                    self.logger.error(msg)
                    self.logger.debug('addToNames(): add(): End.')
                    return False
                
                msg = 'Failed to add %s to proj_names.xml'%assetName
                self.logger.error(msg)
                self.logger.debug('addToNames(): add(): End.')
                return False
            
            msg = '%s is not a unique name.'%assetName
            self.logger.error(msg)
            self.logger.debug('addToNames(): add(): End.')
            return False
        
    def remove(self, assetName=None, fileName=None):
        self.logger.debug('removeFromNames(): remove(): Starting...')
        
        if self._remove_from_xml_names( name=assetName, fileName=fileName ):
            msg = 'Removed %s from proj_names.xml'%assetName
            self.logger.debug(msg)
            self.logger.debug('removeFromNames(): remove(): End.')
            return msg
  
    def _remove_from_xml_names(self, name=None, fileName=None):
        self.logger.debug('removeFromNames(): _remove_from_xml_names(): Starting...')
        
        xmlFile = xml.parse( fileName )
        
        for node in xmlFile.childNodes[0].childNodes:
            if node.nodeType != 3:
                if node.attributes['name'].value == name:
                    xmlFile.childNodes[0].removeChild( node )
                    # open write save
                    xmlDoc = open( fileName, 'w' )                    
                    xmlDoc.write( xmlFile.toxml() )
                    xmlDoc.close()
                    self.logger.debug('removeFromNames(): _remove_from_xml_names(): Created Xml File...')
                    return True        
                
        self.logger.debug('removeFromNames(): _remove_from_xml_names(): End.')
        
    def _check_unique(self, name=None, fileName=None):
        self.logger.debug('addToNames(): _check_unique(): Starting...')
        
        names = self._read_xml_names( fileName=fileName )
        if name in names:
            self.logger.debug('addToNames(): _check_unique(): End.')
            return False
        self.logger.debug('addToNames(): _check_unique(): End.')
        return True
        
    def _check_length(self, name=None):
        self.logger.debug('addToNames(): _check_unique(): Starting...')
        
        if len(name) > 20:
            self.logger.debug('addToNames(): _check_unique(): Returned: False')
            return False
        if len(name) < 5:
            self.logger.debug('addToNames(): _check_unique(): Returned: False')
            return False
        self.logger.debug('addToNames(): _check_unique(): Returned: True')
        return True
        
    def _read_xml_names(self, fileName=None):
        self.logger.debug('addToNames(): _read_xml_names(): Starting...')
        
        xmlFile = xml.parse( fileName )
        # Get names as list
        names = []
        for node in xmlFile.getElementsByTagName('assets'): 
            names.append( node.attributes['name'].value )
       
        self.logger.debug('addToNames(): _read_xml_names(): End.')
        return names        
        
    def _add_to_xml_names(self, name=None, fileName=None):
        self.logger.debug('addToNames(): _add_to_xml_names(): Starting...')
        
        xmlFile = xml.parse( fileName )
        
        #namesTag = xmlFile.getElementsByTagName('assets')
        childName = xmlFile.createElement( 'asset' )
        childName.setAttribute( 'name' , name )
        xmlFile.childNodes[0].appendChild( childName )
        # open write save
        xmlDoc = open( fileName, 'w' )
        xmlDoc.write( xmlFile.toxml() )
        xmlDoc.close()
        self.logger.debug('addToNames(): _add_to_xml_names(): End.')
        return True

        