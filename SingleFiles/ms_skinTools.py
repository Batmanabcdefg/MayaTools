import maya.cmds as cmds
import maya.mel as mel

class ms_skinTools():
    def __init__(self):
        if cmds.window('copyVertWeights',exists=True):
            cmds.deleteUI('copyVertWeights' ,window=True)
        window = cmds.window( 'copyVertWeights' , title="Tools", iconName='copyVertWeights' ) #, widthHeight=(200,100) )

        cmds.columnLayout( adjustableColumn=True )

        cmds.separator()
        cmds.columnLayout( adjustableColumn=True )
        cmds.button(label='Copy Vrt Wts',c=self.getVertWts)
        cmds.button( label='Paste Vrt Wts' ,c=self.setVertWts)
        cmds.setParent( '..' )

        cmds.separator()
        cmds.columnLayout( adjustableColumn=True )
        cmds.button(label='Hold All Wts',c=self.holdAllWts)
        cmds.button(label='Unlock All Wts',c=self.unholdWts)
        cmds.button(label='Hold Selected Wts',c=self.holdSelWts)
        cmds.button(label='Unlock Selected Wts',c=self.unholdSelWts)
        cmds.setParent('..')

        cmds.separator()
        cmds.columnLayout( adjustableColumn=True )
        cmds.button(label='Mirror: -x ---> +x',c=self.mirrorNegPos)
        cmds.button(label='Mirror: -x <--- +x',c=self.mirrorPosNeg)
        cmds.setParent('..')

        cmds.separator()
        cmds.columnLayout( adjustableColumn=True )
        cmds.button(label='List Influences',c=self.listInfs)
        cmds.button(label='Select Influences',c=self.selectInfs)
        cmds.setParent('..')

        cmds.separator()
        cmds.columnLayout( adjustableColumn=True )
        cmds.button(label='Match Model A <--- B',c=self.matchModel)

        cmds.setParent('..')
        cmds.separator()
        cmds.columnLayout( adjustableColumn=True )
        cmds.button(label='Match Pivot sel[:-1] ---> sel[-1]',c=self.matchPivots)
        cmds.setParent('..')

        cmds.showWindow( window )

    def matchPivots(self,*args):
        ''' Match pivot of all selected objects to the last selected object '''
        sel = cmds.ls(sl=True)
        for each in sel:
            cmds.xform(each,ws=1,rp=cmds.xform(sel[-1],q=1,ws=1,rp=1))

    def listInfs(self,*args):
        sel = cmds.ls(sl=True)
        infs = []
        for each in sel:
            sc = mel.eval('findRelatedSkinCluster("%s");'%each)
            if sc:
                for i in cmds.skinCluster(sc,q=True,inf=True):
                    infs.append(i)
        print '['
        for each in infs:
            print '"%s",'%each
        print ']'

    def selectInfs(self,*args):
        sel = cmds.ls(sl=True)
        infs = []
        for each in sel:
            sc = mel.eval('findRelatedSkinCluster("%s");'%each)
            if sc:
                infs.append(cmds.skinCluster(sc,q=True,inf=True))
        cmds.select(clear=True)
        for each in infs:
            cmds.select(each,add=True)

    def getVertWts(self,*args):
        sel = cmds.ls(sl=1)

        mesh = sel[0].split('.')[0]
        self.skClstr = mel.eval('findRelatedSkinCluster("%s")'%mesh)
        if self.skClstr:
            self.srcVals = cmds.skinPercent(self.skClstr, sel[0] , query=True, value=True )
            self.infs = cmds.skinCluster(self.skClstr, query=True, inf=True)
        else:
            raise Exception('No skinCluster found!')

    def setVertWts(self,*args):
        sel = cmds.ls(sl=True,fl=True)
        mesh = sel[0].split('.')[0]
        self.skClstr = mel.eval('findRelatedSkinCluster("%s")'%mesh)        
        for vert in sel:
            for val,inf in zip(self.srcVals,self.infs):
                cmds.skinPercent( self.skClstr, vert, transformValue=[(inf,val)] )

    def matchModel(self,*args):
        """ Move B points to A point positions."""
        sel = cmds.ls(sl=True,fl=True)
        if len( sel ) > 2:
            meshA = sel[0].split('.')[0]
            meshB = sel[-1]

            verts = sel[:-1]
            for vert in verts:
                a_pos = cmds.xform( vert, query=True,ws=True,t=True)
                cmds.xform(vert.replace(meshA, meshB),ws=True,t=a_pos)
        elif len( sel ) == 2:
            numVerts = cmds.polyEvaluate(sel[0],v=True)
            for index in range(numVerts):
                a_pos = cmds.xform('%s.vtx[%s]'%(sel[0],index),query=True,ws=True,t=True)
                cmds.xform('%s.vtx[%s]'%(sel[1],index),ws=True,t=a_pos)
        else:
            raise Exception('Select mesh A and B, or verts and mesh B.')


    def getInfWts(self,*args):
        """ On hold. Transfer weights from first selected inf to second
        	selected inf for selected components """
        sel = cmds.ls(sl=True,fl=True)
        mesh = sel[0].split('.')[0]
        self.skClstr = mel.eval('findRelatedSkinCluster("%s")'%mesh)

        infList = cmds.skinCLuster(skClstr,query=True,inf=True)
        for vert in sel:
            try:
                # Get value list, ordered to coorespond with infList
                valList = cmds.skinPercent( skClstr, vert, query=True, value=True )

                # Transfer the weights
                cmds.skinPercent( skClstr, vert, query=True, value=True )

            except Exception,e:
                raise Exception(e)

    def setInfWts(self,*args):
        """ On hold
        	Transfer values from the copied inf to the selected inf
        """
        sel = cmds.ls(sl=True)

        # Per vertex

    def holdSelWts(self,*args):
        sel = cmds.ls(sl=True)
        infs = []
        for each in sel:
            if cmds.objectType(each) == 'joint':
                infs.append(each)
        try:
            skClstr = mel.eval('findRelatedSkinCluster("%s");'%infs[0])
        except:
            raise Exception('Could not get a skinCluster for selected: ',infs[0])

        # Iterate the influences
        for inf in infs:
            cmds.setAttr('%s.liw'%inf,1)

    def unholdSelWts(self,*args):
        sel = cmds.ls(sl=True)
        infs = []
        for each in sel:
            if cmds.objectType(each) == 'joint':
                infs.append(each)
        try:
            skClstr = mel.eval('findRelatedSkinCluster("%s");'%infs[0])
        except:
            raise Exception('Could not get a skinCluster for selected: ',infs[0])

        # Iterate the influences
        for inf in infs:
            cmds.setAttr('%s.liw'%inf,0)


    def holdAllWts(self,*args):
        """ Hold all inf wts for selected mesh's skinCluster. """
        sel = cmds.ls(sl=True)
        try:
            skClstr = mel.eval('findRelatedSkinCluster("%s");'%sel[0])
        except:
            raise Exception('Could not get a skinCluster for selected: ',sel[0])
        # Get influences
        infs = cmds.skinCluster(skClstr,query=True,inf=True)

        # Iterate the influences
        for inf in infs:
            cmds.setAttr('%s.liw'%inf,1)

    def unholdWts(self,*args):
        """ Unhold all weights """
        sel = cmds.ls(sl=True)
        try:
            skClstr = mel.eval('findRelatedSkinCluster("%s");'%sel[0])
        except:
            raise Exception('Could not get a skinCluster for selected: ',sel[0])
        # Get influences
        infs = cmds.skinCluster(skClstr,query=True,inf=True)

        # Iterate the influences
        for inf in infs:
            cmds.setAttr('%s.liw'%inf,0)

    def mirrorNegPos(self,*args):
        """ Expects components to be selected """
        sel = cmds.ls(sl=True,fl=True)
        try:
            skClstr = mel.eval( 'findRelatedSkinCluster("%s");'%sel[0].split('.')[0] )
        except:
            raise Exception('Could not get a skinCluster for selected: ',sel[0].split('.')[0])

        # Inverse: - to +
        cmds.copySkinWeights( ss=skClstr, ds=skClstr, mirrorMode='YZ', mirrorInverse=True )

    def mirrorPosNeg(self,*args):
        """ Expects components to be selected """
        sel = cmds.ls(sl=True,fl=True)
        try:
            skClstr = mel.eval( 'findRelatedSkinCluster("%s");'%sel[0].split('.')[0] )
        except:
            raise Exception('Could not get a skinCluster for selected: ',sel[0].split('.')[0])

        # Inverse: - to +
        cmds.copySkinWeights( ss=skClstr, ds=skClstr, mirrorMode='YZ', mirrorInverse=False )

if __name__ =='__main__':
    msSkinTools()
