#        Name:            rg_skinUpdate.py
#        Version:         1.0
#        Company:        Red Giants Studio, LLC
#        Author:         Mauricio Santos
#        Contact:        mauricioptkvp@hotmail.com
#        Date Created:     9 Sep 2008
#        Last Modified:    15 Sep 2008
#
#
#        Description:
#
#            Select Skin Cluster A, B
#            
#
#

class rg_skinTools():
    def __init__(self):
        if(mc.window( 'skinToolsWin',exists=True )):
            mc.deleteUI( 'skinToolsWin',window=True)
            
        mc.window('skinToolsWin',rtf=True, title = "Skin Tools v1.0",w=320)   
        
        mc.columnLayout()
        
        mc.frameLayout(label="List/Select Influences",cl=True,cll=True)
        mc.columnLayout()
        
        self.meshField = mc.textFieldButtonGrp( label="Mesh", buttonLabel="Load", bc = self.loadMesh)
        
        mc.rowLayout(nc=2)
        mc.button(label="List",c=self.listInfluences)
        mc.button(label="Select",c=self.selectInfluences)
        mc.setParent("..")
        
        
        mc.setParent("..")
        mc.setParent("..")

    def listInfluences(self,*args):
        mesh = mc.textFieldButtonGrp(self.meshField,query=True,text=True)
        
        skinCluster = mc.listConnections(mesh,et='skinCluster' )
        
        print skinCluster
    
    def selectInfluences(self,*args):
        pass
    
    def loadMesh(selfself,*args):
        sel = mc.ls(sl=1)
        mc.textFieldButtonGrp(self.meshField,edit=True,text=sel[0])        


'''
scA = "skinCluster64"
scB = "NewSkin:skinCluster64"

Aunique = []
Bunique = []

aInf = mc.listConnections(scA,type='joint')
bInf = mc.listConnections(scB,type='joint')

#Unique items in A
#    For each item in aInf, check against each item in bInf,
#        store items that match > Create new list
#
#
for each in aInf:
        temp = "NewSkin:" + each
        if(temp not in bInf):         
            Aunique.append(each)    
    
for each in bInf:
    temp = each.split(":")
    if(temp[1] not in aInf):
        Bunique.append(temp[1])

print "A Influences not in B"        
for each in Aunique:
    print each
    
print "\nB Influences not in A"
for each in Bunique:
    print each
'''    
        