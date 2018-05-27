import pymel.core as pm
from functools import partial

SHELFTAB_HEIGHT = 30

class FloatingShelf(object):
    ''' Floating self in maya '''
    def __init__(self):
        self.version = '0.1'
    
    def ui(self):
        winName = 'FloatingShelfWin'
        if pm.window(winName,exists=True):
            pm.deleteUI(winName)
            
        self.win = pm.window(winName,title='Floating Shelf v%s'%self.version,
                  rtf=True)
        
        pm.columnLayout(adj=True)
        
        #--- Top Buttons
        pm.rowLayout(nc=3,adj=3,cw3=(100,100,100))
        pm.button(label='\tExit\t', 
                  c = self.exit, 
                  bgc=[1.0,0.2,0.2],
                  w=100)    
        pm.button(label='\tNew Tab\t', 
                  c = self._addTab, 
                  w=100)         
        pm.text('')
        pm.setParent( '..' )
        
        #--- Tabs
        self.mainLayout = pm.shelfTabLayout( 'mainShelfTab' , 
                                             image='smallTrash.xpm', 
                                             imageVisible=True, 
                                             imh=SHELFTAB_HEIGHT,
                                             cc=self._refreshTabs)
        self.shelfTabs = []
        sTab = pm.shelfLayout( 'General',h=SHELFTAB_HEIGHT )
        self.shelfTabs.append( sTab )
        self._createDeleteTabButton(shelfTab=sTab)
        pm.setParent( '..' )
        pm.setParent( '..' )
        
        pm.showWindow()    
        
    def exit(self,*args):
        #--- Save shelves
        self._saveSettings()
        
        #--- Delete UI
        pm.deleteUI(self.win, window=True)
    
    def _saveSettings(self,*args):
        tempDir = pm.internalVar( userTmpDir=True )
        #--- Get tabs in the layout
        for sLayout in self.shelfTabs:
            if '(Deleted)' not in sLayout:
                pm.saveShelf( shelf, (tempDir + sLayout.split('|')[-1]+'_FloatingShelf') );        
    
    def _loadSettings(Self,*args):
        pass
        #--- Get tab files
        
        #--- load to layout
        
    def _createDeleteTabButton(self, shelfTab=None, *args):
        pm.shelfButton(annotation='Delete this tab.', 
                       image1='delete-icon.xpm', 
                       label='Delete',
                       command=partial(self._deleteShelfTab,shelfTab))
    
    def _addTab(self,*args):
        #--- Prompt for name
        result = pm.promptDialog(
                    title='Tab Name',
                    message='Enter Name:',
                    button=['Ok', 'Cancel'],
                    defaultButton='Ok',
                    cancelButton='Cancel',
                    dismissString='Cancel')
        #--- Create the tab
        if result == 'Ok':
            text = pm.promptDialog(query=True, text=True)
            sTab = pm.shelfLayout( text, h=SHELFTAB_HEIGHT, parent=self.mainLayout )
            self.shelfTabs.append( sTab )
            self._createDeleteTabButton(shelfTab=sTab)
            
    def _refreshTabs(self,*args):
        ''' Created to handle 2010 issue on mac where shelfLayouts
        were growing when as you changed tabs. '''
        #--- Rest to default size
        for shelfTab in self.shelfTabs:
            if pm.shelfLayout(shelfTab, q=True, exists=True):
                pm.shelfLayout( shelfTab, e=True, h=SHELFTAB_HEIGHT )

    def _deleteShelfTab(self, shelfTab=None,*args):
        ''' Deleting shelfLayout crashes 2010, so hiding, disabling and changing name.
        When saving shelves, hidden ones will be ignored. '''
        
        if len(self.shelfTabs) == 1:
            print '\nFloatingShelf: Warning: Can not delete the last tab.',
            return
        
        if pm.shelfLayout(shelfTab, q=True, exists=True):
            # Display shelf not being deleted
            for tab in self.shelfTabs:
                if tab != shelfTab:
                    pm.tabLayout(self.mainLayout,edit=True,selectTab=tab)
                
            # Hide the shelf
            pm.shelfLayout( shelfTab, e=True, visible=False )
            pm.shelfLayout( shelfTab, e=True, enable=False )
            tabName = shelfTab.split('|')[-1]
            pm.shelfTabLayout( self.mainLayout, e=True, tabLabel=(tabName,'%s(Deleted)'%tabName) )
            index = self.shelfTabs.index(shelfTab)
            self.shelfTabs[index] = shelfTab.replace(tabName,tabName+'(Deleted)')
            
    
if __name__ == '__main__':
    x = FloatingShelf()
    x.ui()
    