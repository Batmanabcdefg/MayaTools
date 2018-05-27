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

from subprocess import Popen
import tkMessageBox
import threading
from Queue import Queue
from threading import Timer
from functools import partial
import os
import time
import signal

try:
    import psutil
except:
    tkMessageBox.showwarning(
        "Missing Python Library",
        "You need to install 'psutil' for this tool to work properly." ) 
    raise Exception('Missing dependency: psutil python library')
   

class Render():
    '''
    Object with methods used to structure and call a Maya batch render via Job Object
    
    Used by mr_render_ui.py
    '''
    def __init__(self):
        self.q = Queue()
        t = threading.Thread(target=self.monitorQueue)
        t.daemon = True
        t.start()
        
    def monitorQueue(self):
        print 'Starting queue monitor...'
        while True:
            job = self.q.get()
            job.daemon = True          
            job.start()
            job.join()
            self.q.task_done()
    
    def addToQueue(self, job):
        self.q.put(job)
    
    def renderSettings(self, scene=None):
        f = open(os.path.dirname(__file__) + '/render_settings.mel', 'r')
        lines = f.readlines()
        f.close()
    
        return lines
    
    def get_camera_renderLayers(self, scene=None):
        # Open the file
        f = open(scene, 'r')
        lines = f.readlines()
        f.close()
    
        render_layers = []
        cameras = []
        for line in lines:
            if 'createNode renderLayer' in line and ':' not in line:
                if 'Manager' not in line:
                    render_layers.append(line.split('"')[1])
            if 'createNode camera' in line:
                l = line.split()[-1].split('"')[1]
                cameras.append(l)
            if 'animCam' in line and '-r' in line:
                l = line.split()
                for elem in l:
                    if 'animCam' in elem and 'RN' not in elem and '.ma' not in elem:
                        if '"' in elem:
                            elem = elem.split('"')[1]
                        cameras.append(elem)
    
        cameras = list(set(cameras))
    
        return [cameras, render_layers]    
    
    def formatCmd(self, settings=None):
        # Format render command
        #-sampling 0
        #-unifiedQuality 1.0
    
        cmd = [settings['render']]
        cmd.extend( ['-verb', '-log', settings['log'], '-proj', settings['rd']] )
        cmd.extend( ['-rd', settings['rd'], '-r', 'mr'] )
        cmd.extend( ['-im', settings['im'], '-aml', '-at', '-fnc', settings['fnc']] )
        if settings['rt']:
            cmd.extend( ['-rt', settings['rt']] )
        else:
            cmd.extend( ['-art'] )
        cmd.extend( ['-rl', settings['layer'], '-of', 'exr'] )
        cmd.extend( ['-s', settings['start'], '-e', settings['end']] )
        cmd.extend( ['-b', settings['by'], '-pad', settings['pad']] )
        cmd.extend( ['-skipExistingFrames', '1', '-cam', settings['cam']] )
        cmd.extend( ['-x', '1920', '-y', '1080', '-percentRes', settings['res']] )
    
        # Add preRender mel for render settings to the command
        for line in self.renderSettings():
            l = line.rstrip()
            if l != '':
                cmd.extend( ['-preRender', l] )
    
        cmd.extend( [settings['scene']] ) 
        
        return cmd
    
    def render(self, settings=None):
        ''' Send Render job with given settings to queue '''
        
        try:
            var = settings['statVar'].get()
            blockStates = ['Started','Queued']
            if var in blockStates:
                tkMessageBox.showwarning(
                    "Start Job",
                    "Cannot start Job becasue it is already %s" % var )
                return 
            
            # Create Job thread
            p = Job(settings['statVar'], 
                    self.formatCmd(settings),
                    settings['timeOut'],
                    settings['maxIdle'],
                    settings['cpuMin'],
                    settings['btn'],
                    settings['sbtn'],
                    os.path.dirname(settings['log']),
                    settings['log'],
                    settings['layer'],
                    settings['auto'])
 
            # Add to Queue
            settings['statVar'].set('Queued')
            self.addToQueue(p)
            

        except Exception,e:
            print e
            settings['statVar'].set('Error')
            raise Exception(e)
 
 
