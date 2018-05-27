import pymel.core as pm

def normalAvgInputs(name=None, inputs=None, connectObj=None):
    ''' 
    Input X connections and min/max values, output an averaged value normalized to 0 - 1
    connected to connectObj.name
    
    @param name Name to use for node naming and attribute
    @param inputs {'name.attr' : [min, max]} Source attribute that moves through min/max range.
    @param connectObj Object to place attribute on
    '''
    
    inputmdNormNodes = []
    results = []
    count = 0
    avgNode = pm.createNode('plusMinusAverage', n=name + '_avgNode')
    avgNode.operation.set(3)
    for attr in inputs.keys():
        minVal = inputs[attr][0]
        maxVal = inputs[attr][1]
        
        #
        # Normalize attribute range to 0 - 1
        #
        mdNormNode = pm.createNode('multiplyDivide', n=attr + '_mdNormNode')
        mdNormNode.operation.set(2)
        inputmdNormNodes.append( mdNormNode )
            
        # Case 1:[0<x<2.5] 0-2.5 ---> z ---> z/(max-min) ---> 0-1 ---> AVG.z
        if minVal == 0 and maxVal > 0:
            pm.connectAttr( attr, '%s.input1X' % mdNormNode.name(), f=1)
            mdNormNode.input2X.set(maxVal - minVal)
            pm.connectAttr(mdNormNode.outputX, avgNode.input1D[count], f=1)
            results.append("Case 1: %s ---> %s.input1D[%s]" % (attr, avgNode, count))
            
        # Case 2:[0>x>-3]  0-(-3)  ---> e+max ---> e/max ---> e-1 ---> 0-1 ---> AVG.e
        elif minVal == 0 and maxVal < 0:
            addMaxNode = pm.createNode('plusMinusAverage', n=name + '_addMaxNode')
            addMaxNode.operation.set(1)
            pm.connectAttr( attr, '%s.input1D[0]' % addMaxNode.name(), f=1)
            addMaxNode.input1D[1].set(maxVal)
            
            addMaxNode.output1D >> mdNormNode.input1X
            mdNormNode.input2X.set(maxVal)
            
            minusOneNode = pm.createNode('plusMinusAverage', n=name + '_minusOneNode')
            minusOneNode.operation.set(2)
            minusOneNode.input1D[1].set(1)
            mdNormNode.outputX >> minusOneNode.input1D[0]
            
            minusOneNode.output1D >> avgNode.input1D[count]
            results.append("Case 2: %s ---> %s.input1D[%s]" % (attr, avgNode, count))
        
        # Case 3:[-3<x<0]  -3-0  ---> e+(min*-1) ---> e/(min*-1) ---> 0-1 ---> AVG.e
        elif minVal < 0 and maxVal == 0:
            addInvMinNode = pm.createNode('plusMinusAverage', n=name + '_addInvMinNode')
            addInvMinNode.operation.set(1)
            pm.connectAttr( attr, '%s.input1D[0]' % addInvMinNode.name(), f=1)
            addInvMinNode.input1D[1].set(minVal*-1)
            
            addInvMinNode.output1D >> mdNormNode.input1X
            mdNormNode.input2X.set(minVal * -1)
            pm.connectAttr(mdNormNode.outputX, avgNode.input1D[count], f=1)
            results.append("Case 3: %s ---> %s.input1D[%s]" % (attr, avgNode, count))
        
        # Case 4:[-1<x<1]  -1-1  ---> b+max ---> b/((min*-1)+max) ---> 0-1 ---> AVG.b
        elif minVal < 0 and maxVal > 0:
            addMaxNode = pm.createNode('plusMinusAverage', n=name + '_addMaxNode')
            addMaxNode.operation.set(1)
            pm.connectAttr( attr, '%s.input1D[0]' % addMaxNode.name(), f=1)
            addMaxNode.input1D[1].set(maxVal)
            
            addMaxNode.output1D >> mdNormNode.input1X
            mdNormNode.input2X.set((minVal * -1) + maxVal)
            pm.connectAttr(mdNormNode.outputX, avgNode.input1D[count], f=1)
            results.append("Case 4: %s ---> %s.input1D[%s]" % (attr, avgNode, count))
        
        # Case 5:[-2<x<-1] -2-(-1)  ---> d+(min*-1) ---> d/(min-max) ---> min>max? *-1 ---> x > min? ---> 0-1 ---> AVG.d
        # Case 5:[-1>x>-5] -1-(-5)  
        elif minVal < 0 and maxVal < 0:
            minConNode = pm.createNode('condition', n=attr + '_minConNode')
            minConNode.operation.set(4) # Less than
            pm.connectAttr( attr, '%s.firstTerm' % minConNode.name(), f=1)
            minConNode.secondTerm.set(minVal)
            minConNode.colorIfFalseR.set(0)
            
            maxConNode = pm.createNode('condition', n=attr + '_maxConNode')
            pm.connectAttr( attr, '%s.firstTerm' % maxConNode.name(), f=1)
            maxConNode.secondTerm.set(maxVal)
            maxConNode.colorIfFalseR.set(1)            
            
            mdNegNode = pm.createNode('multiplyDivide', n=attr + '_mdNegNode')
            mdNegNode.operation.set(2)
            mdNegNode.input1X.set(minVal)
            mdNegNode.input2X.set(-1)
            
            addNode = pm.createNode('plusMinusAverage', n=name + '_addNode')
            addNode.operation.set(1)
            pm.connectAttr( attr, '%s.input1D[0]' % addNode.name(), f=1)
            mdNegNode.outputX >> addNode.input1D[1]            
            
            addNode.output1D >> mdNormNode.input1X
            mdNormNode.input2X.set(minVal - maxVal)
            
            if minVal > maxVal:
                maxConNode.operation.set(2) # Less than
                mdNegNodeB = pm.createNode('multiplyDivide', n=attr + '_mdNegNodeB')
                mdNegNodeB.operation.set(1)
                mdNormNode.outputX  >> mdNegNodeB.input1X
                mdNegNodeB.input2X.set(-1)
                mdNegNodeB.outputX >> minConNode.colorIfTrueR
            else:
                maxConNode.operation.set(4) # Greater than
                mdNormNode.outputX >> minConNode.colorIfTrueR
            
            minConNode.outColorR >> maxConNode.colorIfTrueR
            maxConNode.outColorR >> avgNode.input1D[count]
            results.append("Case 5: %s ---> %s.input1D[%s]" % (attr, avgNode, count))
        
        # Case 6:[0.5<x<1] 0.5-1 ---> a-min ---> a/(max-min) ---> 0-1 ---> AVG.a
        elif minVal > 0 and maxVal > 0:
            minConNode = pm.createNode('condition', n=attr + '_minConNode')
            minConNode.operation.set(4) # Less than
            pm.connectAttr( attr, '%s.firstTerm' % minConNode.name(), f=1)
            minConNode.secondTerm.set(minVal)
            minConNode.colorIfFalseR.set(0)
            
            maxConNode = pm.createNode('condition', n=attr + '_maxConNode')
            pm.connectAttr( attr, '%s.firstTerm' % maxConNode.name(), f=1)
            maxConNode.secondTerm.set(maxVal)
            maxConNode.colorIfFalseR.set(1)            

            minusMinNode = pm.createNode('plusMinusAverage', n=name + '_minusMinNode')
            minusMinNode.operation.set(2)
            pm.connectAttr( attr, '%s.input1D[0]' % minusMinNode.name(), f=1)
            minusMinNode.input1D[1].set(minVal)
            
            minusMinNode.output1D >> mdNormNode.input1X
            mdNormNode.input2X.set(maxVal - minVal)
            
            if minVal > maxVal:
                maxConNode.operation.set(2) # Less than
                mdNormNode.outputX  >> minConNode.colorIfTrueR 
            else:
                minConNode.operation.set(2) # Less than
                maxConNode.operation.set(4) # Greater than
                mdNormNode.outputX >> minConNode.colorIfTrueR            
            
            minConNode.outColorR >> maxConNode.colorIfTrueR
            maxConNode.outColorR >> avgNode.input1D[count]            
            results.append("Case 6: %s ---> %s.input1D[%s]" % (attr, avgNode, count))

        count += 1
            
    # Create / Connect driver Attribute
    # AVG.output1D ---> resultAttr(0-1) ---> SDK ---> Corrective
    pm.addAttr(connectObj, ln=name, k=1)
    pm.connectAttr(avgNode.output1D, connectObj + '.' + name, f=1)
    
    for each in results:
        print each

name = 'ClavUpShldrDwn'
inputs = {'CRIG:l_clav_cnt.LShoulder_v':[0.5, 0], 
          'CRIG:l_clav_cnt.LClav_v':[0.5, 0.2]}
connectObj = 'CRIG:l_clav_cnt'
normalAvgInputs(name=name, inputs=inputs, connectObj=connectObj)

name = 'ClavUpShldrDwn'
inputs = {'CRIG:r_clav_cnt.RShoulder_v':[0.5, 0], 
          'CRIG:r_clav_cnt.RClav_v':[0.5, 0.2]}
connectObj = 'CRIG:r_clav_cnt'
normalAvgInputs(name=name, inputs=inputs, connectObj=connectObj)