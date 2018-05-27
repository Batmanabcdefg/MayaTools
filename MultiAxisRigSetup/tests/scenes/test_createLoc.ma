//Maya ASCII 2010 scene
//Name: test_createLoc.ma
//Last modified: Fri, Mar 8, 2013 4:34:07 PM
//Codeset: UTF-8
requires maya "2010";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya Unlimited 2010";
fileInfo "version" "2010";
fileInfo "cutIdentifier" "200907280341-756013";
fileInfo "osv" "Mac OS X 10.7.5";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1.2148555978692777 4.1783036189702312 9.0365327573823642 ;
	setAttr ".r" -type "double3" -20.738352729615794 -0.99999999999987776 2.4851868508880361e-17 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 9.0187272655866373;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0.43932206925261058 -0.41097870994599073 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 14.951122034242083;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode joint -n "joint1";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 45.000000000000007 ;
	setAttr ".radi" 0.52142483943309115;
createNode joint -n "joint2" -p "joint1";
	setAttr ".t" -type "double3" 1.4142135623730951 -2.2204460492503131e-16 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -45.000000000000007 ;
	setAttr ".radi" 0.55172413793103448;
createNode joint -n "joint3" -p "joint2";
	setAttr ".t" -type "double3" 1.9999999999999998 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.55172413793103448;
createNode transform -n "control" -p "joint1";
	setAttr ".r" -type "double3" 0 0 -45.000000000000014 ;
createNode nurbsCurve -n "controlShape" -p "control";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 16 2 no 3
		21 -2 -1 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
		19
		0.39264623741499377 5.8044086617135588e-17 -0.94793187158204539
		2.4323770812907161e-16 6.2826466627483697e-17 -1.0260340642089774
		-0.39264623741499438 5.8044086617135588e-17 -0.94793187158204539
		-0.7255156445305615 4.4425020590284048e-17 -0.72551564453056139
		-0.9479318715820455 2.4042647892376221e-17 -0.39264623741499427
		-1.0260340642089776 -2.8980332155736397e-33 4.7328474097043542e-17
		-0.94793187158204517 -2.4042647892376227e-17 0.39264623741499433
		-0.7255156445305615 -4.4425020590284066e-17 0.72551564453056172
		-0.39264623741499421 -5.80440866171356e-17 0.94793187158204562
		7.7537057127920921e-17 -6.2826466627483697e-17 1.0260340642089774
		0.39264623741499455 -5.8044086617135588e-17 0.94793187158204539
		0.72551564453056139 -4.4425020590284029e-17 0.72551564453056117
		0.94793187158204584 -2.4042647892376209e-17 0.39264623741499405
		1.0260340642089771 1.0793273227319641e-32 -1.7626752847979251e-16
		0.9479318715820455 2.4042647892376246e-17 -0.39264623741499466
		0.72551564453056117 4.442502059028406e-17 -0.72551564453056161
		0.39264623741499377 5.8044086617135588e-17 -0.94793187158204539
		2.4323770812907161e-16 6.2826466627483697e-17 -1.0260340642089774
		-0.39264623741499438 5.8044086617135588e-17 -0.94793187158204539
		;
createNode transform -n "test_multiAxisRigGrp";
createNode transform -n "test_multiAxisRigPlane" -p "test_multiAxisRigGrp";
	setAttr ".s" -type "double3" 4 4 4 ;
	setAttr ".rp" -type "double3" 1.0000000000000002 1 0 ;
	setAttr ".sp" -type "double3" 1.0000000000000002 1 0 ;
