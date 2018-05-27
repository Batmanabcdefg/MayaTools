import threading
import time
import random

import Job

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active=[]
        self.lock=threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
    def numActive(self):
        with self.lock:
            return len(self.active)
    def __str__(self):
        with self.lock:
            return str(self.active)
        
def worker(pool, name, start, end):
    name=threading.current_thread().name
    pool.makeActive(name)
    print '\nNow running: %s' % str(pool)
    j = Job.Job(name=name)
    cmd = j.renderJob(start=start, end=end)
    j.run(cmd)
    pool.makeInactive(name)

if __name__=='__main__':
    frames = 200
    count = 0
    poolA=ActivePool()
    
    jobs=[]
    for i in range(frames):
        frame = i+1
        jobs.append(
            threading.Thread(target=worker, name='Frame_{0}'.format(frame),
                             args=(poolA, str(i), frame, frame)))
    for i in range(8):
        jobs[i].daemon=True
        jobs[i].start()
        count += 1
        
    while threading.activeCount()>1:
        if threading.activeCount()<8:
            if count < frames:
                jobs[count].daemon=True
                jobs[count].start()
                count += 1
        for j in jobs:
            try:
                j.join(1)
                print 'Pool-threads active: {0}'.format(poolA.numActive())
            except:
                pass