"""
Name: ms_sdkGui.py
Version: 1.1
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 13 July 2009
Last Modified: 16 July 2014
License: LGNU
Description:
    SDK interface were you can enter values instead of having to set keys.

To do: 
    Fix bug: Attribute option menu grows when object re-loaded.
                Re-load is necessary to update the Value field with new current 
                values after objects have been repositioned.
            Work around:
                Manually enter the values for any SDK after the default one:)

"""

import maya.cmds as mc
import pymel.core as pm

class ms_sdkGui():
    """
    SDK interface were you can enter values instead of having to set keys.
    """
    def __init__(self,*args):
        if(mc.window('sdkGuiWin',exists=True)):
           mc.deleteUI('sdkGuiWin',window=True)

        mc.window('sdkGuiWin',title="SDK GUI v1.1",rtf=True)
        mc.columnLayout()
        
        mc.text('    Driver:     ',fn='boldLabelFont')
        mc.rowLayout(nc=3)
        mc.text(' ')
        mc.text('Object:   ')
        self.driverField = mc.textFieldButtonGrp(bl='Load',bc=self.loadDriver)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(' ')
        mc.text('Attribute:   ')
        self.driverAttField = mc.optionMenu(changeCommand=self.setDriverVal)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(' ')
        mc.text('Value:    ')
        self.driverValueField = mc.floatField(v=0.0)
        mc.setParent('..')
        
        mc.separator(w=500)
       
        mc.text('    Driven:     ',fn='boldLabelFont')
        mc.rowLayout(nc=3)
        mc.text(' ')
        mc.text('Object:   ')
        self.drivenField = mc.textFieldButtonGrp(bl='Load',bc=self.loadDriven)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(' ')
        mc.text('Attribute:   ')
        self.drivenAttField = mc.optionMenu(changeCommand=self.setDrivenVal)
        mc.setParent('..')
        
        mc.rowLayout(nc=3)
        mc.text(' ')
        mc.text('Value:    ')
        self.drivenValueField = mc.floatField(v=0.0)
        mc.setParent('..')
        
        mc.separator(w=500)

        mc.text('    Options:',font='boldLabelFont')
        
        mc.rowLayout(nc=2)
        mc.text(' ')
        self.inTangentField = mc.optionMenu(label='In Tangent:   ')
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.text(' ')
        self.outTangentField = mc.optionMenu(label='Out Tangent:')
        mc.setParent('..')
        mc.rowLayout(nc=2)
        mc.text(' ')
        self.insertBlendField = mc.optionMenu(label='Insert Blend?:')
        mc.setParent('..')
        
        #Populate Options Insert Blend optionMenu
        mc.menuItem(parent=self.insertBlendField,label='False')
        mc.menuItem(parent=self.insertBlendField,label='True')
        
        #Populate Options In Tangent Type optionMenu
        mc.menuItem(parent=self.inTangentField,label='spline')
        mc.menuItem(parent=self.inTangentField,label='linear')
        mc.menuItem(parent=self.inTangentField,label='fast')
        mc.menuItem(parent=self.inTangentField,label='slow')
        mc.menuItem(parent=self.inTangentField,label='flat')
        mc.menuItem(parent=self.inTangentField,label='step')
        mc.menuItem(parent=self.inTangentField,label='clamped')
        mc.menuItem(parent=self.inTangentField,label='plateau')
        #Get user defined default
        #itt = mc.keyTangent(q=True,g=True,itt=True)
        #Set ITT optionMenu to default type
        #mc.optionMenu(self.inTangentField,e=True,v=itt[0])
        
        #Populate Options Out Tangent Type optionMenu
        mc.menuItem(parent=self.outTangentField,label='spline')
        mc.menuItem(parent=self.outTangentField,label='linear')
        mc.menuItem(parent=self.outTangentField,label='fast')
        mc.menuItem(parent=self.outTangentField,label='slow')
        mc.menuItem(parent=self.outTangentField,label='flat')
        mc.menuItem(parent=self.outTangentField,label='step')
        mc.menuItem(parent=self.outTangentField,label='clamped')
        mc.menuItem(parent=self.outTangentField,label='plateau')
        #Get user defined default
        #ott = mc.keyTangent(q=True,g=True,ott=True)
        #Set ITT optionMenu to default type
        #mc.optionMenu(self.outTangentField,e=True,v=ott[0])
        
        mc.separator(w=500)
        
        #Create button
        mc.rowLayout(nc=2,cw2=(200,100))
        mc.text(" ")
        mc.button(label="     Create SDK   ",c=self.createSDK,w=100)
        
        mc.showWindow('sdkGuiWin')
        
    def createSDK(self,*args):
        """
         Create the SDK with given values
        """
        #Store user values in variables
        driver = mc.textFieldGrp(self.driverField,q=True,text=True)
        driverVal = mc.floatField(self.driverValueField,q=True,v=True)
        driverAttr = mc.optionMenu(self.driverAttField,q=True,v=True)
        drivenValue = mc.floatField(self.drivenValueField,q=True,v=True)
        drivenAttr = mc.optionMenu(self.drivenAttField,q=True,v=True)
        drivenObj = mc.textFieldGrp(self.drivenField,q=True,text=True)
        inTangent = mc.optionMenu(self.inTangentField,q=True,v=True)
        outTangent = mc.optionMenu(self.outTangentField,q=True,v=True)
        blend = mc.optionMenu(self.insertBlendField,q=True,sl=True)
        
        currentDriver = '%s.%s' % (driver,driverAttr) 
        
        mc.setDrivenKeyframe(drivenObj,cd=currentDriver,dv=driverVal,v=drivenValue,at=drivenAttr,itt=inTangent,ott=outTangent,ib=blend)
        
    
    def objectAtts(self,*args):
        """
         Given object, returns it's keyable attributes
         Called by: loadDriver
        """
        obj = args[0]
        return mc.listAttr(obj, keyable=True)
        
    def loadDriver(self,*args):
        """
         Loads object name into text field.
        """
        sel = mc.ls(sl=True,fl=True)
        mc.textFieldButtonGrp(self.driverField,edit=True,text=sel[0])  
        
        #clear the menu items so list doesn't grow
        items = mc.optionMenu(self.driverAttField,q=True,ill=True)
        if(items):
                mc.setParent(self.driverAttField,menu=True)
                for each in items:
                        mc.deleteUI(each)
        
        #populate the option Menu with the names of objects keyable atts
        atts = mc.listAttr(sel[0], keyable=True)
        for each in atts:
            mc.menuItem(parent=self.driverAttField,label=each)  
        self.setDriverVal(sel[0])
            
    def setDriverVal(self,*args):
        """
         When the changeMenu is triggered for the driver attribute option menu, set the value to
         the new attribute.
        """
        obj = mc.textFieldGrp(self.driverField,q=True,text=True)
        attr = mc.optionMenu(self.driverAttField,q=True,v=True)
        val = mc.getAttr('%s.%s' % (obj,attr) )
        
        mc.floatField(self.driverValueField,e=True,v=float(val))
        
    def loadDriven(self, *args): 
        """
         Load object name for driven object in text field
        """
        sel = pm.ls(sl=True, fl=True)
        pm.textFieldButtonGrp(self.drivenField, edit=True, text=sel[0])  
        
        # Clear the menu items so list doesn't grow
        items = pm.optionMenu(self.drivenAttField, q=True, ill=True)
        if(items):
                pm.setParent(self.drivenAttField, menu=True)
                for each in items:
                        pm.deleteUI(each)
        
        # Check if blendshape
        if 'BlendShape' in str(type(sel[0])):  
            bs = sel[0]
        
            temp = pm.aliasAttr(bs, q=1)
            temp.sort()
            targets = []
            for each in temp:
                if each.startswith('weight'): continue
                targets.append(each)
        
            for tgt in targets:
                try:
                    pm.menuItem(parent=self.drivenAttField, label=tgt)
                except Exception, e:
                    print e
                    pm.warning('%s failed to create / connect' % tgt)
                    
        else:  
            #populate the option Menu with the names of objects keyable atts
            print sel[0]
            atts = pm.listAttr(sel[0], keyable=True)
            for each in atts:
                pm.menuItem(parent=self.drivenAttField, label=each)
            
    def setDrivenVal(self,*args):
        """
         When the changeMenu is triggered for the Driven attribute option menu, set the value to
         the new attribute.
        """
        obj = pm.textFieldGrp(self.drivenField, q=True, text=True)
        attr = pm.optionMenu(self.drivenAttField, q=True, v=True)
        val = pm.getAttr('%s.%s' % (obj, attr) )
        
        pm.floatField(self.drivenValueField, e=True, v=float(val))

        
