''' Assorted Cluster related methods. To be used in Maya. '''
import maya.cmds as cmds

def cluster(name=None, deform=None, 
            handle=None, follow=None, parent=None):
    '''
    Create a cluster.
    Returns: ['clusterName','handleName']
    
    name -- Name for new cluster.
    deform -- Mesh or verts to deform with cluster.
    handle -- Transform to be used as the cluster handle.
    follow -- Transform that the cluster will follow.
    parent -- Transform that cluster will be parented under.
    
    All arguments are optional except deform.
    '''
    if not deform:
        raise Exception('No deform value passed in by caller.' + \
                        'Should be mesh name or list of vertices.')
    
    if type(deform) == 'list':
        cmds.select(clear=True)
        for each in deform:
            cmds.select(each,add=True)
    else:
        cmds.select(deform, r=True)
        
    if handle:
        cls = cmds.cluster(n=name, wn=[handle, handle])
    else:
        cls = cmds.cluster(n=name)
        
    if parent:
        cmds.parent(cls[1], parent)
        
    if follow:
        cmds.connectAttr('%s.pim'%cls[1],'%s.pm'%cls[0], f=True)
        cmds.parentConstraint(cls[1],follow,mo=True)
    
    return cls
    
        