import pymel.core as pm
fluid = 'FG_Smoke'

def connect(fluid=None):
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
on = 250
off = 251
rate= 100
for each in pm.ls(sl=1):
    pm.currentTime( on, edit=True )
    each.rate.set(rate)
    pm.setKeyframe( each, attribute='rate', t=[on] )


    pm.currentTime( off, edit=True )
    each.rate.set(0)
    pm.setKeyframe( each, attribute='rate', t=[off] )

# Zero emitters
for each in pm.ls(sl=1):
    each.rate.set(0)

# Zero emitters
for each in pm.ls(sl=1):
    each.speedMethod.set(1)
    each.directionalSpeed.set(50)
