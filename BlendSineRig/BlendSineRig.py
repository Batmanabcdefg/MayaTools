'''
import sys
path = '/users/mauricio/Google Drive'
if path not in sys.path:
    sys.path.insert(0,path)

from BlendSineRig import BlendSineRig_ui
reload( BlendSineRig_ui )
BlendSineRig_ui.BlendSineRig_ui()
'''


import pymel.core as pm


class BlendSineRig(object):
    '''
    Create a sine rig that is intuitive to animate.
    Uses joints on curve and blendshapes on curve
    to achieve sinuous motion
    '''
    def __init__(self,
                 control=None,
                 name=None,
                 curve=None,
                 numJnts=None,
                 fwdBackCrvs=None,
                 sideToSideCrvs=None):

        pm.select(control, r=1)
        control = pm.ls(sl=1)[0]

        pm.select(curve, r=1)
        curve = pm.ls(sl=1)[0]

        joints = self.createJoints(name=name, curve=curve, num=numJnts)

        self.createFKControls(name=name, joints=joints)

        self.createAttrs(control=control, name=name)

        fwd_blendshape = pm.blendShape(fwdBackCrvs,
                                       curve, ib=1,
                                       name='fwd_%s_blendshape' % name)[0]

        side_blendshape = pm.blendShape(sideToSideCrvs,
                                        curve, ib=1,
                                        name='side_%s_blendshape' % name)[0]

        self.setupTimeSineExp(control=control)

        pm.connectAttr('%s.time_sine' % control,
                       '%s.%s' % (fwd_blendshape, fwdBackCrvs[-1]), f=1)

        pm.connectAttr('%s.time_sine' % control,
                       '%s.%s' % (side_blendshape, sideToSideCrvs[-1]), f=1)

        pm.connectAttr('%s.fwd_back' % control,
                       '%s.envelope' % fwd_blendshape)

        pm.connectAttr('%s.side_to_side' % control,
                       '%s.envelope' % side_blendshape)

    def createJoints(self, name=None, curve=None, num=None):
        ''' Create groups on curve. '''
        num = float(num)
        joints = []
        param_increment = 1.0/num
        param = 0
        curveshape = curve.getShape()
        prnt = []
        for i in range(int(num)):
            pm.select(clear=1)

            # create joint
            jnt = pm.joint(name='%s%s_jnt' % (name, i))
            joints.append(jnt)

            # attach to curve
            poci = pm.createNode('pointOnCurveInfo')
            pm.connectAttr('%s.ws' % curveshape, '%s.inputCurve' % poci, f=1)
            pm.connectAttr('%s.position' % poci, '%s.translate' % jnt, f=1)
            pm.setAttr('%s.turnOnPercentage' % poci, 1)
            pm.setAttr('%s.parameter' % poci, param)

            pm.disconnectAttr('%s.position' % poci, '%s.translate' % jnt)
            pm.delete(poci)

            if len(prnt):
                pm.parent(jnt, prnt[-1])

            prnt.append(jnt)
            param += param_increment

        return joints

    def createFKControls(self, name=None, joints=None):
        ''' Create a curve, parent shape to joint. '''
        for jnt in joints:
            temp = pm.circle(name='%s_%s_tweak_ctrl' % (name, jnt))
            pm.delete(pm.parentConstraint(jnt, temp[0], mo=0))
            shape = temp[0].getShape()
            pm.parent(shape, jnt, shape=True, r=1)
            pm.delete(temp[0])

    def createAttrs(self, control=None, name=None):
        '''BlendSineRig attributes on control'''
        # { 'attr' : [min, max, default], ...}
        attrs = {'speed': [0, 10, 24],
                 'fwd_back': [0, 1, 1],
                 'side_to_side': [0, 1, 0.1],
                 'time_sine': []}

        pm.addAttr(control, ln=name, k=1)
        pm.setAttr('%s.%s' % (control, name), l=1)

        orderedList = ['speed', 'fwd_back',
                       'side_to_side', 'time_sine']

        for attr in orderedList:
            if len(attrs[attr]):
                pm.addAttr(control,
                           ln=attr,
                           minValue=attrs[attr][0],
                           maxValue=attrs[attr][1],
                           defaultValue=attrs[attr][2],
                           k=True)
            else:
                pm.addAttr(control,
                           ln=attr,
                           k=True)

    def setupTimeSineExp(self, control=None):
        ''' Create expression that generates si n(time)
        value and display it on an attribute to drive
        blendshape expression connect to blendshapes'''
        s = 'float $speed = %s.speed;\n' % control
        s += 'float $val = float((abs((frame/$speed) % 10.0))/10.0);\n'
        s += '%s.time_sine = $val;\n' % (control)

        pm.expression(name='%s_timeSine_exp', s=s)
