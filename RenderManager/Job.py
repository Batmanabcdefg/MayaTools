import time
import random
from threading import Thread
import shlex
from subprocess import Popen


'''
Render job
'''
class Job(object):
    def __init__(self, name=None):
        self.name = name
        self.threads = []        # List of threads
        self.job_status = 'ip'
        self.timeout = 100       # Max time per thread
        self.frames = {}         # Frames and their respective status
        self.max_threads = 8     # Max number of threads that exists at one time
        self.num_frames = 200    # Number of frames to render   
        self.offset = 0
        self.by_frame = 1
    
    def timer(self, typ=None, startTime=None):
        if typ == 'start':
            return time.time()
        if typ == 'end':
            seconds = (time.time() - startTime)
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            print("--- Runtime: %d:%02d:%02d h:m:s" % (h, m, s))
    
    def options(self):
        options = {}
        logDir = "/Users/mauricio/Desktop/SmokeAssets/Logs"
        log = "Render.MayaRender.log"
        options['logFileVar'] = logDir + '/' + log
        
        options['rd'] = "/Users/mauricio/Desktop/SmokeAssets/Images"
        options['scene'] = "/Users/mauricio/Desktop/SmokeAssets/AmbientCloud_01.ma" 
        
        options['app'] = "/Applications/Autodesk/maya2014/Maya.app/Contents/bin/Render"
        options['proj'] = "/Users/mauricio/Desktop/SmokeAssets"
        
        options['layer'] = "masterLayer"    
        options['res'] = (1920, 1080)
    
        options['percent'] = 50
        options['cam'] = "SHOTCAM"    
        
        return options  
    
    def renderJob(self, start=None, end=None, logFile=1):
        options = self.options() 
        
        cmd = '"%s" ' % options['app']
        cmd += '-verb -proj "%s" ' % options['proj']
        if logFile:
            cmd += '-log "%s" ' % (options['logFileVar'])
        cmd += '-rd "%s" -r mr -im "<RenderLayer>/<RenderLayer>" ' % options['rd']
        cmd += '-aml -at -art -fnc "name.#.ext" -rl "%s" -of "exr" ' % options['layer']
        cmd += '-s %s -e %s -b 1 -pad 3 -skipExistingFrames 1 -cam "%s" ' % (start, end, options['cam'])
        cmd += '-x %s -y %s -percentRes %s "%s"' % (options['res'][0], options['res'][1], options['percent'], options['scene'])
    
        return shlex.split(cmd)   

    def run(self, cmd):
        start_time = self.timer(typ='start')
        
        try:
            proc = Popen(cmd)
            proc.wait()
            
        except Exception, e:
            print("Error %s" % e)
            
        finally:
            print("\n--- Render complete. Exit Status: %s" % proc.returncode)
            self.timer(typ='end', startTime=start_time)