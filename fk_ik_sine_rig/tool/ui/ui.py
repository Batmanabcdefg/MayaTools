'''
Create rig GUI for selected rig
'''
import pymel.core as pm
from functools import partial


# Display window
class ui():
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

        pm.window(win, title=win, rtf=True)
        pm.columnLayout()

        self.names = []

        for crv in self.crvs:
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

        # Get reg_node
        reg_node = sel[0].message.listConnections()[0]
        print reg_node

        # Get control curves
        attrs = reg_node.listAttr()
        self.crvs = []
        for a in attrs:
            if 'FK_' in a.name():
                if 'top' in a.name() or 'root' in a.name():
                    continue
                else:
                    self.crvs.append(a.listConnections()[0])
            elif '_ik_' in a.name():
                self.crvs.append(a.listConnections()[0])

    def _tglSelect(self, name=None, *args):
        pm.select(name, tgl=1)

    def _reset(self, name=None, *args):
        obj = pm.PyNode(name)
        obj.setTranslation(0)
        obj.setRotation([0, 0, 0])

    def _resetAll(self, *args):
        for name in self.names:
            self._reset(name=name)

    def _selectAll(self, *args):
        pm.select(clear=1)
        for name in self.names:
            self._tglSelect(name=name)

if __name__ == '__main__':
    ui()
