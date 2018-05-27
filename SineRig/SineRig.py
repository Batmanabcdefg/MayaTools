'''
import sys
path = '/users/mauricio/Google Drive'
if path not in sys.path:
    sys.path.insert(0,path)
    
from SineRig import SineRig_ui
reload( SineRig_ui )
SineRig_ui.SineRig_ui()
'''


import pymel.core as pm


class SineRig(object):
    '''
    Create a sine rig that is intuitive to animate.
    Uses expressions to animate joint chain rotations
    based on attributes created by this tool.
    '''
    def __init__(self,
                 control=None,
                 name=None,
                 baseJnt=None,
                 tipJnt=None):
        if not control or not name or not baseJnt or not tipJnt:
            raise(Exception('Must pass in: control, name, baseJnt, tipJnt'))

        joints = self.getJoints(baseJnt=baseJnt, tipJnt=tipJnt)
        numJnts = len(joints)

        self.createAttrs(control=control, name=name, numJnts=numJnts)

        effect_inc = 100.0/float(numJnts)

        self.createJointAttrs(joints=joints, effect_inc=effect_inc)

        self.createTimeNetwork(control=control, name=name, numJnts=numJnts)

        pm.select(clear=True)
        count = 1
        for jnt in joints:
            try:
                prnt = pm.listRelatives(jnt, p=1)[0]
            except Exception:
                prnt = None
            prnt_grp, sine_grp = self.createGroups(name=name, jnt=jnt)
            pm.parent(jnt, sine_grp)
            pm.parent(sine_grp, prnt_grp)
            if prnt:
                pm.parent(prnt_grp, prnt)

            self.createNetwork(control=control,
                               name=name,
                               sine_grp=sine_grp,
                               jnt=jnt,
                               axis='z',
                               count=count,
                               numJnts=numJnts)

            self.createNetwork(control=control,
                               name=name,
                               sine_grp=sine_grp,
                               jnt=jnt,
                               axis='y',
                               count=count,
                               numJnts=numJnts)

            self.createFkControl(name=name, jnt=jnt)

            count += 1

    def createFkControl(self, name=None, jnt=None):
        ''' Create a curve, parent shape to joint, lock translations. '''
        temp = pm.circle(name='%s_%s_FK_ctrl' % (name, jnt))
        pm.delete(pm.parentConstraint(jnt, temp[0], mo=0))
        shape = temp[0].getShape()
        pm.parent(shape, jnt, shape=True, r=1)
        pm.delete(temp[0])

    def createAttrs(self, control=None, name=None, numJnts=None):
        '''SineRig attributes on control'''
        # { 'attr' : [min, max, default], ...}
        attrs = {'amplitude': [0.001, 10, 1],
                 'speed': [0, 100, 2],
                 'time_offset': [0, 100, 1],
                 'z_rotation': [0, 1, 0.2],
                 'y_rotation': [0, 1, 0],
                 'fwd_limit': [1, 180, 5],
                 'back_limit': [-180, -1, -20],
                 'effect': [0, 10, 1],
                 'time_sine_value': [],
                 'switch_count': [1, numJnts, 1],
                 'last_frame': []}

        pm.addAttr(control, ln=name, k=1)
        pm.setAttr('%s.%s' % (control, name), l=1)

        orderedList = ['amplitude', 'speed', 'time_offset', 'z_rotation',
                       'y_rotation', 'fwd_limit', 'back_limit',
                       'effect', 'time_sine_value', 'switch_count', 'last_frame']

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

    def getJoints(self, baseJnt=None, tipJnt=None):
        ''' Return: [baseJnt, ..., tipJnt] '''
        pm.select(baseJnt, r=1, hi=1)

        joints = []
        for j in pm.ls(sl=1, type='joint'):
            if j == tipJnt:
                joints.append(j)
                break
            joints.append(j)

        return joints

    def createJointAttrs(self, joints=None, effect_inc=None, direction=None):
        ''' Stamp each joint with sine_effect_value attribute and value '''
        effect = effect_inc
        count = 0
        for jnt in joints:
            if count > 0:
                direction = -1
            else:
                direction = 1
            pm.addAttr(jnt, ln='sine_effect_value', k=1)
            pm.setAttr('%s.sine_effect_value' % jnt, effect, l=1)
            pm.addAttr(jnt, ln='sine_direction', k=1)
            pm.setAttr('%s.sine_direction' % jnt, direction, l=0)
            effect += effect_inc
            count += 1

    def createGroups(self, name=None, jnt=None):
        ''' Create Parent and Sine groups above joint'''
        pGrp = pm.group(name='%s_%s_prnt_grp' % (name, jnt), em=True)
        sGrp = pm.group(name='%s_%s_sine_grp' % (name, jnt), em=True)

        pm.delete(pm.parentConstraint(jnt, pGrp, mo=0))
        pm.delete(pm.parentConstraint(jnt, sGrp, mo=0))

        return pGrp, sGrp

    def createTimeNetwork(self, control=None, name=None, numJnts=None):
        '''
        Mel expression that gets base value for sine rig.
        Uses control attributes: amplitude, speed
        Results in control attribute: time_sine_value
        Also sets up direction switch counter for offset motion.
        '''
        s = "// Expression: amplitude * ( sin(time*speed) )\n"
        s += 'float $last_frame = %s.last_frame;\n' % control
        s += 'float $offset = %s.time_offset;\n' % control
        s += "float $amp = %s.amplitude;\n" % control
        s += "float $speed = %s.speed;\n" % control
        s += "%s.time_sine_value =  $amp * sin((time + $offset) * $speed);\n" % control

        s += '\n// Switch counter incrementation\n'
        s += 'float $sw_count = %s.switch_count;\n' % control
        s += 'if($offset > 0)\n'
        s += '{  if((`currentTime -query` % $offset) == 0)\n'
        s += '   {  if( $last_frame < `currentTime -query` )\n'
        s += '      { %s.switch_count = $sw_count + 1;}\n' % control
        s += '      else{ %s.switch_count = $sw_count - 1;}\n' % control
        s += '   }\n'
        s += '   if($sw_count > %s)\n' % numJnts
        s += '   { %s.switch_count = 1; }\n' % control
        s += '}\n'

        s += '\n// Store value in Last_Frame\n'
        s += '%s.last_frame = frame;\n' % control

        pm.expression(name='%s_SineRig_exp' % name, s=s)

    def createNetwork(self,
                      control=None,
                      name=None,
                      sine_grp=None,
                      jnt=None,
                      axis=None,
                      count=None,
                      numJnts=None):
        '''
        Use attributes:
        time_sine_value, z_rotation or y_rotation,
        fwd_limit, back_limit, effect, count, numJnts

        Create expression to animate sine_grp rotations.
        '''
        s = '//Expression to drive %s sine_grp.rotate%s\n' % (jnt, axis)
        s += 'float $sw_count = %s.switch_count;\n' % (control)
        s += 'float $sine = %s.time_sine_value;\n' % (control)
        s += 'float $amplitude = %s.amplitude;\n' % (control)
        s += 'float $offset = %s.time_offset;\n' % (control)
        s += 'float $fwd_limit = %s.fwd_limit;\n' % (control)
        s += 'float $back_limit = %s.back_limit;\n' % (control)
        s += 'float $effect = %s.effect;\n' % (control)
        s += 'float $effect_val = %s.sine_effect_value;\n' % jnt
        s += 'float $direction = %s.sine_direction;\n' % jnt
        s += 'float $temp1 = 0;\n'
        s += 'float $temp2 = 0;\n'

        if axis == 'z':
            s += 'float $r_value = %s.z_rotation;\n\n' % control
        else:
            s += 'float $r_value = %s.y_rotation;\n\n' % control

        s += '$temp1 = $sine;\n'
        s += '\n// Remap range to user set min / max range\n'
        s += 'float $old_range = ($amplitude - (-$amplitude));\n'
        s += 'float $new_range = ($fwd_limit - $back_limit);\n'
        s += '$temp2 = (((($temp1 - (-$amplitude)) * $new_range)/$old_range)' + \
            '+ $back_limit) * $r_value;\n'

        s += '\n// Apply direction section\n'
        # s += '$temp1 = $temp1 * $direction;\n'
        # s += '$temp2 = $temp2 * $direction;\n'

        s += '\n// Final connection to rotation of sine_grp\n'
        if axis == 'z':
            s += '\n// Change Direction value on joint only in z exp, not y.\n'
            s += 'if($sw_count == %s)\n' % count
            s += '{ %s.sine_direction = $direction * -1; }\n' % jnt

            s += 'if($effect>0){ // Dampen effect\n'
            s += '    %s.rotateZ = $temp2 * ($effect_val/100) * $effect;}\n' \
                % (sine_grp)
            s += 'else{\n'
            s += '    %s.rotateZ = $temp1 * $r_value;}\n' % (sine_grp)
        else:
            s += 'if($effect>0){ // Dampen effect\n'
            s += '     %s.rotateY = $temp2 * ($effect_val/100) * $effect;}\n' \
                % (sine_grp)
            s += 'else{\n'
            s += '    %s.rotateY = $temp1 * $r_value;}\n' % (sine_grp)

        pm.expression(name='%s_%s_%s_SineRig_exp' % (name, jnt, axis),
                      s=s)


