'''
With influences point constrained to curves setup:
- Create duplicate of the curve
- Name the duplicate based on prefix input by user
- Crete blendshape named using prefix
- SDK to multiAxis attr
'''
import pymel.core as pm

multiAxisAttr = 'rt_shoulder_jacket_inf_cnt.RtShldr_u'

crv = pm.ls(sl=1)[0]
name=crv.name().replace('_curve','_back_crv')
dup = pm.duplicate(crv)[0]
dup.rename(name)
bs = pm.blendShape(dup,crv,n='%sBS'%name)[0]

#off
pm.setDrivenKeyframe( bs, at='%s'%name, cd=multiAxisAttr, dv=.5, v=0 )

#on
pm.setDrivenKeyframe( bs, at='%s'%name, cd=multiAxisAttr, dv=1, v=1 )


