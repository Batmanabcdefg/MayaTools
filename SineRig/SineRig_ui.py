import pymel.core as pm


import SineRig as SineRig
reload( SineRig )


class SineRig_ui(object):
    '''
    Create a sine rig that is intuitive to animate.
    Uses expressions to animate joint chain rotations 
    based on attributes created by this tool.
    '''
    def __init__(self):
        winName = 'SineRigWin333'
        if pm.window(winName, exists=1):
            pm.deleteUI(winName,window=1)
        win = pm.window(winName, t='SineRig')
        
        pm.columnLayout(adj=1)
        pm.text('X Axis should be joint chain aim axis.')
        # Control
        self.cnt_fld = pm.textFieldButtonGrp(l='Control',bl='Load')
        pm.textFieldButtonGrp( self.cnt_fld, e=1, bc=lambda: pm.textFieldButtonGrp(self.cnt_fld,e=1,text=pm.ls(sl=1)[0]) )
        
        # Name
        self.name_fld = pm.textFieldGrp(l='Name')
        
        # Base jnt
        self.base_fld = pm.textFieldButtonGrp(l='Base Joint',bl='Load')
        pm.textFieldButtonGrp( self.base_fld, e=1, bc=lambda: pm.textFieldButtonGrp(self.base_fld,e=1,text=pm.ls(sl=1)[0]) ) 
        
        # Tip jnt
        self.tip_fld = pm.textFieldButtonGrp(l='Tip Joint',bl='Load')
        pm.textFieldButtonGrp( self.tip_fld, e=1, bc=lambda: pm.textFieldButtonGrp(self.tip_fld,e=1,text=pm.ls(sl=1)[0]) )        
        
        # Create button
        pm.button(l="Create",c=self.createRig)
        
        ##### Development Aide
        pm.textFieldButtonGrp(self.cnt_fld,e=1,text='TopFin_Base_ctrlA')
        pm.textFieldGrp(self.name_fld,e=1,text='Fin')
        pm.textFieldButtonGrp(self.base_fld,e=1,text='TopFinA_jnt_1')        
        pm.textFieldButtonGrp(self.tip_fld,e=1,text='TopFinA_jnt_12')        
        
        pm.showWindow(win)
        
    def createRig(self, *args):
        SineRig.SineRig(control=pm.textFieldButtonGrp(self.cnt_fld,q=1,text=1),
                        name=pm.textFieldGrp(self.name_fld,q=1,text=1),
                        baseJnt=pm.textFieldButtonGrp(self.base_fld,q=1,text=1),
                        tipJnt=pm.textFieldButtonGrp(self.tip_fld,q=1,text=1))
        