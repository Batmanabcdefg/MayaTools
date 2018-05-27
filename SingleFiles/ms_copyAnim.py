import pymel.core as pm

class ms_copyAnim():
    '''
    Given source namespace and target namespace,
    copy all animation from control ns to target ns on all transform nodes.
    '''
    def __init__(self):
        version = "1.0"
        if pm.window('ms_copyAnimWin',exists=True):
            pm.deleteUI('ms_copyAnimWin' ,window=True)
        self.window = pm.window( 'ms_copyAnimWin' , title="Copy Animation v%s" % version, iconName='ms_copyAnimWin' ) #, widthHeight=(200,100) )

        with pm.columnLayout(adj=1):
            self.mainLO = pm.columnLayout( adjustableColumn=True )
            removeList = ['shared', 'UI']
            self.namespaces = pm.namespaceInfo(lon=1)
            for each in removeList:
                self.namespaces.remove(each)
                
            with pm.rowLayout(nc=2):
                self.srcFld = pm.optionMenu( label='Source Namespace' )
                for each in self.namespaces:
                    pm.menuItem( label=each )  
                self.tgtFld = pm.optionMenu( label='Target Namespace' )
                for each in self.namespaces:
                    pm.menuItem( label=each ) 
                    
            pm.button(l='Copy animation', c=self.copyAnim)
            
        pm.showWindow( self.window )
            
    def copyAnim(self, args):
        '''
        Copy all animation on transform nodes from one namespace to another
        '''
        srcNS = pm.optionMenu(self.srcFld, q=1, v=1)
        tgtNS = pm.optionMenu(self.tgtFld, q=1, v=1)
        
        sourceControls = pm.ls('%s:*' % srcNS, type='transform')
        sourceControls += pm.ls('%s:CRIG:*' % srcNS, type='transform')

        msgs = []
        for src in sourceControls:
            try:
                if not src.getShape().type() == 'nurbsCurve': 
                  continue
            except: 
                continue

            print "Trying: ", src
            cnt = src.split(':')[1:]
            cnt = ":".join(cnt)
            tgtCnt = '%s:%s' % (tgtNS, cnt)

            try:
                pm.copyKey(src)
                pm.pasteKey(tgtCnt)
            except Exception, e:
                # try:
                #     pm.delete(pm.pointConstraint(src, tgtCnt, mo=0))
                #     pm.delete(pm.orientConstraint(src, tgtCnt, mo=0))
                # except Exception, e:
                print '\nFailed'
                print 'Source: ',src
                print 'Error:', e
            
            
        
        

if __name__ =='__main__':
    ms_copyAnim()