class Job(threading.Thread):
    '''
    Run a command via Thread and monitor CPU and Job via JobMonitor 
    and CpuMonitor Objects. Also starts a threading.Timer() to kill
    the job if Time Out time exceeded.
    
    @param statVar Tkinter UI StringVar for the render Job status
    @param cmd Maya batch render command
    @param timeOut Max time for thread to live
    @param maxIdle Max time for CPUs to be idle
    @param cpuMin If CPU usage % drops below this, cpu considered idle
    @param btn Render button
    @param sbtn Stop button
    @param tgtPath Directory where images will be created
    @param log Path/log file name
    @param layer Render layer name
    @param auto Auto restart check box state as int
    '''        
    def __init__(self, statVar, cmd, timeOut, 
                 maxIdle, cpuMin, button, 
                 stopBtn, tgtPath, log, layer, auto):
        threading.Thread.__init__(self)
        
        self.statVar = statVar
        self.cmd = cmd
        self.timeOut = timeOut
        self.maxIdle = maxIdle
        self.cpuMin = cpuMin
        self.button = button
        self.stopBtn = stopBtn
        self.tgtPath = tgtPath
        self.log = log
        self.layer = layer
        self.auto = auto
        
        self.proc = None
        self.timer = None
        self.cpuMonitor = None
        self.jobMonitor = None
        self.statMonitor = None
        
    def createLogFile(self):
        # Create the log file
        try:
            path = os.path.dirname(self.log)
            if not os.path.exists(path):
                os.makedirs(path)
    
            f = open(self.log, 'w')
            f.close()
            msg = 'Created log file: ', self.log
            print msg
    
        except Exception, e:
            self.statVar.set('Error: See terminal')
            print e
            raise Exception(e)
        
    def removeSmallFiles(self, directory):
        # Remove 128 byte files from directory
        filenames = None
        for dirname, dirnames, filenames in os.walk(directory):
            filenames = filenames
            break
        
        files = [os.path.join(directory, f) for f in filenames]
        for f in files:
            info = os.stat(f)
            if info.st_size == 128:
                os.remove(f)
            
    def run(self):
        self.runCmd()
        
    def runCmd(self):
        self.statVar.set('Started')
        self.createLogFile()
        self.removeSmallFiles(self.tgtPath)
        self.proc = psutil.Popen(self.cmd)
        
        # Ensure we only have one each of the following for this job
        if not self.timer:
            self.timer = Timer(float(self.timeOut)*60, 
                               self.timedOutExceeded)
            self.timer.daemon = True
            self.timer.start()
            
        if not self.cpuMonitor:
            self.cpuMonitor = CpuMonitor(self.statVar, 10, 
                                         float(self.maxIdle)*60, self, 
                                         self.cpuMin)
            self.cpuMonitor.daemon = True
            self.cpuMonitor.start()
            
        if not self.jobMonitor:
            self.jobMonitor = JobMonitor(self)
            self.jobMonitor.daemon = True
            self.jobMonitor.start()   
        
        if self.auto:
            if not self.statMonitor:
                self.statMonitor = StatMonitor(self)
                self.statMonitor.daemon = True
                self.statMonitor.start()        
    
        # Configure stop button command
        stopCmd = partial(self.infanticide, 'Stopped')
        self.stopBtn.config(text='Stop', command=stopCmd)
        
        # Block this thread until process completes
        self.proc.wait()
        
    def timedOutExceeded(self):
        self.infanticide('Timed out')
        return

    def infanticide(self, msg):
        ''' 
        Kill Popen pid and all it's children.
        Also stop monitors.
        '''
        try:
            parent = psutil.Process(self.proc.pid)
        except psutil.NoSuchProcess:
            return
        children = parent.children(recursive=True)
        for p in children:
            self.statVar.set(msg)
            p.kill()
        parent.kill()
        
        self.jobMonitor.monitor = False
        self.cpuMonitor.monitor = False
        if self.auto:
            self.statMonitor.monitor = False
                
