import pymel.core as pm

bs = pm.PyNode('ShapesBS')

cntA = pm.PyNode('MouthNarrow')
cntB = pm.PyNode('Sneer')
cntC = pm.PyNode('UprLip')

#A: R_wide
md1 = pm.shadingNode('multiplyDivide', n='%s_R_wide_md1' % cntA, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_R_wide_md2' % cntA, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_R_wide_pma' % cntA, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_R_wide_clamp' % cntA, asUtility=1)

pm.setAttr('%s.input2X' % md1, -1)
pm.setAttr('%s.input2Y' % md1, 1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntA.tx >> md1.input1X
cntA.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.R_wide

#A: L_wide
md1 = pm.shadingNode('multiplyDivide', n='%s_L_wide_md1' % cntA, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_L_wide_md2' % cntA, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_L_wide_pma' % cntA, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_L_wide_clamp' % cntA, asUtility=1)

pm.setAttr('%s.input2X' % md1, 1)
pm.setAttr('%s.input2Y' % md1, 1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntA.tx >> md1.input1X
cntA.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.L_wide

#A: R_narrow
md1 = pm.shadingNode('multiplyDivide', n='%s_R_narrow_md1' % cntA, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_R_narrow_md2' % cntA, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_R_narrow_pma' % cntA, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_R_narrow_clamp' % cntA, asUtility=1)

pm.setAttr('%s.input2X' % md1, -1)
pm.setAttr('%s.input2Y' % md1, -1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntA.tx >> md1.input1X
cntA.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.R_narrow

#A: L_narrow
md1 = pm.shadingNode('multiplyDivide', n='%s_L_narrow_md1' % cntA, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_L_narrow_md2' % cntA, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_L_narrow_pma' % cntA, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_L_narrow_clamp' % cntA, asUtility=1)

pm.setAttr('%s.input2X' % md1, 1)
pm.setAttr('%s.input2Y' % md1, -1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntA.tx >> md1.input1X
cntA.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.L_narrow

#B: L_Sneer
md1 = pm.shadingNode('multiplyDivide', n='%s_L_Sneer_md1' % cntB, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_L_Sneer_md2' % cntB, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_L_Sneer_pma' % cntB, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_L_Sneer_clamp' % cntB, asUtility=1)

pm.setAttr('%s.input2X' % md1, 1)
pm.setAttr('%s.input2Y' % md1, 1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntB.tx >> md1.input1X
cntB.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.L_Sneer

#B: R_Sneer
md1 = pm.shadingNode('multiplyDivide', n='%s_R_Sneer_md1' % cntB, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_R_Sneer_md2' % cntB, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_R_Sneer_pma' % cntB, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_R_Sneer_clamp' % cntB, asUtility=1)

pm.setAttr('%s.input2X' % md1, -1)
pm.setAttr('%s.input2Y' % md1, 1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntB.tx >> md1.input1X
cntB.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.R_Sneer

#C: L_UprlipUp
md1 = pm.shadingNode('multiplyDivide', n='%s_L_UprlipUp_md1' % cntC, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_L_UprlipUp_md2' % cntC, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_L_UprlipUp_pma' % cntC, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_L_UprlipUp_clamp' % cntC, asUtility=1)

pm.setAttr('%s.input2X' % md1, 1)
pm.setAttr('%s.input2Y' % md1, 1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntC.tx >> md1.input1X
cntC.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.L_UprlipUp

#C: R_Sneer
md1 = pm.shadingNode('multiplyDivide', n='%s_R_UprlipUp_md1' % cntC, asUtility=1)
md2 = pm.shadingNode('multiplyDivide', n='%s_R_UprlipUp_md2' % cntC, asUtility=1)
pma = pm.shadingNode('plusMinusAverage', n='%s_R_UprlipUp_pma' % cntC, asUtility=1)
clamp = pm.shadingNode('clamp', n='%s_R_UprlipUp_clamp' % cntC, asUtility=1)

pm.setAttr('%s.input2X' % md1, -1)
pm.setAttr('%s.input2Y' % md1, 1)
pm.setAttr('%s.input1D[1]' % pma, 1)
pm.setAttr('%s.maxR' % clamp, 1)
pm.setAttr('%s.maxG' % clamp, 1)
pm.setAttr('%s.maxB' % clamp, 1)

cntC.tx >> md1.input1X
cntC.ty >> md1.input1Y
md1.outputX >> pma.input1D[0]
pma.output1D >> clamp.inputR
md1.outputY >> clamp.inputG
clamp.outputR >> md2.input1X
clamp.outputG >> md2.input2X
md2.outputX >> clamp.inputB
clamp.outputB >> bs.R_UprlipUp