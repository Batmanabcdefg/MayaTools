import pymel.core as pm

def connect_selected():
    '''
    Select fluid container and emitters
    Connect emitters to fluid
    '''
    sel = pm.ls(sl=1)
    fluid = sel[0]
    emitters = sel[1:]
    for each in emitters:
        pm.connectDynamic(fluid, em=each, d=True)
        pm.connectDynamic(fluid, em=each)


# Set keys on emitters
def selected_rate_switch(  start=None,
                        startVal=None,
                        end=None,
                        endVal=None):
    for each in pm.ls(sl=1):
        each.rate.set(startVal)
        pm.setKeyframe( each, attribute='rate', t=[start] )
        each.rate.set(endVal)
        pm.setKeyframe( each, attribute='rate', t=[end] )

def set_selected(rate=None, speedMethod=None, directionalSpeed=None):
    for each in pm.ls(sl=1):
        if rate: each.rate.set(rate)
        if speedMethod: each.speedMethod.set(speedMethod)
        if directionalSpeed: each.directionalSpeed.set(directionalSpeed)

def swirl_selected(direction=None, start=None, step=None):
    '''
    Swirl animation for selected emitter
    '''
    def set(obj=None, x=None, y=None, time=None):
        obj.directionX.set(x)
        obj.directionY.set(y)
        pm.setKeyframe( obj, attribute='directionX', t=[time] )
        pm.setKeyframe( obj, attribute='directionY', t=[time] )

    # Animation
    direction = direction
    step = step
    for each in pm.ls(sl=1):
        start = start
        # Forward
        set(each, (1*direction), 0, start)
        # Up
        start += step
        set(each, 0, (1*direction), start)
        # Back
        start += step
        set(each, (-1*direction), 0, start)
        # Down
        start += step
        set(each, 0, (-1*direction), start)
        # Forward
        start += step
        set(each, (1*direction), 0, start)
