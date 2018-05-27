import pymel.core as pm

__author__ = Mauricio Santos

def getA( ):
    return pm.ls(sl=1)[0]

def getB( ):
    return pm.ls(sl=1)[1]

def createDecomp( obj=None )
    """ Create decomposeMatrix node. """
    return pm.createNode('decompseMatrix', n='%s_decomp'%obj)

def createWMMDs( aDecomp=None, bDecomp=None )
    a_attrs = [attr for attr in pm.listAttr( aDecomp ) if 'out*' in attr]
    b_attrs = [attr for attr in pm.listAttr( bDecomp ) if 'out*' in attr]

    mds = []
    inde
    for a_attr, b_attr in zip( a_attrs, b_attrs ):
        mds.apped( pm.createNode( 'multiplyDivide', n='%s_dcmpmd'%aDecomp) )
        pm.connectAttr( '%s.%s'%( aDecomp, a_attr ), '%s.input1X'%( mds[ index ], b_attr ), f=1 )

        index += index
def createResultMD( wmMds=None ):
    pass

def main( ):
    a = getA( )
    b = getB( )

    aDecomp = createDecomp( a )
    bDecomp = createDecomp( b )

    wmMds = createWMMDs( aDecomp, bDecomp )

    createResultMD( wmMds )


