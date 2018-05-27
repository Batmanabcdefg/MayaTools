#--- Add cwd and lib
cwd = os.path.dirname(os.path.abspath(__file__))
lib = cwd+'/library'
modules = cwd+'/modules'
if modules not in sys.path:
    sys.path.append(modules)
if lib not in sys.path:
    sys.path.append(lib)
    
import Names
reload( Names )
import Control
reload( Control )

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

def build():
    pymelLogger.debug('Starting: build()...') 
    
    pymelLogger.debug('End: build()...')

        