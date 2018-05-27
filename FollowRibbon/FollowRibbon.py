class FollowRibbon(object):
    '''
    Given nurbs plane, create soft falloff controls.
    
    Use:
    x = FollowRibbon(name='browRig')
    plane = 'nurbsPlane'
    grps, jnts, cpos = x._createPlaneControls( plane=plane, direction='u', number=5 )
    mainGrp, ctrls = x._createDriveControls( grps=grps, cposNodes=cpos )
    x._clusterPlane( plane=plane, controls=ctrls, mainGrp=mainGrp )
    
    
    '''
    def __init__(self, **keywords):  
        import logging
        import pymel.core as pm
        self.pm = pm

        #--- Determine how much feedback in log file
        if keywords.has_key('v'):
            self.verbosity = keywords['v']
        else:
            # Default. Higher verbosity reveals more info in log file. 1 - 5
            self.verbosity = 1        

        #--- Setup logging
        logging.basicConfig( filename='FollowRibbon.log', filemode='w',
                             format= '%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                             datefmt='%m/%d/%Y %I:%M:%S %p' )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.verbosity * 10)

        if keywords.has_key('name'):
            self.name = keywords['name']
        else:
            self.logger.error('No name passed in by caller.')
            raise Exception('No name passed in by caller.')

    def _clusterPlane(self, plane=None, controls=None, mainGrp=None):
        ''' Cluster plane and connect the translations to the controls passed in '''
        clusters = []
        for ctrl in controls:
            cluster = self.pm.cluster(plane,name=ctrl.replace('ctrl', 'cluster'))
            self.pm.connectAttr('%s.translate'%ctrl, '%s.translate'%cluster[1])
            self.pm.parent(cluster[1],mainGrp)
            clusters.append(cluster[1])
        return clusters

    def _createDriveControls(self, grps=None, cposNodes=None):
        ''' 
        Create grps and control that the animator will use, connect to ribbon.
        grps = ['blah_drvGrp_01', 'blah_drvGrp_02', 'blah_drvGrp_03', 'blah_drvGrp_04']
        '''
        self.logger.info('Starting: _createDriveControls()...')
        if not grps:
            self.logger.error('No grps passed in by caller.')
            raise Exception('No grps passed in by caller.')  
        self.pm.select(clear=True)
        mainGrp = self.pm.group(name='%s_ctrlsGrp'%grps[0].split('_')[0])

        ctrls = []
        for index in range(len(grps)):
            topGrp = self.pm.group(em=True, name='%s_ctrlTopGrp_%s'%(self.name, str(index+1).zfill(2)))
            midGrp = self.pm.group(em=True,name='%s_ctrlMidGrp_%s'%(self.name, str(index+1).zfill(2)))
            btmGrp = self.pm.group(em=True,name='%s_ctrlBtmGrp_%s'%(self.name, str(index+1).zfill(2)))
            ctrl = self.sphereControl(name=('%s_ctrl_%s'%(self.name, str(index+1).zfill(2))))
            self.pm.addAttr(ctrl, ln='uParam', at='float', k=1, min=0, max=1)
            self.pm.addAttr(ctrl, ln='vParam', at='float', k=1, min=0, max=1)
            valU = self.pm.getAttr('%s.parameterU'%cposNodes[index])
            valV = self.pm.getAttr('%s.parameterV'%cposNodes[index])
            self.pm.connectAttr('%s.uParam'%ctrl,'%s.parameterU'%cposNodes[index])
            self.pm.connectAttr('%s.vParam'%ctrl,'%s.parameterV'%cposNodes[index])
            self.pm.setAttr('%s.uParam'%ctrl,valU)
            self.pm.setAttr('%s.vParam'%ctrl,valV)
            ctrls.append(ctrl)

            self.pm.delete(self.pm.pointConstraint(grps[index], topGrp, mo=0).name())
            self.pm.delete(self.pm.pointConstraint(grps[index], midGrp, mo=0).name())
            self.pm.delete(self.pm.pointConstraint(grps[index], btmGrp, mo=0).name())
            self.pm.delete(self.pm.pointConstraint(grps[index], ctrl, mo=0).name())	    

            self.pm.parent(topGrp, mainGrp)
            self.pm.parent(midGrp, topGrp)
            self.pm.parent(btmGrp, midGrp)
            self.pm.parent(ctrl, btmGrp)

            self.pm.parentConstraint(grps[index], topGrp, mo=1)

            md = self.pm.createNode('multiplyDivide', name='%s_InvertMdNode_%s'%(self.name, str(index+1).zfill(2)))
            md.setAttr('input2X', -1)
            md.setAttr('input2Y', -1)
            md.setAttr('input2Z', -1)

            self.pm.connectAttr('%s.translate'%ctrl, '%s.input1'%md.name())
            self.pm.connectAttr('%s.output'%md.name(), '%s.translate'%btmGrp.name())

        self.logger.info('End: _createDriveControls().')
        return mainGrp, ctrls

    def _createPlaneControls(self, plane=None, direction='u', number=5):
        ''' Given nurbs plane, create grps/joints that follow the plane. '''
        self.logger.info('Starting: _createPlaneControls()...')

        # Validate input -------------------------------------------------------------------------------------
        if not plane:
            self.logger.error('Invalid plane passed in by user: %s'%plane)
            raise Exception('Please pass in a nurbs plane; plane = "nurbsPlane01"')

        if self.pm.objectType(self.pm.listRelatives(plane,s=1)[0]) != 'nurbsSurface':
            self.logger.error('Invalid plane passed in by user: %s'%plane)
            raise Exception('%s is not a nurbs plane.'%plane)

        if not direction:
            self.logger.error('Invalid direction passed in by user: %s'%direction)
            raise Exception('Please pass in a direction: direction = "u" or "v"')

        if not number:
            self.logger.error('Invalid number passed in by user: %s'%number)
            raise Exception('Please specify the number of controls to put on the nurbs plane; number = 5')

        if (number-1) <= 0:
            self.logger.error('Invalid number value passed in by user: %s. Minimum is 2.'%number)
            raise Exception('Please specify a number of 2 or more.')            

        # Create closestPointOnSurface nodes -----------------------------------------------------------------
        cposNodes = []

        increment = (100.0 / (number-1))/100.0
        inc = increment
        for index in range(number):
            if index == 0:
                percent = 0
            elif index == (number-1):
                percent = 1
            else:
                percent = inc
                inc = inc + increment

            cpos = self.pm.createNode('pointOnSurfaceInfo', 
                                      n='%s_drvCPOS_'%self.name+'%s'%(str(index+1)).zfill(2))
            cpos.setAttr('turnOnPercentage',1)
            if direction == 'u':
                cpos.setAttr('parameterU',percent)
                cpos.setAttr('parameterV',.5)
            if direction == 'v':
                cpos.setAttr('parameterU',.5)
                cpos.setAttr('parameterV',percent)    
            self.pm.connectAttr('%s.worldSpace'%plane,'%s.is'%cpos.name())	    
            cposNodes.append(cpos)

        # Create groups -----------------------------------------------------------------
        grps = []
        for index in range(number):
            grps.append(self.pm.group( em=True, name='%s_drvGrp_'%self.name+'%s'%(str(index+1)).zfill(2)))
            self.pm.connectAttr('%s.position'%cposNodes[index].name(), 
                                '%s.t'%grps[index])
            '''self.pm.move( grps[index],
                          [int(cposNodes[index].getAttr('positionX')),
                          int(cposNodes[index].getAttr('positionY')),
                          int(cposNodes[index].getAttr('positionZ'))] )'''


        # Create joints -----------------------------------------------------------------
        jnts = []
        for index in range(number):
            pos = self.pm.xform(grps[index], q=1, ws=1, t=1)
            jnt = self.pm.joint( name='%s_drvJnt_'%self.name+'%s'%(str(index+1)).zfill(2),
                                 position = (pos[0], pos[1], pos[2]) )
            self.pm.parent(jnt, grps[index])
            jnts.append(jnt)

        self.logger.info('End: _createPlaneControls().\nINFO : Returned:\nINFO : grps: %s\nINFO : jnts: %s'%(grps,jnts))  
        cpos = []
        for each in cposNodes:
            cpos.append(each.name())
        return grps, jnts, cpos

    def sphereControl(self, name=None):
        ''' Create a sphere control curve with the given name. '''

        if not name:
            raise Exception('No name passed in by caller.')

        self.pm.mel.eval('createNode transform -n "%s";\n'%name +\
                         'createNode nurbsCurve -n "%s_shape_1" -p "%s";\n'%(name, name) +\
                         'setAttr -k off ".v";\n' +\
                         'setAttr ".ove" yes;\n' +\
                         'setAttr ".ovc" 17;\n' +\
                         'setAttr ".cc" -type "nurbsCurve" \n' +\
                         '3 8 2 no 3\n' +\
                         '13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n' +\
                         '11\n' +\
                         '0.017167416392123373 0.017167416392123356 6.9388939039072284e-018\n' +\
                         '-6.2393213061196954e-018 0.024278393092647056 6.9388939039072284e-018\n' +\
                         '-0.017167416392123363 0.017167416392123366 6.9388939039072284e-018\n' +\
                         '-0.024278393092647049 1.0504717872765056e-017 6.9388939039072284e-018\n' +\
                         '-0.01716741639212337 -0.017167416392123356 6.9388939039072284e-018\n' +\
                         '-1.078500061076102e-017 -0.024278393092647056 6.9388939039072284e-018\n' +\
                         '0.017167416392123346 -0.017167416392123363 6.9388939039072284e-018\n' +\
                         '0.024278393092647042 -9.570525338805305e-018 6.9388939039072284e-018\n' +\
                         '0.017167416392123373 0.017167416392123356 6.9388939039072284e-018\n' +\
                         '-6.2393213061196954e-018 0.024278393092647056 6.9388939039072284e-018\n' +\
                         '-0.017167416392123363 0.017167416392123366 6.9388939039072284e-018\n' +\
                         ';\n' +\
                         'createNode nurbsCurve -n "%s_shape_2" -p "%s";\n'%(name, name) +\
                         'setAttr -k off ".v";\n' +\
                         'setAttr ".ove" yes;\n' +\
                         'setAttr ".ovc" 17;\n' +\
                         'setAttr ".cc" -type "nurbsCurve" \n' +\
                         '3 8 2 no 3\n' +\
                         '13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n' +\
                         '11\n' +\
                         '3.4248523841892813e-019 0.017167416392123356 -0.017167416392123373\n' +\
                         '-3.4694469519536142e-018 0.024278393092647056 6.9388939039072284e-018\n' +\
                         '-7.2813791423261503e-018 0.017167416392123366 0.017167416392123366\n' +\
                         '-8.8603331544250348e-018 1.0504717872765056e-017 0.024278393092647038\n' +\
                         '-7.2813791423261534e-018 -0.017167416392123356 0.017167416392123366\n' +\
                         '-3.469446951953615e-018 -0.024278393092647056 1.3877787807814457e-017\n' +\
                         '3.4248523841892197e-019 -0.017167416392123363 -0.017167416392123346\n' +\
                         '1.9214392505178087e-018 -9.570525338805305e-018 -0.024278393092647042\n' +\
                         '3.4248523841892813e-019 0.017167416392123356 -0.017167416392123373\n' +\
                         '-3.4694469519536142e-018 0.024278393092647056 6.9388939039072284e-018\n' +\
                         '-7.2813791423261503e-018 0.017167416392123366 0.017167416392123366\n' +\
                         ';\n' +\
                         'createNode nurbsCurve -n "%s_shape_3" -p "%s";\n'%(name, name) +\
                         'setAttr -k off ".v";\n' +\
                         'setAttr ".ove" yes;\n' +\
                         'setAttr ".ovc" 17;\n' +\
                         'setAttr ".cc" -type "nurbsCurve" \n' +\
                         '3 8 2 no 3\n' +\
                         '13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n' +\
                         '11\n' +\
                         '-0.017167416392123352 1.1093311332698693e-017 -0.017167416392123373\n' +\
                         '-0.024278393092647049 8.8603331544250379e-018 6.9388939039072284e-018\n' +\
                         '-0.017167416392123363 3.4694469519536142e-018 0.017167416392123366\n' +\
                         '-1.0504717872765053e-017 -1.9214392505178087e-018 0.024278393092647038\n' +\
                         '0.017167416392123352 -4.1544174287914628e-018 0.017167416392123366\n' +\
                         '0.024278393092647049 -1.9214392505178126e-018 1.3877787807814457e-017\n' +\
                         '0.017167416392123359 3.4694469519536115e-018 -0.017167416392123346\n' +\
                         '9.5705253388053019e-018 8.8603331544250348e-018 -0.024278393092647042\n' +\
                         '-0.017167416392123352 1.1093311332698693e-017 -0.017167416392123373\n' +\
                         '-0.024278393092647049 8.8603331544250379e-018 6.9388939039072284e-018\n' +\
                         '-0.017167416392123363 3.4694469519536142e-018 0.017167416392123366;')

        return name

