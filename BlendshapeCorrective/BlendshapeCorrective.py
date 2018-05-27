__author__ = 'mauriciosantoshoyos@gmail.com'

import pymel.core as pm
import pymel.core.datatypes as pmd

class BlendshapeCorrective(object):
    '''
    Give: Neutral, TargetA, TargetB, TargetC (Requires individual meshes)
    
    Generate: Corrective = TargetC - (TargetA + TargetB)
    
    Use: 
    - Turn on shapes A and B on blendshape
    - Duplicate blendshape mesh and sculpt corrective fix (TargetC)
    - Select: Neutral, TargetA, TargetB, TargetC
    - Run script
    - Result: Corrective Shape that can be added to blendshape
    '''    
    def __init__(self):
        win = 'BlendshapeCorrectiveWin'
        if pm.window(win, exists=True):
            pm.deleteUI(win ,window=True)
        window = pm.window( win , title="Blendshape Corrective", iconName=win )

        pm.columnLayout( adjustableColumn=True )

        pm.separator()
        pm.columnLayout( adjustableColumn=True )
        pm.button(label='Create Corrective Shape', c=self.generateShape)
        pm.setParent( '..' )

        pm.showWindow( window )
    
    def generateShape(self, *args):
        sel = pm.ls(sl=1)
        if len(sel) != 4:
            pm.mel.warning('Must select: Neutral, TargetA, TargetB, TargetC meshes')
            return
        
        meshN = sel[0]
        meshA = sel[1]
        meshB = sel[2]
        meshC = sel[3]
        
        # Create new mesh
        new = pm.duplicate(meshN, n='Corrective')[0]
        
        # Per vertex, translate in world space: C-(A+B)
        for vtx in new.vtx:
            vert = vtx.split('.')[1]
            n_pos = pmd.Point(pm.xform( vtx, query=True, ws=True, t=True))
            a_pos = pmd.Point(pm.xform( meshA + '.' + vert, query=True, ws=True, t=True))
            b_pos = pmd.Point(pm.xform( meshB + '.' + vert, query=True, ws=True, t=True))
            c_pos = pmd.Point(pm.xform( meshC + '.' + vert, query=True, ws=True, t=True))
            
            aVec = a_pos - n_pos
            bVec = b_pos - n_pos
            cVec = c_pos - n_pos

            delta = cVec - (aVec + bVec)
            
            pm.move(vtx, delta, r=1)
            
if __name__ == '__main__':
    BlendshapeCorrective()