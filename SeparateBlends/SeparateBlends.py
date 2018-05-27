import pymel.core as pm
import pdb

'''
Required: Pymel. Uses pymel object methods.

Needed:
- Neutral and Target models
- Shaders with "_SB" assigned to faces to define regions

Creates region target models named after shader
'''

'''
Todo: Remove partition, get sets intersections of vertices
'''
def _getShaders():
    ''' Return all shaders with _SB suffix as list '''
    regionShaders = []
    lamberts = pm.ls(type='lambert')
    for lambert in lamberts:
        if '_SB' in lambert.name():
            regionShaders.append(lambert)
    return regionShaders
    
def _createSets(shaders=None):
    ''' Create partition and then sets from shaders.
    Returns: list of set names '''
    # Create main partition
    #part = pm.partition(name='BlendRegionsPartition')
    sets = []
    for shader in shaders:
        pm.select(_vertsFromShader(shader=shader),r=1)
        setName = '%s_set'%shader
        pm.sets(n=setName)
        #pm.mel.eval('$createSetResult = `sets -name "%s" -em`;'%(setName) +\
        #            'partition -e -addSet %s $createSetResult;'%(part) +\
        #            'sets -edit -forceElement $createSetResult;')
        sets.append(setName)
    return sets
        
def _createVertShaderMap(mesh=None, sets=None):
    weights = {}
    for i in range(mesh.numVertices()):
        numSets = 0
        for s in sets:
            if pm.sets(s,im='%s.vtx[%s]'%(mesh.name(),i)):
                numSets += 1
        weights[i] = numSets
    return weights
        
def _vertsFromShader(shader=None):
    currentSel = pm.ls(sl=1)
    faces = pm.listConnections(shader,type='shadingEngine')[0].members(flatten=1)
    pm.select(faces,r=1)
    pm.mel.eval('ConvertSelectionToVertices;')
    verts = pm.ls(sl=1)
    pm.select(currentSel, r=1)
    return verts
    
def _floodWeightsOnSelected(blendNode=None,value=None):
    ''' Set weights to value for selected components '''
    sel = pm.ls(sl=1,fl=1)
    blendName = blendNode.name()
    for each in sel:
        name = each.name()
        vert = name.split('[')[-1].split(']')[0]
        pm.setAttr('%s.inputTarget[0].inputTargetGroup[0].targetWeights[%s]'%(blendName,vert), value)
    
def _createTarget(name=None, mesh=None):
    ''' Duplicate neutral with masked blend weights '''
    d = pm.duplicate(mesh,n=name)
    pm.parent(d,world=True)
    
def main(neutral=None, target=None):
    ''' Generate separated blendshapes '''
        
    # Get shaders
    shaders = _getShaders()
    
    # Create sets
    sets = _createSets(shaders=shaders)
    
    # _createBlend
    blend = pm.blendShape( target, neutral )[0]
    pm.setAttr('%s.%s'%(blend,target),1)
    
    # Flood all weights to 0
    pm.mel.eval("select -r %s.vtx[0:%s]"%(neutral.name(), (neutral.numVertices()-1)))
    _floodWeightsOnSelected(blendNode=blend, value=0)
           
    # Get vertex weight dictionary
    weights = _createVertShaderMap(mesh=neutral,sets=sets)
    
    # Setup progressbar
    gMainProgressBar = pm.mel.eval('$tmp = $gMainProgressBar')
    pm.progressBar( gMainProgressBar,
                    edit=True,
                    beginProgress=True,
                    isInterruptable=True,
                    status='Creating blendshape targets from shaders ...',
                    maxValue=len(sets) )
    
    # Generate target per set
    for s in sets:
        if pm.progressBar(gMainProgressBar, query=True, isCancelled=True ) : break  

        # Select components
        pm.select(s,r=1)
        verts = pm.ls(sl=1,fl=1)
        
        # Flood blend deformer weights to 1
        for v in verts:
            pm.select(v,r=1)
            num = int(v.split('[')[-1].split(']')[0])
            w = float(1.0/weights[num])
            _floodWeightsOnSelected(blendNode=blend, value=w)
        
        # Create target
        _createTarget(mesh=neutral, name=s.replace('_set','Morph'))
        
        # Flood all weights to 0
        pm.mel.eval("select -r %s.vtx[0:%s]"%(neutral.name(), (neutral.numVertices()-1)))
        _floodWeightsOnSelected(blendNode=blend, value=0)
        
        pm.progressBar(gMainProgressBar, edit=True, step=1)

    pm.progressBar(gMainProgressBar, edit=True, endProgress=True)
    