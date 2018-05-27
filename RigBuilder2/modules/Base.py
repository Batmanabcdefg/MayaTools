import logging
import sys
import os

sys.path.append('../library')
sys.path.append('../../library')

from names import rigs as rigNames
reload(rigNames)
import Control as control
reload(control)

os.environ['LANG'] = 'en_US'

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
for handler in LOGGER.handlers:
    LOGGER.removeHandler(handler)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
ch.setFormatter(formatter)
LOGGER.addHandler(ch)

class Base(object):
    def __init__(self):
        ''' Base class used by all rigging modules for initial setup. '''
        self.logger = LOGGER
        self.names = rigNames
        
        