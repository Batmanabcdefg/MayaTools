'''
Create rig GUI for selected vks fk control
'''
import pymel.core as pm
from functools import partial

# Display window 
class vks_fk_gui():
    def __init__(self):
        self.crvs = []
        self.count = 0
        self._getControls()
        self.ui()
        
    
    def ui(self):
        if not len(self.crvs):
            return
        
        win = "%s_UI" % self.crvs[0].split('_')[0]
        if(pm.window(win, exists=True)):
            pm.deleteUI(win, window=True)
    
        pm.window(win,title=win, rtf=True)
        pm.columnLayout()
        
        self.names = []
    
        for crv in self.crvs[1:]:
            self.count += 1
            pm.rowLayout(nc=2)
            pm.button(l=crv.name(), 
                      c=partial(self._tglSelect, 
                                crv.name()), 
                      w=200)
            pm.button(l='Reset', 
                      c=partial(self._reset, 
                                crv.name()), 
                      w=50)
            pm.setParent('..')
            self.names.append(crv.name())
            
        pm.rowLayout(nc=2)
        pm.button(l='Select All', 
                  c=self._selectAll, 
                  w=200)
        pm.button(l='Reset All', 
                  c=self._resetAll, 
                  w=50)
        pm.setParent('..')        
    
        pm.showWindow(win)
        
    def _getControls(self):
        sel = pm.ls(sl=1)
        if not len(sel):
            pm.warning('Please select an fk control.')
            return
        
        orig = sel
        
        # Get base control
        p1 = sel[0].getParent()
        p2 = p1.getParent()
        baseCnt = p2.getParent()
        
        # Get control curves
        pm.select(baseCnt, r=1, hi=1)
        sel = pm.ls(sl=1)
        for each in sel:
            try:
                if each.getChildren()[0].type() == 'nurbsCurve':
                    self.crvs.append(each)
            except:
                pass
        pm.select(orig, r=1)
    
    def _tglSelect(self, name=None, *args):
        pm.select(name, tgl=1)
        
    def _reset(self, name=None, *args):
        obj = pm.PyNode(name)
        num = name.split('_')[-1]
        if num == self.count:
            obj.position.set(10)
        elif num == 1:
            obj.position.set(0)
        else:
            obj.position.set((float(num)-1) * (10.0/(self.count-1)))
            
        obj.falloff.set(2)
        obj.rx.set(0)
        obj.ry.set(0)
        obj.rz.set(0)
        
    def _resetAll(self, *args):
        for name in self.names:
            self._reset(name=name)
    
    def _selectAll(self, *args):
        pm.select(clear=1)
        for name in self.names:
            self._tglSelect(name=name)
    
if __name__ == '__main__':
    vks_fk_gui()