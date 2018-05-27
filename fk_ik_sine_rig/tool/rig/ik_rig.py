import pymel.core as pm
from ..errors import errors
from ..maya_testing import general
import utils
import control


# reg_node
def build(name=None, crv=None, loc=None,
          num_jnts=None, num_cnts=None, order=None,
          reg_node=None, log=False):
    '''Create advnced IK spine rig

    Attributes:
        name -- Prefix name used for the rig. Str
        crv -- Nurbs curve used as guide. nt.Transform
        loc -- SpaceLocator used to determine "up" vector. Str
        num_jnts -- Number of spine joints. Int
        num_cnts -- Number of controls to make. Int
        order -- Joint order. Str
        reg_node -- Registration node. nt.Transform
        log -- Output log messages. Bool
    '''
    general.check_type(name, 'name', [str])
    general.check_type(crv, 'crv', [pm.nt.Transform])
    general.check_type(loc, 'loc', [pm.nt.Transform])
    general.check_type(num_jnts, 'num_jnts', [int])
    general.check_type(num_cnts, 'num_cnts', [int])
    general.check_type(order, 'order', [str])
    if reg_node:
        general.check_type(reg_node, 'reg_node', [pm.nt.Transform])
    general.check_type(log, 'log', [bool])

    if num_jnts < 5 or num_jnts > 50:
        raise errors.InputError('num_jnts', num_jnts, 'Value Range: 5 - 50')
    if num_cnts < 2 or num_jnts > 20:
        raise errors.InputError('num_cnts', num_cnts, 'Value Range: 2 - 20')
    if order not in ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']:
        raise errors.InputError('order', order, 'String: xyz, ...')

    if not reg_node:
        reg_node = control.create_register_node(name)

    # -Make joint chain
    # -- Duplicate loc and call build script
    dup_loc = loc.duplicate()[0]
    reg_node, chain = utils.build_joint_chain(name, crv,
                                              order, num_jnts,
                                              dup_loc, reg_node)
    pm.delete(dup_loc)

    # -Make curve (duplicate / rebuild)
    ik_crv = crv.duplicate(name='%s_ik_curve' % name)[0]
    pm.rebuildCurve(ik_crv, s=20)

    # -Make spline IK
    handle = pm.ikHandle(name='%s_ikHandle' % name,
                         sj=chain[0],
                         ee=chain[-1],
                         c=ik_crv,
                         ccv=False,
                         rtm=False,
                         sol='ikSplineSolver')[0]

    # -Ik curve jnts
    dup_loc = loc.duplicate()[0]
    temp, ikCrvJnts = utils.build_joint_chain('%s_ikCrv' % name, crv,
                                              order, num_cnts, dup_loc)
    pm.delete(dup_loc)
    pm.delete(temp)

    for j in ikCrvJnts:
        try:
            pm.parent(j, w=1)
        except:
            pass

    # -Make controls
    count = 1
    cnts = []
    for j in ikCrvJnts:

        # Create curve
        reg_node, cnt_crv = control.\
            create_curve(name='%s%s_ik_cnt' % (name, count),
                         typ='circle',
                         scale=1.0,
                         color='yellow',
                         reg_node=reg_node)

        # Match curve to object
        control.match_object(cnt_crv, j)

        # Setup heirarchy
        pm.parent(j, cnt_crv)

        # Create heirarchy
        control.create_heirarchy(name='%s_%s' % (name, count),
                                 obj=cnt_crv, num=3)
        cnts.append(cnt_crv)
        count += 1

    # Build plane for follicles, for controls
    plane = utils.build_plane('%s_ik_' % name,
                              crv, 20, 'v', 'x', 0.5)

    # Create follicles
    follicles = []
    incr = 1/float(num_cnts)
    param = incr
    for c in cnts[1:-1]:
        fol = pm.createNode('transform', n='%s_fol' % c.name(), ss=True)
        folShape = pm.createNode('follicle',
                                 n=fol.name()+'Shape',
                                 p=fol, ss=True)
        plane.local >> folShape.inputSurface
        plane.worldMatrix[0] >> folShape.inputWorldMatrix
        folShape.outRotate >> fol.rotate
        folShape.outTranslate >> fol.translate
        fol.inheritsTransform.set(False)
        folShape.parameterU.set(0.5)
        folShape.parameterV.set(param)
        param += incr
        follicles.append(fol)

    # -Setup controls
    cnts_grp = pm.group(name='%s_cnts_grp' % name, em=1)
    count = 0
    for cnt in cnts[1:-1]:
        prnt = cnt.getParent()
        mid = prnt.getParent()
        top = mid.getParent()

        # --Grouping
        pm.parent(top, follicles[count])
        count += 1

    count = 0
    for cnt in [cnts[0], cnts[-1]]:
        prnt = cnt.getParent()
        mid = prnt.getParent()
        top = mid.getParent()

        # --Grouping
        pm.parent(top, cnts_grp)
        count += 1

    # Skin ik curve to control joints
    pm.skinCluster(ikCrvJnts,
                   ik_crv,
                   tsb=True,
                   name='%s_ikCrv_sc' % name)

    # Skin plane curve to top/btm control joints
    pm.skinCluster(ikCrvJnts[0],
                   ikCrvJnts[-1],
                   plane,
                   tsb=True,
                   name='%s_ikPlane_sc' % name)

    # -Make Advance Spline
    ik_crv.inheritsTransform.set(0)

    # Enable Adv Ik / Set: Up Object (start/end)
    handle.dTwistControlEnable.set(1)
    handle.dWorldUpType.set(2)

    up_loc1 = pm.spaceLocator(name='%s_AdvIkUpObj1_loc' % name)
    up_loc2 = pm.spaceLocator(name='%s_AdvIkUpObj2_loc' % name)

    pm.parent(up_loc1, cnts[0])
    pm.parent(up_loc2, cnts[-1])

    for loc in [up_loc1, up_loc2]:
        loc.setTranslation(0)
        loc.setRotation([0, 0, 0])
        attr = getattr(loc, 't%s' % order[1].lower())
        attr.set(5)
        loc.visibility.set(0)

    up_loc1.worldMatrix >> handle.dWorldUpMatrix
    up_loc2.worldMatrix >> handle.dWorldUpMatrixEnd

    # Create poly planes to aid in skinning nurbs plane and curve
    polyPlane = pm.nurbsToPoly(plane, mnd=1, ch=0, f=0,
                               pt=1, pc=20, chr=0.9,
                               ft=0.01, mel=0.001,
                               d=0.1, ut=1, un=3,
                               vt=1, vn=3, uch=0,
                               ucr=0, cht=0.2, es=0,
                               ntr=0, mrt=0, uss=1)[0]

    polyCrvPlane = pm.nurbsToPoly(plane, mnd=1, ch=0, f=0,
                                  pt=1, pc=20, chr=0.9,
                                  ft=0.01, mel=0.001,
                                  d=0.1, ut=1, un=3,
                                  vt=1, vn=3, uch=0,
                                  ucr=0, cht=0.2, es=0,
                                  ntr=0, mrt=0, uss=1)[0]

    p1 = pm.PyNode(polyPlane)
    p1.rename('%s_nurbsPlaneAide' % name)
    p2 = pm.PyNode(polyCrvPlane)
    p2.rename('%s_ikCrvAide' % name)

    pm.skinCluster(ikCrvJnts, p2,
                   tsb=1, name='%s_ikCrvAide_sc' % name)
    pm.skinCluster(ikCrvJnts[0], ikCrvJnts[-1], p1,
                   tsb=1, name='%s_nurbsPlaneAide_sc' % name)

    # Clean up
    for j in ikCrvJnts:
        j.hide()

    fol_grp = pm.group(n='%s_follicle_grp' % name, em=1)
    dont_mov_grp = pm.group(n='%s_dont_move_grp' % name, em=1)
    skin_jnts_grp = pm.group(n='%s_ik_skin_jnts_grp' % name, em=1)

    dont_mov_grp.translate.lock()
    dont_mov_grp.rotate.lock()
    dont_mov_grp.hide()

    pm.parent(follicles, fol_grp)
    pm.parent(chain[0], skin_jnts_grp)
    pm.parent(handle, plane, ik_crv,
              p1, p2, dont_mov_grp)

    main_grp = pm.group(n='%s_ik_rig_grp' % name, em=1)
    pm.parent(fol_grp, dont_mov_grp, skin_jnts_grp, cnts_grp, main_grp)

    # Register joint chain and ik_crv
    control.register_object(reg_node, 'ik_top_node', main_grp)
    control.register_object(reg_node, 'ik_crv', ik_crv)

    return reg_node
