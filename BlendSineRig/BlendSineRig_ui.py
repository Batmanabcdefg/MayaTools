import pymel.core as pm
from functools import partial


import BlendSineRig as BlendSineRig
reload(BlendSineRig)


class BlendSineRig_ui(object):
    '''
    Create a sine rig that is intuitive to animate.
    Uses expressions to animate joint chain rotations
    based on attributes created by this tool.
    '''
    def __init__(self):
        colWidth = 210

        winName = 'BlendSineRigWin333'
        if pm.window(winName, exists=1):
            pm.deleteUI(winName, window=1)
        win = pm.window(winName, t='BlendSineRig', w=400)
        pm.columnLayout(adj=1)

        # Name
        self.name_fld = pm.textFieldGrp(l='Name', w=400)

        # Nuetral curve
        self.crv_fld = pm.textFieldButtonGrp(l='Base Curve', bl='load', w=400)
        pm.textFieldButtonGrp(self.crv_fld, e=1,
                              bc=lambda:
                              pm.textFieldButtonGrp(self.crv_fld,
                                                    e=1,
                                                    text=pm.ls(sl=1)[0]))

        # Number of joints
        self.numJnts_fld = pm.textFieldGrp(l='Number of joints', w=400)

        # Control
        self.cnt_fld = pm.textFieldButtonGrp(l='Control', bl='Load', w=400)
        pm.textFieldButtonGrp(self.cnt_fld, e=1,
                              bc=lambda:
                              pm.textFieldButtonGrp(self.cnt_fld,
                                                    e=1,
                                                    text=pm.ls(sl=1)[0]))

        pm.rowLayout(nc=2, cw=(colWidth, colWidth))
        pm.text('Fordward / Back Curves\t\t\t')
        pm.text('Side to Side Curves')
        pm.setParent('..')

        pm.rowLayout(nc=2)
        self.fwd_sFld = pm.textScrollList(w=colWidth,
                                          numberOfRows=8,
                                          allowMultiSelection=True)
        self.side_sFld = pm.textScrollList(w=colWidth,
                                           numberOfRows=8,
                                           allowMultiSelection=True)
        pm.setParent('..')

        pm.rowLayout(nc=2, cw=(colWidth, colWidth))
        pm.columnLayout(w=colWidth)
        pm.button(l='Add', w=colWidth, c=partial(self.listAdd, self.fwd_sFld))
        pm.button(l='Remove',
                  w=colWidth,
                  c=lambda x: pm.textScrollList(self.fwd_sFld, e=1,
                                                rii=pm.textScrollList(
                                                    self.fwd_sFld,
                                                    q=1,
                                                    sii=1)))
        pm.button(l='Clear',
                  w=colWidth,
                  c=lambda x: pm.textScrollList(self.fwd_sFld, e=1, ra=1))
        pm.setParent('..')
        pm.columnLayout(w=colWidth)
        pm.button(l='Add',
                  c=partial(self.listAdd, self.side_sFld),
                  w=colWidth)
        pm.button(l='Remove',
                  w=colWidth,
                  c=lambda x: pm.textScrollList(self.side_sFld, e=1,
                                                rii=pm.textScrollList(
                                                    self.side_sFld,
                                                    q=1,
                                                    sii=1)))
        pm.button(l='Clear',
                  w=colWidth,
                  c=lambda x: pm.textScrollList(self.side_sFld, e=1, ra=1))
        pm.setParent('..')
        pm.setParent('..')

        # Create button
        pm.button(l="Create", c=self.createRig)

        # Development Aide
        pm.textFieldButtonGrp(self.crv_fld, e=1, text='curve1')
        pm.textFieldButtonGrp(self.cnt_fld, e=1, text='nurbsCircle1')
        pm.textFieldGrp(self.name_fld, e=1, text='Fin')
        pm.textFieldGrp(self.numJnts_fld, e=1, text='10')

        pm.showWindow(win)

    def listAdd(self, textList=None, *args):
        sel = pm.ls(sl=1)
        for s in sel:
            if s not in pm.textScrollList(textList, q=1, ai=1):
                pm.textScrollList(textList, e=1, a=s)

    def createRig(self, *args):
        BlendSineRig.BlendSineRig(control=pm.textFieldButtonGrp(
                                  self.cnt_fld, q=1, text=1),
                                  name=pm.textFieldGrp(
                                  self.name_fld, q=1, text=1),
                                  numJnts=pm.textFieldGrp(
                                  self.numJnts_fld, q=1, text=1),
                                  curve=pm.textFieldButtonGrp(
                                  self.crv_fld, q=1, text=1),
                                  fwdBackCrvs=pm.textScrollList(
                                      self.fwd_sFld, q=1, ai=1),
                                  sideToSideCrvs=pm.textScrollList(
                                      self.side_sFld, q=1, ai=1),)
