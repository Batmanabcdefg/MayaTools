"""
Copyright (c) 2009 Mauricio Santos
Name: ms_matchOrientation.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 17 Aug 2009
Last Modified: 17 Aug 2009
License: LGNU
Description:
    Match the orientation of object A to the orientation of B. A=adjust orientation, B=match this orientation
To do:
    
    

Additional Notes:

"""
import maya.cmds as mc 

class  ms_matchOrientation():
    """
     Match the orientation of object A to the orientation of B. A=adjust orientation, B=match this orientation
    """
    def __init__(self,*args):
        #store selected
        sel = mc.ls(sl=True,fl=True)
        
        #Get
   