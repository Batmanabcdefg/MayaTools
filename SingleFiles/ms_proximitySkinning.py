"""
Copyright (c) 2009 Mauricio Santos
Name: ms_proximitySkinning.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 6 June 2009
Last Modified: 14 June 2009
License: LGNU
Description: Apply gradient weight values to selected vertices
             along selected joints.

To do: 
    GUI:
        -Move items up/down in list.
        -Make sure added items are unique in list

        
Additional Notes:
    Progress:   Done - GUI 
                Almost Done - Need error checking! - Making button functions for list buttons.
                Everything is functioning as expected... Need to test it...
                Maya's default smooth binding out performs this, but this gives you specific control
                over a broad range, determined by an influences proximity to a vertex.
                 

    
"""

import maya.cmds as mc

class ms_proximitySkinning():
    """
    Description: Apply gradient weight values to selected vertices along selected joints.		
    """
    def __init__(self,*args):
        #GUI
        if(mc.window('ms_gsWin', exists=True)):
            mc.deleteUI('ms_gsWin',window=True)
						
        mc.window('ms_gsWin',rtf=True,title='Gradient Skinning v1.0', menuBar = True)
				
        mc.menu( label='Help' )
        mc.menuItem(label='Read Me',c=self.readMe)
				
				
        mc.columnLayout()
				
	mc.rowLayout(nc=2,cw2=(200,300))
				
	mc.frameLayout(label='Weight To list:',cll=False,fn='boldLabelFont',w=200, h=600)
	self.infsList = mc.textScrollList(numberOfRows=25, w=200, ams = True)
	mc.setParent("..")
				
        mc.frameLayout(label=' ',cll=False,w=310, h=600)
        mc.columnLayout()
        mc.frameLayout(label='Weight values per vertex: ',cll=False,fn='boldLabelFont',w=310, h=150)
        mc.columnLayout()
        mc.text("  Not all fields need values. You can place 1 in one field and\n leave the others at 0.")
        self.w1Field = mc.floatFieldGrp( numberOfFields=1, label='Nearest Influence:', value1=0.6 )
        self.w2Field = mc.floatFieldGrp( numberOfFields=1, label=' ', value1=0.2 )
        self.w3Field = mc.floatFieldGrp( numberOfFields=1, label=' ', value1=0.2 )
        self.w4Field = mc.floatFieldGrp( numberOfFields=1, label=' ', value1=0 )
        self.w5Field = mc.floatFieldGrp( numberOfFields=1, label='Farthest:', value1=0 )
        mc.setParent("..")
        mc.setParent("..")
        
        mc.frameLayout(label='Options:',cll=False,fn='boldLabelFont',w=310, h=100)
        mc.columnLayout()
        #self.maxInfsField = mc.intFieldGrp( numberOfFields=1, label='Max Influences:', extraLabel='Max: 5', value1=3 )
        self.maxDistField = mc.floatFieldGrp( numberOfFields=1, label='Max Distance:', value1=20 )
        self.pruneField = mc.floatFieldGrp( numberOfFields=1, label='Prune below:', value1=0.1 )
        mc.text(" ")
        self.normalField = mc.radioButtonGrp( label='Normalization:', labelArray2=['On', 'Off'], nrb=2,vr=False, sl=1 )
        mc.text(" ")
        mc.setParent("..")
        mc.setParent("..")
				
        mc.separator(w=310)
        
        mc.text('  List Options:  ',fn='boldLabelFont')
        
        mc.rowLayout(nc=2,cw2=(200,60))
        mc.text('  Add selected object(s) to list:')
        mc.button(label="Add",w=60,al='center', c=self.addToList)
        mc.setParent("..")
        
        """ Need to figure this out, but low priority
        mc.rowLayout(nc=3)
        mc.text('  Move selected:')
        mc.button(label="Up",w=60,al='center', c=self.itemUp)
        mc.button(label="Down",w=60,al='center', c=self.itemDown)
        mc.setParent("..")
        """
        
        mc.rowLayout(nc=3)
        mc.text('  Delete:')
        mc.button(label="Selected",w=60,al='center', c=self.delItem)
        mc.button(label="All",w=60,al='center', c=self.delAll)
        mc.setParent("..")
        mc.text(" ")
        
        mc.separator(w=310)
        
        mc.text(" ")
        mc.rowLayout(nc=3,cw3=(40,120,120))
        mc.text(" ")
        mc.button(label='   Skin',al='center',w=100, c=self.skin )
        mc.button(label='   Reset Weight',al='center',w=100,c=self.resetWgt ) 
        mc.setParent("..")
        
        mc.setParent("..")
        mc.setParent('..')
        
        mc.setParent("..")
        mc.setParent("..")
        
        mc.showWindow('ms_gsWin')
        #End GUI

    #The actual skinning function
    def skin(self, *args):
        
        vertices = mc.ls(sl=True,fl=True)
        influences = mc.textScrollList(self.infsList,q=True,ai=True)
        normalState = mc.radioButtonGrp(self.normalField,q=True,sl=True)
        
        w1 = mc.floatFieldGrp(self.w1Field,q=True,value=True)
        w2 = mc.floatFieldGrp(self.w2Field,q=True,value=True)
        w3 = mc.floatFieldGrp(self.w3Field,q=True,value=True)
        w4 = mc.floatFieldGrp(self.w4Field,q=True,value=True)
        w5 = mc.floatFieldGrp(self.w5Field,q=True,value=True)
        
        #maxInfs = mc.intFieldGrp(self.maxInfsField, q=True, value1=True)
        maxDist = mc.floatFieldGrp(self.maxDistField, q=True, value=True)
        prune = mc.floatFieldGrp(self.pruneField,q=True,value=True)
        
        prox = 0 #Initialized here to make it globally available
        
	#Make sure user has something selected
	if len(vertices) < 1:
	    print "No verts selected! Please select some verts to assign weight values to."
	    return 0
	
	temp = 0
	try:
	    temp = len(influences)
	except:
	    pass

	if temp:#Not zero or null type
	    pass
	else:
	    print "No influences in list! Please add some influences to use during weighting."
	    return 0

	
        #Get object name. skinCluster associated to vertices
        obj = vertices[0].split(".")
        #Get the skinCluster 
        history = mc.listHistory(obj[0])
               
        for each in history:
            if("skinCluster" in each):
                if("Group" not in each):
                    self.skinCluster = each
        
        #Progress window
        amount = 0
        mc.progressWindow(title="Applying Values",progress=amount,status='Percentage complete: 0%',ii=True)
        
        for vert in vertices:
            if mc.progressWindow( query=True, isCancelled=True): break
            if mc.progressWindow( query=True, progress=True ) >= 100: break
            amount += 1
            mc.progressWindow (edit=True, progress=amount, status=('Applying: ' + `amount` + '%'))
            
            infProxDict = {} #Create Dictionary > [Key: Proximity][Value: Influence name]
            for inf in influences: 
                prox = self.proximity(vert, inf)
                if prox < maxDist[0]:
                    #print inf + ":" + str(prox)
                    infProxDict[prox] = inf #Assigning to new key creates new entry in dict. [Key=Distance][Value=Inf Name]
                        
            #Sort the distances, and return a sorted list of the corresponding influences 
            sortedInfDict = self.sortDict(infProxDict) #Hold all the influences, sorted by distances from vert.
            
            finalInfDict = []   #List of influences within
            
            x = 0
            for each in sortedInfDict: 
                finalInfDict.append(each)
                x = x + 1
                
            #print "vert: " + vert
            #print "finalInfDict:" + str(finalInfDict)
            #print str(self.finalInfDict[0])
            #print str(self.finalInfDict[-1:][0])
            #print "sortedInfDict:" + str(sortedInfDict)
            #print "finalInfDict:" + str(finalInfDict)
            
            #Set the specified weights for the current vertex.
            if len(finalInfDict) == 1:        
                #print "In 1."
                mc.skinPercent( self.skinCluster, vert, transformValue= [ ( str(finalInfDict[0]), w1[0] ) ] )
            
            elif len(finalInfDict) == 2:        
                #print "In 2."
                mc.skinPercent( self.skinCluster, vert, transformValue= [ ( str(finalInfDict[0]), w1[0] ) , \
                                                                ( str(finalInfDict[1]), w2[0] ) ] ) 
            elif len(finalInfDict) == 3:        
                #print "In 3."
                mc.skinPercent( self.skinCluster, vert, transformValue= [ ( str(finalInfDict[0]), w1[0] ) , \
                                                                ( str(finalInfDict[1]), w2[0] ), \
                                                                ( str(finalInfDict[2]), w3[0] ) ] ) 
            elif len(finalInfDict) == 4:        
                #print "In 4."
                mc.skinPercent( self.skinCluster, vert, transformValue= [ ( str(finalInfDict[0]), w1[0] ) , \
                                                                ( str(finalInfDict[1]), w2[0] ), \
                                                                ( str(finalInfDict[2]), w3[0] ), \
                                                                ( str(finalInfDict[3]), w4[0] ) ] )
            elif len(finalInfDict) == 5 or len(finalInfDict) > 5:        
                #print "In 5."
                mc.skinPercent( self.skinCluster, vert, transformValue= [ ( str(finalInfDict[0]), w1[0] ) , \
                                                                ( str(finalInfDict[1]), w2[0] ), \
                                                                ( str(finalInfDict[2]), w3[0] ), \
                                                                ( str(finalInfDict[3]), w4[0] ), \
                                                                ( str(finalInfDict[4]), w5[0] )] ) 
            else:
                print "Not enough influences in list to support assignment." 

            
            if normalState == 1: #Turn it on
                mc.skinPercent( self.skinCluster, vert, normalize=True )
                
            #Prune small weights
            mc.skinPercent( self.skinCluster, obj[0], pruneWeights=prune[0] )
            
        mc.progressWindow(endProgress=1)
        #Ta da!
    
    def resetWgt(self,*args):
        """ 
            Reset selected verts to bindPose positions.
        """
        verts = mc.ls(sl=True,fl=True)
        #Get object name. skinCluster associated to vertices
        obj = verts[0].split(".")
        
        #Get the skinCluster 
        history = mc.listHistory(obj[0])
               
        for each in history:
            if("skinCluster" in each):
                if("Group" not in each):
                    skinCluster = each
        
        for each in verts:
            mc.skinPercent( skinCluster, each, resetToDefault=True )

        
        
        
    def sortDict(self,dict):
        #Keys are the proximity values and their values are the influence names.
        keys = dict.keys()
                   
        keys.sort()
        #print "Keyes:" + str(keys)
        
        #Return a sorted list of influence names.
        return [dict[key] for key in keys] 
                
    def proximity(self,vert,inf):
        """
            Get the distance for given vert from given inf
        """
                
        #Get vert location (0.0,0.0,0.0)
        vertLoc = mc.xform(vert,q=True,ws=True,t=True)
        #Get vert location (0.0,0.0,0.0)
        infLoc = mc.xform(inf,q=True,ws=True,t=True)
        
        distNode = mc.createNode('distanceBetween')
        mc.setAttr(distNode + ".p1x", vertLoc[0])
        mc.setAttr(distNode + ".p1y", vertLoc[1])
        mc.setAttr(distNode + ".p1z", vertLoc[2])
        mc.setAttr(distNode + ".p2x", infLoc[0])
        mc.setAttr(distNode + ".p2y", infLoc[1])
        mc.setAttr(distNode + ".p2z", infLoc[2])
        proximity = mc.getAttr(distNode + ".distance")
        mc.delete(distNode)
        
        return proximity
        
    
    #GUI List Management button functions.
    
    def addToList(self, *args):
        add = mc.ls(sl=True,fl=True) #Can put exact type and error check selection here
               
        for each in add:
               #Add the item
                mc.textScrollList(self.infsList,e=True,a=each)  
                
    
    def itemUp(self, *args):
        pass
    
    def itemDown(self, *args):
        pass
            
    def delItem(self, *args):
        selected = mc.textScrollList(self.infsList,q=True,si=True)    
        for each in selected:
            mc.textScrollList(self.infsList,e=True,ri=each)
    
    def delAll(self, *args):
        mc.textScrollList(self.infsList,e=True,ra=True)


    #Help Menu contents
    def readMe(self,*args):
        """
                Print use information.
        """
        if mc.window('ms_gs_rmWin',exists=True):
                        mc.deleteUI('ms_gs_rmWin', window=True)
        mc.window('ms_gs_rmWin',title='Gradient Skinning: Read Me', rtf=True)
        
        mc.columnLayout()
        
        mc.frameLayout(label='Directions',cll=False,fn='boldLabelFont',w=400, h=120)
        mc.columnLayout()
        mc.text('\n     Load joints/clusters/influences/etc to weight list.' )
        mc.text('     Then, set weight values and options as desired. ')
        mc.text('     Select the vertices you want to skin to the influences and')
        mc.text('     then press "Skin".')
        mc.setParent("..")
        mc.setParent("..")
        
        mc.frameLayout(label='What it does:',cll=False,fn='boldLabelFont',w=400, h=120)
        mc.columnLayout()
        mc.text('\n     Assigns weight values, entered by user, to each vertex. ' )
        #mc.text('     The Max Influences value controls how many influences can be')
        #mc.text('     weighted to by a given vertex.')
        mc.text('     The Max distance sets a limit on how far an influence that')
        mc.text('     gets weighted to can be .')
        mc.setParent("..")
        mc.setParent("..")
        
        mc.frameLayout(label='Options:',cll=False,fn='boldLabelFont',w=400, h=200)
        mc.columnLayout()
        mc.text('\n     Nearest Influence: The weight to assign to the nearest influence.\n' )
        mc.text('     Farthest Influence: Influence farthest from vertex.\n')
        mc.text('     Max Distance: Sets a limit on how far an influence that.')
        mc.text('     gets weighted to can be .')
        mc.text('     Prune Below: Zeros all influences with weight values below this value.\n')
        mc.text('     Skin button: Sets the weight values for selected verts.\n')
        mc.text('     Reset Weight: Resets selected verts to original smooth bind values.\n')
        mc.setParent("..")
        mc.setParent("..")
        
        mc.showWindow('ms_gs_rmWin')





            

