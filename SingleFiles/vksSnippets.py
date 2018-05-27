
''' Duplicate vks fk rig chains and constrain to fk rig'''
def dupChain(obj=None):
    #--- Duplicate / constraint FK rig joint chain
    # Select the chain
    pm.select(obj, r=1)
    pm.select(hi=1)
    sel = pm.ls(sl=1)
    pm.select(clear=1)
    orig_chain = [x for x in sel if x.type() == 'joint']
    
    # Duplicate and rename chain
    dup_chain = pm.duplicate(orig_chain[0])
    pm.select(dup_chain, hi=1)
    dup_chain = pm.ls(sl=1)
    pm.select(clear=1)
    
    count = 1
    for jnt in dup_chain:
        if jnt.type() != 'joint':
            pm.delete(jnt)
            continue
        jnt.rename(jnt.name().split('|')[-1].split('_')[0]+('_SH_%s' % count))
        count += 1
    
    # Rebiuld list without ocnstraints
    pm.select(dup_chain[0], hi=1)
    dup_chain = pm.ls(sl=1)
    pm.select(clear=1)
        
    pm.parent(dup_chain[0], w=1)
    
    for jnt in dup_chain:
        if jnt.type() == 'joint':
            pm.parentConstraint('%s' % jnt.name().replace('SH', 'joint'), jnt, mo=1)
            pm.scaleConstraint('%s' % jnt.name().replace('SH', 'joint'), jnt, mo=1)
            
# Call dupChain for all vks fk chains in scene
import pymel.core as pm
pm.select('vks_move_grp*')
sel = pm.ls(sl=1, type='transform')
grps = []
for each in sel:
    if each.type() == 'transform':
        grps.append(each)

for each in grps:
    dupChain(obj=each.getChildren()[-1])