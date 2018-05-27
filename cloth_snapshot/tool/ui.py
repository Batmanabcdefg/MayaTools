import pymel.core as pm
from functools import partial
import os

import snapshot
import diff_snapshot
import implement_snapshot
reload(snapshot)
reload(diff_snapshot)
reload(implement_snapshot)


class ui():
    '''UI for cloth snapshot tool
    '''
    def __init__(self, *args):
        win = 'cloth_snapshot_win'
        version = '0.1'

        if pm.window(win, exists=1, *args):
            pm.deleteUI(win, window=1)

        pm.window(win, rtf=1, title='Cloth Snapshot UI v%s' % version)

        pm.columnLayout()
        pm.rowLayout(nc=2)
        pm.text('Working Directory')
        self.dirFld = pm.textFieldButtonGrp(bl='Browse')
        pm.textFieldButtonGrp(self.dirFld, e=1,
                              bc=partial(self.get_dir,
                                         self.dirFld))
        pm.setParent('..')

        pm.rowLayout(nc=3, cw3=(150, 150, 150))
        pm.button(l='Snapshot Selected', c=self.snapshot)
        pm.button(l='Diff Snapshots', c=self.diff_snapshot)
        pm.button(l='Apply Snapshot', c=self.implement_snapshot)
        pm.setParent('..')

        pm.showWindow(win)

    def snapshot(self, *args):  # results. str
        '''Snapshot selected nodes
        '''
        filePath = pm.textFieldButtonGrp(self.dirFld, q=1, text=1)
        results = snapshot.take_snapshot(path=str(filePath))
        self.display('Snapshot_Results',
                     results)

    def diff_snapshot(self, *args):  # results. str
        '''Prompt user to select two snapshot files and display the diff
        '''
        files = []
        files.append(str(self.get_file('file 1')))
        files.append(str(self.get_file('file 2')))

        if len(files) != 2:
            msg = str('Must select two snapshot files.\n' +
                      'Selected: %s' % files)
            raise Exception(msg)

        result = diff_snapshot.get_diff(files[0], files[1])
        lines = ['\t%s,\t%s' % (os.path.basename(files[0]),
                                os.path.basename(files[1]))]
        lines.append('\t' + (len(lines[0]) * '-'))
        for key in result:
            lines.append('\t' + str(key) + ': ' +
                         str(result[key][0]) + ', ' +
                         str(result[key][1]))

        self.display('Diff_Results', lines)

    def implement_snapshot(self, *args):  # results. str
        '''Promptuser for a snapshot file, then apply it's attribute to
        selected node
        '''
        node = pm.ls(sl=1)[0]
        f = self.get_file('Snapshot File to Apply to: %s' % node)
        d = implement_snapshot.get_dict(str(f))
        implement_snapshot.apply_dict(node, d)

        msg = ['\tApplied: %s\n' % str(f)]
        msg.append('\tTo Node: %s' % node)

        self.display('Results', msg)

    def get_dir(self, ui, *args):  # path. str
        '''Prompt user for a directory, write path to ui
        '''
        d = pm.windows.promptForFolder()
        pm.textFieldButtonGrp(ui, e=1, text=d)

    def get_file(self, title=None, *args):  # file paths. list[str, ...]
        '''Prompt user for a file
        '''
        return pm.fileDialog(t=title, dm='*.txt')

    def display(self, title=None, data=None, *args):
        '''Display the data ina window
        '''
        win = '%s_Win' % title

        if pm.window(win, exists=1):
            pm.deleteUI(win, window=1)
        print 'Title: ', title
        print 'data: ', data
        pm.window(win, rtf=1, title=title)

        pm.columnLayout(adj=1)
        for line in data:
            pm.text(str(line), al='left')

        pm.showWindow(win)

if __name__ == '__main__':
    ui()
