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

import Tkinter
import Tkinter as tk
import tkFileDialog
import tkMessageBox
from functools import partial
import os

import mr_render as mr
reload(mr)

class UI():
    '''
    Add widgets to frame
    '''
    def __init__(self, parent=None):
        self.parent = parent
        self.mrRender = mr.Render()
        self.tk = tk
        #self.width = 500
        
    def drawUI(self):
        smallWidth = 12

        self.rlNameVars = []
        self.rlEnableSeVars = []
        self.rlSeVars = []
        self.rlEnableVars = []
        self.rlTimeOutFlds = []
        self.rlMaxIdleFlds = []
        self.rlTimeOutEnableVars = []
        self.rlMaxIdleEnableVars = []

        self.osVar = Tkinter.StringVar()
        self.verVar = Tkinter.StringVar()
        self.mayaVar = Tkinter.StringVar()
        self.tgtDirVar = Tkinter.StringVar()
        self.cameraVar = Tkinter.StringVar()
        self.logVar = Tkinter.StringVar()
        self.rdVar = Tkinter.StringVar()
        self.sceneVar = Tkinter.StringVar()

        self.shot = ''
        self.shotDir = ''
        self.renderButtons = []
        self.rlCanvas = None
        self.mainUIVsb = None

        # Maya selection
        f0 = Tkinter.Frame(self.parent)
        f0_relh = 0.032
        f0.place(relx = 0.2, rely = 0, relwidth=1, relheight=f0_relh)

        # Render, Scene, Tgt dir selection
        f1 = Tkinter.Frame(self.parent)
        f1_relh = 0.13
        f1_rely = f0_relh
        f1.place(relx = 0.12, rely = f1_rely, relwidth=1, relheight=f1_relh)

        # Using self as this frame is referenced in method call outside this block
        # Render Layers Title
        self.f2 = Tkinter.Frame(self.parent)
        f2_relh = 0.03
        f2_rely = f1_rely + f1_relh
        self.f2.place(relx = 0.37, rely = f2_rely, relwidth=1, relheight=f2_relh)

        # Render layers
        self.f3 = Tkinter.Frame(self.parent, 
                                highlightbackground="black", 
                                highlightcolor="black", 
                                highlightthickness=1, 
                                bd=0) # Render layer scroll frame
        f3_relh = 0.587
        f3_rely = f2_rely + f2_relh
        self.f3.place(relx = 0, rely = f3_rely, relwidth=1, relheight=f3_relh)

        # Render Options
        f4 = Tkinter.Frame(self.parent)
        f4_relh = 0.16
        f4_rely = f3_rely + f3_relh
        f4.place(relx = 0.1, rely = f4_rely, relwidth=1, relheight=f4_relh)

        # Divider
        f5=Tkinter.Frame(self.parent, height=1, width=800, bg="black")
        f5_relh = 0.001
        f5_rely = f4_rely + f4_relh
        f5.place(relx = 0, rely = f5_rely, relwidth=1, relheight=f5_relh)

        # Create button
        f6 = Tkinter.Frame(self.parent)
        f6_relh = 0.04
        f6_rely = f5_rely + f5_relh 
        f6.place(relx = 0.45, rely = f6_rely, relwidth=1, relheight=f6_relh)

        # Frame 0 ------------------------------------------------------------------------------------
        def updateMayaPath(*args):
            ''' Update Maya Path accordingly for OS / Maya Version seleced by user '''
            ver = self.verVar.get()
            if self.osVar.get() == 'win':
                self.mayaVar.set('C:/Program Files/Autodesk/Maya%s/bin/Render' % ver)
            if self.osVar.get() == 'mac':
                self.mayaVar.set('/Applications/Autodesk/maya%s/Maya.app/Contents/bin/Render' % ver)

        row = 0
        #self.osVar.set('mac')
        self.osVar.trace("w", updateMayaPath)
        self.osUI = self.makeOptionMenu(f0, 'OS: ', 'mac', 0, row, self.osVar, [])
        self.updateOptionMenu(self.osUI, self.osVar, ['win', 'mac'])

        #self.verVar.set('2015')
        self.verVar.trace("w", updateMayaPath)
        self.verUI = self.makeOptionMenu(f0, 'Maya Version: ', '2014', 2, row, self.verVar, [])
        self.updateOptionMenu(self.verUI, self.verVar, ['2014', '2015'])

        # Frame 1 ------------------------------------------------------------------------------------
        row = 0
        self.makeLabelBtn(f1, 'Maya Render Path: ', row, self.mayaVar,
                          btn='Browse',
                          bc=partial(self.browse_file, self.mayaVar))
        row += 1
        self.makeLabelBtn(f1, 'Render Scene: ', row, self.sceneVar,
                          btn='Browse',
                          bc=partial(self.browse_scene, self.sceneVar))
        #self.sceneVar.set('/Users/mauricio/Desktop/DET.0010.lighting.ma')
        row += 1
        self.makeLabelBtn(f1, 'Target Directory: ', row, self.tgtDirVar,
                          btn='Browse',
                          bc=partial(self.browse_dir, self.tgtDirVar))
        #self.tgtDirVar.set('/Users/mauricio/Desktop/temp')
        row += 1
        self.imUI = self.makeLabelText(f1, 'Image Naming: ', 0, row, '', 10, 18)
        #self.imUI.insert(0,'DET0010/<RenderLayer>/DET.0010.<RenderLayer>')

        # Frame 2 ------------------------------------------------------------------------------------
        # Render layer title frame, populated by browse_scene() once render scene is selected

        # Frame 3 ------------------------------------------------------------------------------------
        # Render layer scrollbar frame, populated by browse_scene() once render scene is selected

        # Frame 4 ------------------------------------------------------------------------------------
        row = 0
        self.toUI = self.makeLabelText(f4, 'Time Out: ', 0, row, '10000', 12, 12)
        self.miUI = self.makeLabelText(f4, 'Max Idle: ', 2, row, '20', 12, 12)
        self.thUI = self.makeLabelText(f4, 'CPU % Min: ', 4, row, '10', 12, 12)

        row += 1
        self.rtFld = self.makeLabelText(f4, 'Render Threads:', 0, row, '18', 18, 4)
        self.rtFld.configure(state='disabled')
        self.rtCB = Tkinter.StringVar()
        c = Tkinter.Checkbutton(f4, 
                                variable=self.rtCB, 
                                command=partial(self.enableSE, self.rtCB, self.rtFld) )
        self.rtCB.set(0)
        c.grid(column=2, row=row, sticky='EW')  
        
        label = Tkinter.Label(f4, text=u'Auto Restart:', anchor='e', width=12)
        label.grid(column=3, row=row, sticky='EW')  
        self.autoCB = Tkinter.StringVar()
        c = Tkinter.Checkbutton(f4, variable=self.autoCB)
        self.autoCB.set(1)
        c.grid(column=4, row=row, sticky='EW')        

        row += 1
        self.fncUI = self.makeLabelText(f4, 'File Naming: ', 0, row, 'name.#.ext', 12, 12)
        self.seUI = self.makeLabelText(f4, 'Start, End: ', 2, row, '1,100', 12, 12)
        self.camUI = self.makeOptionMenu(f4, 'Camera: ', '------', 4, row, self.cameraVar, [])

        row += 1
        self.bUI = self.makeLabelText(f4, 'By Frame: ', 0, row, '1', 12, 12)
        self.padUI = self.makeLabelText(f4, 'Padding: ', 2, row, '4', 12, 12)
        self.skipUI = self.makeLabelText(f4, 'Skip Existing: ', 4, row, '1', 12, 12)

        row += 1
        self.xUI = self.makeLabelText(f4, 'X Resolution: ', 0, row, '1920', 12, 12)
        self.yUI = self.makeLabelText(f4, 'Y Resolution: ', 2, row, '1080', 12, 12)
        self.percentResUI = self.makeLabelText(f4, '% Resolution: ', 4, row, '100', 12, 12)

        # Frame 5: Horizontal Divider ------------------------------------------------------------------------------------

        # Frame 6 ------------------------------------------------------------------------------------
        createBtn = Tkinter.Button(f6, command=self.createJobsWindow, text=u'Create Jobs')
        createBtn.grid(column=3, row=0, sticky='EW')
        row += 1
        
    def makeOptionMenu(self, parent=None, title=None, default=None,
                       col=None, row=None, var=None, options=None):
        ''' Create Option Menu '''
        var.set(default)
        label = Tkinter.Label(parent, text=u'%s' % title, anchor='e', width=12)
        label.grid(column=col, row=row, sticky='EW')
    
        menu = Tkinter.OptionMenu(parent, var, options)
        menu.grid(column=col+1, row=row, sticky='EW')
    
        return menu
    
    def makeLabelBtn(self, parent=None, label=None, row=None, var=None, btn=None, bc=None):
        '''Create a UI label'''
        label = Tkinter.Label(parent, text=u'%s' % label, anchor='e')
        label.grid(column=0, row=row, sticky='EW')

        fld = Tkinter.Label(parent, textvariable=var)
        fld.grid(column=1, row=row, sticky='EW')

        if btn:
            btn = Tkinter.Button(parent, command=bc, text=btn)
            btn.grid(column=2, row=row, sticky='EW')
    
    def makeLabelText(self, parent=None, label=None, col=None, row=None,
                      text=None, wL=None, wE=None):
        '''Create a text field'''
        label = Tkinter.Label(parent, text=u'%s' % label, anchor='e', width=wL)
        label.grid(column=col, row=row, sticky='EW')

        fld = Tkinter.Entry(parent, width=wE)
        fld.grid(column=col+1, row=row, sticky='EW')
        fld.insert(0, text)

        return fld
            
    def browse_dir(self, var):
        var.set(tkFileDialog.askdirectory())

    def updateOptionMenu(self, menu=None, var=None, options=None):
        menu = menu['menu']
        menu.delete(0, "end")
        for name in options:
            menu.add_command(label=name, command=lambda value=name: var.set(value))

    def enableSE(self, c_var, entry):
        '''
        Connect CheckBox state to a an Entry field enable/disable
        '''
        if int(c_var.get()):
            entry.configure(state='normal')
        else:
            entry.configure(state='disabled')

    def browse_scene(self, var):
        ''' Browse for file, then setup camera option menu and render layers frame '''
        smallWidth = 12
        wideWidth = 18
        rlFrameWidth = 825

        fn = tkFileDialog.askopenfilename()
        var.set(fn)
        self.shot = os.path.basename(fn).split('.')[0]
        self.shot += '.' + os.path.basename(fn).split('.')[1]
        self.shotDir = self.shot.split('.')[0] + self.shot.split('.')[1]

        self.imUI.delete(0, Tkinter.END)
        self.imUI.insert(0, 
                         self.shotDir + '/<RenderLayer>/' + self.shot + '.<RenderLayer>')

        result = self.mrRender.get_camera_renderLayers(fn)

        self.updateOptionMenu(self.camUI, self.cameraVar, result[0])

        # Render layer UI setup: Frame 2
        def enableAll():
            for rl in self.rlEnableVars:
                rl.set('Yes')

        def disableAll():
            for rl in self.rlEnableVars:
                rl.set('No')

        btn = Tkinter.Button(self.f2, command=enableAll, text=u'Enable All', width=12)
        btn.grid(column=1, row=0)

        btn = Tkinter.Button(self.f2, command=disableAll, text=u'Disable All', width=12)
        btn.grid(column=2, row=0)


        # Setup scroll bar: Frame 3
        def populate(frame, data):
            '''Render layer rows and enable all/none buttons'''
            row = 0
            for layer in data:
                if layer == 'defaultRenderLayer':
                    continue



                var = Tkinter.StringVar()
                menu = Tkinter.OptionMenu(frame, var, [])
                menu.grid(column=0, row=row, sticky='EW')
                var.set('Yes')
                self.updateOptionMenu(menu, var, ['Yes', 'No'])
                self.rlEnableVars.append(var)

                var = Tkinter.StringVar()
                var.set(layer)
                label = Tkinter.Label(frame, 
                                      textvariable=var, 
                                      anchor='c', 
                                      width=25)
                label.grid(column=1, row=row, sticky='EW')
                self.rlNameVars.append(var)

                se_var = Tkinter.StringVar()
                se_var.set('101,200')
                entry = Tkinter.Entry(frame, textvariable=se_var, width=smallWidth)
                entry.grid(column=2, row=row, sticky='EW')
                entry.configure(state='disabled')
                self.rlSeVars.append(se_var)
                var = Tkinter.StringVar()
                c = Tkinter.Checkbutton(frame, variable=var, 
                                        command=partial(self.enableSE, var, entry) )
                var.set(0)
                c.grid(column=3, row=row, sticky='EW')
                self.rlEnableSeVars.append(var)

                fld= self.makeLabelText(frame, 'Time Out:', 4, row, '60', 12, 4)
                fld.configure(state='disabled')
                self.rlTimeOutFlds.append(fld)
                var = Tkinter.StringVar()
                c = Tkinter.Checkbutton(frame, variable=var, 
                                        command=partial(self.enableSE, var, fld) )
                var.set(0)
                c.grid(column=6, row=row, sticky='EW')
                self.rlTimeOutEnableVars.append(var)

                fld= self.makeLabelText(frame, 'Max Idle:', 7, row, '10', 12, 4)
                fld.configure(state='disabled')
                self.rlMaxIdleFlds.append(fld)
                var = Tkinter.StringVar()
                c = Tkinter.Checkbutton(frame, variable=var, 
                                        command=partial(self.enableSE, var, fld) )
                var.set(0)
                c.grid(column=9, row=row, sticky='EW')
                self.rlMaxIdleEnableVars.append(var)

                row += 1

        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        try:
            self.rlCanvas.destroy()
            self.mainUIVsb.destroy()
        except:
            pass

        self.rlCanvas = Tkinter.Canvas(self.f3, borderwidth=0, background="#ffffff")
        frame = Tkinter.Frame(self.rlCanvas, background="#ffffff")
        self.mainUIVsb = Tkinter.Scrollbar(self.f3, orient="vertical", command=self.rlCanvas.yview)
        self.mainUIVsb.pack(side="right", fill="y")

        self.rlCanvas.configure(yscrollcommand=self.mainUIVsb.set)
        self.rlCanvas.pack(side="left", fill="both", expand=0)
        self.rlCanvas.create_window((4,4), window=frame, anchor="nw", width = rlFrameWidth)

        frame.bind("<Configure>", lambda event, canvas=self.rlCanvas: onFrameConfigure(self.rlCanvas))

        populate(frame, result[1])

        self.f2.config(width=rlFrameWidth)#, height=rlFrameHeight)
        self.f3.config(width=rlFrameWidth)#, height=rlFrameHeight)
        self.rlCanvas.config(width=rlFrameWidth)
        #onFrameConfigure(canvas)

    def browse_file(self, var):
        var.set(tkFileDialog.askopenfilename())

    def createJobsWindow(self):
        ''' Create jobs window '''
        self. validateRenderJobsUIData()

        win = Tkinter.Toplevel()
        win.wm_title("Render Jobs")
        win.geometry("1000x500")

        f0 = Tkinter.Frame(win) #, bg = "orange", width = 500, height = 500)
        f0.pack()#place(relx = 0.2, rely = 0, relwidth=1, relheight=0.13)
        f1 = Tkinter.Frame(win) #, bg = "orange", width = 500, height = 500)
        f1.pack()#place(relx = 0.1, rely = 0.1, relwidth=1, relheight=0.87)

        def on_closing():
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", on_closing)        

        self.createJobs([f0, f1])

    def createJobs(self, frames):
        ''' Creates jobs rows in passed in frames'''
        wide = 24
        narrow = 10
        frame_width = 1000

        def onFrameConfigure(e, canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(frame_id, height=e.height, width=e.width)

        def renderAll():
            for btn in self.renderButtons:
                btn.invoke()

        def populate(frame):
            self.renderButtons = []
            row = 1
            index = 0
            for layer in self.rlEnableVars:
                if layer.get() == 'Yes':

                    name = self.rlNameVars[index].get()
                    seOn = self.rlEnableSeVars[index].get()

                    toOn = self.rlTimeOutEnableVars[index].get()

                    miOn = self.rlMaxIdleEnableVars[index].get()

                    if int(seOn):
                        se = self.rlSeVars[index].get()
                        start = se.split(',')[0]
                        end = se.split(',')[1]
                    else:
                        start = self.seUI.get().split(',')[0]
                        end = self.seUI.get().split(',')[1]

                    if not int(toOn): to = self.toUI.get()
                    else: to = self.rlTimeOutFlds[index].get()

                    if not int(miOn): mi = self.miUI.get()
                    else: mi = self.rlMaxIdleFlds[index].get()


                    #f = Tkinter.Frame(frame)
                    #f.place(relx = 0, rely = 0, relwidth=1, relheight=1)

                    label = Tkinter.Label(frame, text=u'%s' % name, anchor='c', width=wide)
                    #label.place(relx = 0, rely = 0, relwidth=0.2, relheight=0.1)
                    label.grid(column=0, row=row, sticky='EW')

                    label = Tkinter.Label(frame, text=u'%s' % start, anchor='c', width=narrow)
                    #label.place(relx = 0, rely = 0.2, relwidth=0.05, relheight=0.1)
                    label.grid(column=1, row=row, sticky='EW')

                    label = Tkinter.Label(frame, text=u'%s' % end, anchor='c', width=narrow)
                    #label.place(relx = 0, rely = 0.25, relwidth=0.05, relheight=0.1)
                    label.grid(column=2, row=row, sticky='EW')

                    label = Tkinter.Label(frame, text=u'%s' % to, anchor='c', width=narrow)
                    #label.place(relx = 0, rely = 0.3, relwidth=0.1, relheight=0.1)
                    label.grid(column=3, row=row, sticky='EW')

                    label = Tkinter.Label(frame, text=u'%s' % mi, anchor='c', width=narrow)
                    #label.place(relx = 0, rely = 0.4, relwidth=0.1, relheight=0.1)
                    label.grid(column=4, row=row, sticky='EW')

                    statVar = Tkinter.StringVar()
                    statVar.set(u'Not started')
                    statLabel = Tkinter.Label(frame, textvariable=statVar, anchor='c', width=16)
                    #statLabel.place(relx = 0, rely = 0.5, relwidth=0.2, relheight=0.1)
                    statLabel.grid(column=5, row=row, sticky='EW')


                    btn = Tkinter.Button(frame, text=u'Render', width=6)
                    #btn.place(relx = 0, rely = 0.7, relwidth=0.15, relheight=0.1)
                    btn.grid(column=6, row=row)
                    self.renderButtons.append(btn)

                    sbtn = Tkinter.Button(frame, text=u'Stop', width=6)
                    #sbtn.place(relx = 0, rely = 0.85, relwidth=0.15, relheight=0.1)
                    sbtn.grid(column=7, row=row) 

                    cmd = partial(self.render, name, start, end, to, mi, statVar, btn, sbtn)
                    btn.config(command=cmd)      

                    row += 1
                index += 1

        # Title row
        label = Tkinter.Label(frames[0], text=u'Scene Path: ', anchor='w', width=12)
        label.grid(column=0, row=0, sticky='EW')
        label = Tkinter.Label(frames[0], text=u'%s' % os.path.dirname(self.sceneVar.get()), anchor='w', width=100)
        label.grid(column=1, row=0, sticky='EW')

        label = Tkinter.Label(frames[0], text=u'Scene: ', anchor='w', width=12)
        label.grid(column=0, row=1, sticky='EW')
        label = Tkinter.Label(frames[0], text=u'%s' % os.path.basename(self.sceneVar.get()), anchor='w', width=80)
        label.grid(column=1, row=1, sticky='EW')
        
        label = Tkinter.Label(frames[0], text=u'Target Path: ', anchor='w', width=12)
        label.grid(column=0, row=2, sticky='EW')
        label = Tkinter.Label(frames[0], text=u'%s' % self.tgtDirVar.get(), anchor='w', width=80)
        label.grid(column=1, row=2, sticky='EW')     

        btn = Tkinter.Button(frames[0], command=renderAll, text=u'Render All', width=wide, anchor='w')
        btn.grid(column=1, row=3)


        # Scroll bar setup
        canvas = Tkinter.Canvas(frames[1], height=800)
        frame = Tkinter.Frame(canvas, background="#ffffff", 
                              highlightbackground="black", 
                              highlightcolor="black", 
                              highlightthickness=1, 
                              bd=0)
        frame.pack(side="left", fill="both", expand=1)#.place(relx = 0, rely = 0, relwidth=1, relheight=1)
        vsb = Tkinter.Scrollbar(frames[1], orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)


        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=1)
        frame_id = canvas.create_window((4,4), window=frame, anchor="nw", width = 900)
        frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(event, canvas))

        # Title row
        label = Tkinter.Label(frame, text=u'Layer Name', anchor='c', width=wide)
        label.configure(font=("Arial", 12, "bold"))
        label.grid(column=0, row=0, sticky='EW')

        label = Tkinter.Label(frame, text=u'Start', anchor='c', width=narrow)
        label.configure(font=("Arial", 12, "bold"))
        label.grid(column=1, row=0, sticky='EW')

        label = Tkinter.Label(frame, text=u'End', anchor='c', width=narrow)
        label.configure(font=("Arial", 12, "bold"))
        label.grid(column=2, row=0, sticky='EW')

        label = Tkinter.Label(frame, text=u'Time out', anchor='c', width=narrow)
        label.configure(font=("Arial", 12, "bold"))
        label.grid(column=3, row=0, sticky='EW')

        label = Tkinter.Label(frame, text=u'Max Idle', anchor='c', width=narrow)
        label.configure(font=("Arial", 12, "bold"))
        label.grid(column=4, row=0, sticky='EW')          

        label = Tkinter.Label(frame, text=u'Status', anchor='c', width=narrow)
        label.configure(font=("Arial", 12, "bold"))
        label.grid(column=5, row=0, sticky='EW')        

        populate(frame)

        frames[0].config(width=frame_width)#, height=rlFrameHeight)
        frames[1].config(width=frame_width)#, height=rlFrameHeight)
        canvas.config(width=frame_width)


    def render(self, layer=None, start=None, end=None, 
               timeOut=None, maxIdle=None, statVar=None,
               btn=None, sbtn=None):
        self.validateRenderJobsUIData()

        s = '.'
        logName = s.join([self.shot, layer, 'render.log'])

        temp = self.imUI.get().split('/')[:-1]
        customPath = ''
        for each in temp:
            customPath += '/' + each.replace('<RenderLayer>', layer)

        logFile = self.tgtDirVar.get() + customPath
        logFile = logFile
        logFile += '/' + logName

        # Define settings
        settings = {'log':logFile,
                    'rd':self.tgtDirVar.get(),
                    'layer':layer,
                    'scene':self.sceneVar.get(),
                    'start':start,
                    'end':end,
                    'res':self.percentResUI.get(),
                    'cam':self.cameraVar.get(),
                    'shot':self.shot,
                    'render':self.mayaVar.get(),
                    'im':self.imUI.get(),
                    'fnc':self.fncUI.get(),
                    'statVar':statVar,
                    'pad':self.padUI.get(),
                    'by':self.bUI.get(),
                    'timeOut':timeOut,
                    'maxIdle':maxIdle,
                    'cpuMin':self.thUI.get(),
                    'btn':btn,
                    'sbtn':sbtn}

        if int(self.rtCB.get()):
            settings['rt'] = self.rtFld.get() 
        else:
            settings['rt'] = 0
            
        # Auto restart check box state
        settings['auto'] = int(self.autoCB.get())

        # Issue render command
        self.mrRender.render(settings)

    def validateRenderJobsUIData(self):
        if not self.tgtDirVar.get():
            tkMessageBox.showwarning(
                "Missing Information",
                'Must select a target directory for renders.' )
            raise Exception('Must select a target directory for renders.')             

        if self.cameraVar.get() == '------':
            tkMessageBox.showwarning(
                "Missing Information",
                'Must select a valid camera.' )    
            raise Exception('Must select a valid camera.')
    