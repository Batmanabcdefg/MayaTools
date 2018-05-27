import pymel.core as pm

class RigToolsRename():
    '''
    Rename joints and controls created by rigtools variableKinematics script.
    '''
    def __init__(self):
        version = "1.0"
        if pm.window('RigToolsRenameWin', exists=True):
            pm.deleteUI('RigToolsRenameWin' , window=True)
        self.window = pm.window( 'RigToolsRenameWin' , title="Rig Tools Rename v%s" % version, iconName='RigToolsRenameWin' )

        with pm.columnLayout(adj=1):
            with pm.columnLayout( adjustableColumn=True ):
                pm.text('Assumes only one rig in the scene.')
                pm.text('Will only rename things with default naming.')
                self.cbFld = pm.checkBoxGrp( numberOfCheckBoxes=2,
                                             label='Type:',
                                             labelArray2=['FK', 'IK'] )
                self.nameFld = pm.textFieldGrp( label='Name' )
                pm.button(l='Rename', c=self.rename)

        pm.showWindow( self.window )

    def rename(self, *args):
        v1 = pm.checkBoxGrp(self.cbFld, q=1, v1=1)
        v2 = pm.checkBoxGrp(self.cbFld, q=1, v2=1)
        if v1 and v2:
            pm.warning('Only select one Type: FK or IK. No action taken.')
            return

        name = pm.textFieldGrp( self.nameFld, q=1, text=1)

        # Rename base control
        baseCnt = pm.PyNode('vks_explicit1')
        baseCnt.rename('%s_baseCnt' % name)

        # Get joints
        pm.select('vks_skin_joint_1', hi=1)
        jnts = pm.ls(sl=1, type='joint')
        count = 1
        for each in jnts:
            pc = each.listConnections(et=1, type='parentConstraint')[0]
            print pc
            pc.rename('%s_joint_%s_parentConstraint' % (name, count))
            each.rename('%s_joint_%s' % (name, count))
            pm.select(each, r=1)
            pm.mel.eval('ToggleLocalRotationAxes;')
            count += 1

        # FK parametric controls
        if v1:
            pm.select('vks_parametric*Shape')
            sel = pm.ls(sl=1)
            count = 1
            for each in sel:
                prnt = each.getParent()
                prnt.rename('%s_cnt_%s' % (name, count))
                count += 1

if __name__ =='__main__':
    RigToolsRename()