createNode nurbsSurface -n "test_multiAxisRigPlaneShape" -p "test_multiAxisRigPlane";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 0 no 
		6 0 0 0 1 1 1
		6 0 0 0 1 1 1
		
		16
		1 1.4998641241847173 -0.49986412418471754
		1.0000000000000002 1.1666213747282392 -0.49986412418471743
		1.0000000000000002 0.83337862527176088 -0.49986412418471743
		1.0000000000000002 0.50013587581528252 -0.49986412418471732
		1.0000000000000002 1.4998641241847173 -0.16662137472823926
		1.0000000000000002 1.1666213747282392 -0.16662137472823918
		1.0000000000000002 0.83337862527176088 -0.16662137472823912
		1.0000000000000004 0.50013587581528263 -0.16662137472823904
		1.0000000000000002 1.4998641241847173 0.16662137472823899
		1.0000000000000002 1.1666213747282392 0.16662137472823907
		1.0000000000000004 0.83337862527176099 0.16662137472823912
		1.0000000000000004 0.50013587581528263 0.16662137472823921
		1.0000000000000002 1.4998641241847175 0.49986412418471732
		1.0000000000000004 1.1666213747282392 0.49986412418471743
		1.0000000000000004 0.83337862527176099 0.49986412418471743
		1.0000000000000004 0.50013587581528274 0.49986412418471754
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode parentConstraint -n "test_multiAxisRigGrpParentConst" -p "test_multiAxisRigGrp";
	addAttr -ci true -k true -sn "w0" -ln "joint1W0" -bt "W000" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tor" -type "double3" 0 0 -45.000000000000014 ;
	setAttr -k on ".w0";
createNode lightLinker -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode closestPointOnSurface -n "test_multiAxisRigCPOS";
	setAttr ".ip" -type "double3" 1.0000000000000002 1.0000000000000002 -9.0205620750793969e-17 ;
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 24 -ast 1 -aet 48 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr ".o" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :lightList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
connectAttr "joint1.s" "joint2.is";
connectAttr "joint2.s" "joint3.is";
connectAttr "test_multiAxisRigGrpParentConst.ctx" "test_multiAxisRigGrp.tx";
connectAttr "test_multiAxisRigGrpParentConst.cty" "test_multiAxisRigGrp.ty";
connectAttr "test_multiAxisRigGrpParentConst.ctz" "test_multiAxisRigGrp.tz";
connectAttr "test_multiAxisRigGrpParentConst.crx" "test_multiAxisRigGrp.rx";
connectAttr "test_multiAxisRigGrpParentConst.cry" "test_multiAxisRigGrp.ry";
connectAttr "test_multiAxisRigGrpParentConst.crz" "test_multiAxisRigGrp.rz";
connectAttr "test_multiAxisRigGrp.ro" "test_multiAxisRigGrpParentConst.cro";
connectAttr "test_multiAxisRigGrp.pim" "test_multiAxisRigGrpParentConst.cpim";
connectAttr "test_multiAxisRigGrp.rp" "test_multiAxisRigGrpParentConst.crp";
connectAttr "test_multiAxisRigGrp.rpt" "test_multiAxisRigGrpParentConst.crt";
connectAttr "joint1.t" "test_multiAxisRigGrpParentConst.tg[0].tt";
connectAttr "joint1.rp" "test_multiAxisRigGrpParentConst.tg[0].trp";
connectAttr "joint1.rpt" "test_multiAxisRigGrpParentConst.tg[0].trt";
connectAttr "joint1.r" "test_multiAxisRigGrpParentConst.tg[0].tr";
connectAttr "joint1.ro" "test_multiAxisRigGrpParentConst.tg[0].tro";
connectAttr "joint1.s" "test_multiAxisRigGrpParentConst.tg[0].ts";
connectAttr "joint1.pm" "test_multiAxisRigGrpParentConst.tg[0].tpm";
connectAttr "joint1.jo" "test_multiAxisRigGrpParentConst.tg[0].tjo";
connectAttr "test_multiAxisRigGrpParentConst.w0" "test_multiAxisRigGrpParentConst.tg[0].tw"
		;
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[0].llnk";
connectAttr ":initialShadingGroup.msg" "lightLinker1.lnk[0].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[1].llnk";
connectAttr ":initialParticleSE.msg" "lightLinker1.lnk[1].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[0].sllk";
connectAttr ":initialShadingGroup.msg" "lightLinker1.slnk[0].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[1].sllk";
connectAttr ":initialParticleSE.msg" "lightLinker1.slnk[1].solk";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "test_multiAxisRigPlaneShape.ws" "test_multiAxisRigCPOS.is";
connectAttr "lightLinker1.msg" ":lightList1.ln" -na;
connectAttr "test_multiAxisRigPlaneShape.iog" ":initialShadingGroup.dsm" -na;
// End of test_createLoc.ma
