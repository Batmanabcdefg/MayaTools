from threading import Thread
from datetime import datetime
import shlex
from subprocess import call, Popen, PIPE


def timer(typ=None, startTime=None, frames=None):
    if typ == 'start':
        t = datetime.now()
        print("--- Render Start: %s" % t)
        return t

    if typ == 'end':
        et = datetime.now()
        dt = (et - startTime)
        result = "--- Render Start: %s\n" % startTime
        result += "--- Render End: %s\n" % et
        result += "--- Runtime: %s\n" % dt
        if frames:
            result += "--- Avg. per Frame: %s\n" % (dt/frames)

        return result

def renderCmd(options=None):
    options = options

    for layer in options['layers']:
        cmd = '"%s" ' % options['app']
        cmd += '-v 6 -proj "%s" ' % options['proj']
        if options['enableLog']:
            cmd += '-log "%s" ' % (options['logFileVar'])
        cmd += '-rd "%s" -r mr -im "%s" ' % (options['rd'], options['naming'])
        cmd += '-aml -at -art -fnc "name.#.ext" -rl "%s" -of "exr" ' % layer
        cmd += '-s %s -e %s -b %s -pad 4 -skipExistingFrames %s -cam "%s" ' % (options['start'], options['end'], options['step'], options['skip'], options['cam'])
        cmd += '-x %s -y %s -percentRes %s "%s"' % (options['res'][0], options['res'][1], options['percent'], options['scene'])

        yield cmd

def runJob(cmd, frames):
    start_time = timer(typ='start')
    try:
        cmd = shlex.split(cmd)

        code = call(cmd)
        #proc = Popen(cmd)
        #proc.wait()
        #code = proc.returncode

    except Exception, e:
        print("Error: %s" % e)

    finally:
        result = timer(typ='end', startTime=start_time, frames=frames)
        return "\n--- Render complete. Exit Status: %s\n" % code + result
