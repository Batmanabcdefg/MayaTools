from subprocess import call

'''
cd Desktop\SAI_Tests
"C:\Program Files\Autodesk\Maya2014\bin\mayapy.exe" mr_render.py
/Applications/Autodesk/maya2015/Maya.app/Contents/bin/mayapy mr_render.py
'''


settings = {'log':'/Users/mauricio/Desktop/ThemGreeks/Rendering/DET0040/render.log',
            'rd':'/Users/mauricio/Desktop/ThemGreeks/Rendering/DET0040',
            'layer':'magasBlow_smoke',
            'scene':'/Users/mauricio/Desktop/ThemGreeks/working_copy/VFX/DET/DET0040/in_progress/DET.0040.cigSmoke.fx.ma',
            'start':'187',
            'end':'187',
            'res':'75',
            'cam':'animCamDET0040',
            'shot':'DET0040',
            'os':'mac'}

def render(settings=None):
    ''' Render scene using given settings '''
    if settings['os'] == 'mac':
        cmd = ['/Applications/Autodesk/maya2015/Maya.app/Contents/bin/Render']
    elif settings['os'] == 'win':
        cmd = ['C:/Program Files/Autodesk/Maya2014/bin/Render']
    cmd.extend( ['-verb', '-log', settings['log'], '-proj', settings['rd']] )
    cmd.extend( ['-rd', settings['rd'], '-r', 'mr'] )
    cmd.extend( ['-im', settings['shot']+'.<RenderLayer>', '-aml', '-at', '-art', '-fnc', 'name.#.ext'] )
    cmd.extend( ['-rl', settings['layer'], '-of', 'exr'] )
    cmd.extend( ['-s', settings['start'], '-e', settings['end'], '-b', '1', '-pad', '3'] )
    cmd.extend( ['-skipExistingFrames', '1', '-cam', settings['cam']] )
    cmd.extend( ['-x', '1920', '-y', '1080', '-percentRes', settings['res']] )
    cmd.extend( [settings['scene']] )

    # Run the command
    try:
        #print cmd
        p = call(cmd)
    except Exception,e:
        raise Exception(e)

if __name__ == '__main__':
    render(settings)
