'''
MrRender v1.7 Threaded job management for Maya Mental Ray batch rendering
Copyright (C) 2017  Mauricio Santos-Hoyos

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

'''
TODO:
- Add logic to make temp copy of .ma, update render settings in temp file via mayapy call
- Notify via e-mail if x status
- Set SG Task Status, add message with G-Drive link if status is Pending Review
- Improve thread / mainloop exiting so user can leave app open and switch scenes as needed
- Send job to cloud instance
- Logging
'''

'''
Release Note:
- v1.7:
     - Display target directory in Jobs windows
     - Added tabs: render & settings (settings ui/logic is wip)
     - Added retry ui/logic
- v1.6: 
     - Added render thread UI option
     - Made all threads daemonic
     Bug fixes
     - Disabled auto-retry logic
- v1.5: 
     - Enforce queueing of render jobs when "Render All" button pressed vs all starting at once
     Bug fixes
     - Fixed stop button for Windows
- v1.4:
     - Added auto retry logic on any status other than Timed Out or Render Complete
     - Increased Layer info and Jobs info scroll window size
- v1.3: 
     - Fixed log file path to account for custom path updates 
     - Removed EXR count check
     - Fixed Jobs UI "Status" label column error
- v1.2: 
     - Added job Stop button
     - EXR count check 
     - UI alert prompts vs shell errors
     - Remove 128 byte EXRs from target directory
- v1.1: 
     - Added Time out
     - Max Idle
- v1.0: Initial release

Known Bugs/Limitations:
- Requires restart of app when switching scene 
- Only works for MentalRay
'''


import Tkinter
import tkFileDialog
import tkMessageBox
from functools import partial
import os

import render_ui as render_ui
reload(render_ui)

import settings_ui as settings_ui
reload(settings_ui)

version = '1.7'

class TabFrame(Tkinter.Frame):
    def __init__(self, master, name):
        Tkinter.Frame.__init__(self, master)
        self.tab_name = name
        self.configure(highlightbackground="black", 
                       highlightcolor="black", 
                       highlightthickness=2, bd=0)
        
        
class TabBarFrame(Tkinter.Frame):
    def __init__(self, master=None, init_name=None):
        Tkinter.Frame.__init__(self, master)
        
        self.font = 'Arial'
        self.fontSmall = 12
        self.fontLarge = 16
        
        self.tabFrames = []
        self.tabButtons = []
        self.current_tab = None
        self.init_name = init_name
        self.btn_index = 0
        

    def add(self, tabFrame):
        name = tabFrame.tab_name
        self.tabFrames.append(tabFrame)
        
        btn = Tkinter.Button(self, 
                        text=name, 
                        command=partial(self.click, len(self.tabFrames)-1),
                        font=(self.font, self.fontSmall))
        self.tabButtons.append( btn )
        self.placeButtons()
        
    def placeButtons(self):
        btnsLen = len(self.tabFrames)
        btnWidth = 1.0/btnsLen
        if btnsLen == 1:
            btnOffsetX_inc = 0
        else:
            btnOffsetX_inc = 1.0/btnsLen
        
        index = 0
        for btn in self.tabButtons:
            btn.place(relx = btnOffsetX_inc*index,
                      relwidth=btnWidth, 
                      relheight=1) 
            index += 1
        
    def click(self, index):
        # Set all buttons to normal font
        for btn in self.tabButtons:
            btn.configure(font=(self.font,
                                self.fontSmall))       
                
        # Set clicked button to selected font
        self.tabButtons[index].configure(font=(self.font,
                                               self.fontLarge,
                                               "bold"))
            
        # Lower all tabFrames
        for tabFrame in self.tabFrames:
            tabFrame.lower()
            
        # Lift desired tabFrame
        self.tabFrames[index].lift()
        
class UI(Tkinter.Tk):
    '''
    UI for batch rendering Maya scenes using Mental Ray
    '''
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        WIN_WIDTH = 850
        WIN_HIGHT = 950
        WIN_PADX = 30 
        WIN_PADY = 30
        self.geometry("%sx%s+%s+%s" % (WIN_WIDTH, 
                                       WIN_HIGHT, 
                                       WIN_PADX, 
                                       WIN_PADY))
        self.resizable(width=False, height=True)
        
        # Tab setup
        bar = TabBarFrame(parent, "MrRender v%s" % version)
        bar.place(relx = 0, rely = 0, relwidth=1, relheight=0.03)
    
        tabFrame1 = TabFrame(parent, "Render")
        tabFrame1.place(relx = 0, rely = 0.03, relwidth=1, relheight=0.9)
        tc = render_ui.UI(tabFrame1)
        tc.drawUI()
    
        tabFrame2 = TabFrame(parent, "Settings")
        tabFrame2.place(relx = 0, rely = 0.03, relwidth=1, relheight=0.9)
        #tt = settings_ui.UI(tabFrame2)
        #tt.drawUI()   
        
        bar.add(tabFrame1)                  
        bar.add(tabFrame2)	
    
        # Set tab to first tabFrame
        bar.tabButtons[0].invoke()


if __name__ == "__main__":
    app = UI(None)
    app.title('MrRender v%s' % version)
    def on_closing():
        if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
            app.destroy()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