class JobMonitor(threading.Thread):
    def __init__(self, job):
        '''
        Monitor Job Popen process via poll(). Update UI with appropriate status.
        
        @param job Job object (Thread) that is in charge of batch render
        '''
        threading.Thread.__init__(self)
        self.job = job
        self.monitor = True
        
    def run(self):
        self.monitorJob()
        
    def monitorJob(self):
        # Monitor job every three seconds
        while self.monitor:
            time.sleep(3)
            # Get the currently displayed job status
            varVal = self.job.statVar.get()            

            # Check the Popen process state
            state = self.job.proc.poll()
            
            if varVal in ['Timed out','Stopped']:
                print "JobMonitor ending for %s job." % self.job.layer
                return
            
            elif state == None: # None = Still running
                continue
            
            elif state == 0:
                self.job.statVar.set('Render Complete')
                print "JobMonitor ending for %s job. Render complete." % self.job.layer
                return
            
            else:
                # Display the status
                self.job.infanticide('Status: %s' % str(state))
                print "JobMonitor ending for %s job. An error has occured." % self.job.layer
                return                
                
        print "JobMonitor Stopped for %s job." % self.job.layer
        return        
            

class CpuMonitor(threading.Thread):
    '''
    Monitor system cpu. Kill job if max idle time is exceeded.
    
    @param statVar Tkinter UI StringVar for the render Job status
    @param poll Time interval in seconds to be checking CPU usage
    @param maxIdle Maximum amount of time that CPU usage can be below threshold
    @param job Job object (Thread) that is in charge of batch render
    @param minCPU If CPU usage % drops below this, cpu considered idle
    '''
    def __init__(self, statVar, poll, maxIdle, job, minCPU):
        threading.Thread.__init__(self)
        self.statVar = statVar
        self.job = job
        self.minCPU = float(minCPU)
        self.maxIdle = float(maxIdle)
        self.poll = poll
        self.monitor = True

    def run(self):
        while self.monitor:
            time.sleep(self.poll)
            state = self.job.proc.poll()
            msg = 'Status:' + str(state)
            if state == 0:
                print "CpuMonitor ending for %s job." % self.job.layer
                return
            elif state == None:
                print "Checking CPUs for %s job." % self.job.layer
                self.checkCPU()
            else:
                print "CpuMonitor ending for %s job." % self.job.layer
                return
        print "CpuMonitor stopped for %s job." % self.job.layer
        return
    
    def cpuPercent(self):
        psutil.cpu_percent()
        time.sleep(0.2)
        return psutil.cpu_percent()

    def checkCPU(self):
        '''
        Check cpu usage three times every 1/20th of max idle time
        If usage below threshold all 20 times, conclude that 
        the process is idle and terminate it.
        '''
        check_freq = 20.0
        count = 0
        check = 0
        inc = self.maxIdle / check_freq
        usage = float(self.cpuPercent())
        print 'CPU Usage:', usage
        if usage < self.minCPU:
            while count < check_freq:
                state = self.job.proc.poll()
                if state != None:
                    print "CpuMonitor ending for %s job." % self.job.layer
                    return
                time.sleep(inc)
                #print 'Idle Check %s' % str(count + 1) 
                usage = float(self.cpuPercent())
                #print 'CPU usage: ', usage
                if usage < self.minCPU:
                    check += 1
                count += 1
                
            # If every check was below min threshold and 
            # the proces is still running, terminate it
            if check == check_freq:
                state = self.job.proc.poll()
                if state == None:
                    self.job.infanticide('Max idle exceeded.')


class StatMonitor(threading.Thread):
    def __init__(self, job):
        '''
        Monitor Job Status. If not: Started, Queued, Stopped, Render Complete,
        re-invoke the Render button.
        
        @param job Job object (Thread) that is in charge of batch render
        '''
        threading.Thread.__init__(self)
        self.job = job
        self.monitor = True
        
    def run(self):
        self.monitorStatus()
        
    def monitorStatus(self):
        # Monitor job every three seconds
        while True:
            #time.sleep(3)
            # Get the currently displayed job status
            if self.job.statVar.get() not in ['Started','Queued', 'Stopped', 'Render Complete']:
                self.job.button.invoke()
                print "StatMonitor ending for %s job." % self.job.layer
                return
            
            if not self.monitor:
                break
            
        print "StatMonitor stopped for %s job." % self.job.layer
        return 