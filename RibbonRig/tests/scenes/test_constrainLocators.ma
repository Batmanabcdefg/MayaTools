//Maya ASCII 2010 scene
//Name: test_constrainLocators.ma
//Last modified: Sun, Mar 17, 2013 12:06:20 PM
//Codeset: UTF-8
requires maya "2010";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya Unlimited 2010";
fileInfo "version" "2010";
fileInfo "cutIdentifier" "200907280341-756013";
fileInfo "osv" "Mac OS X 10.7.5";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -2.0527885745159198 3.9085224369744447 14.200074954832971 ;
	setAttr ".r" -type "double3" -17.999999999997875 352.79999999998688 2.0036460232682847e-16 ;
	setAttr ".rpt" -type "double3" 2.7497122435741483e-17 6.1217135333370927e-17 -3.2698759415417925e-17 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999979;
	setAttr ".coi" 14.505585772443057;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -2.2758954752073961e-15 3.7016940813325569e-22 0 ;
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
	setAttr ".t" -type "double3" 0.73574039698773475 0.5467909122795096 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 6.2410669813812998;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 -2.7767055430841063 -1.7780404429142409 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 7.3087310464548967;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "pCube1";
	setAttr ".s" -type "double3" 1 5.9888892050695475 1 ;
createNode mesh -n "pCubeShape1" -p "pCube1";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "ribbon01_plane";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
createNode nurbsSurface -n "ribbon01_planeShape" -p "ribbon01_plane";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".tw" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".dcv" yes;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
createNode nurbsSurface -n "ribbon01_planeShapeOrig" -p "ribbon01_plane";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".dcv" yes;
	setAttr ".cc" -type "nurbsSurface" 
		1 3 0 0 no 
		2 0 1
		11 0 0 0 0.16666666666666666 0.33333333333333331 0.5 0.66666666666666663 0.83333333333333326
		 1 1 1
		
		18
		-0.50000000000000011 -3.0000000000000009 0
		-0.50000000000000011 -2.6666666666666683 0
		-0.50000000000000011 -1.9999999999999996 0
		-0.50000000000000011 -0.99999999999999978 0
		-0.50000000000000011 3.1238234436425623e-17 0
		-0.50000000000000011 0.99999999999999978 0
		-0.50000000000000011 1.9999999999999996 0
		-0.50000000000000011 2.6666666666666683 0
		-0.50000000000000011 3.0000000000000009 0
		0.49999999999999983 -3 0
		0.49999999999999983 -2.6666666666666661 0
		0.49999999999999983 -2 0
		0.49999999999999983 -1 0
		0.49999999999999983 4.6443961262081249e-17 0
		0.49999999999999983 0.99999999999999978 0
		0.49999999999999983 1.9999999999999996 0
		0.49999999999999983 2.6666666666666661 0
		0.49999999999999983 3 0
		
		;
createNode transform -n "hairSystem1Follicles";
createNode transform -n "ribbon01_follicle01" -p "hairSystem1Follicles";
createNode follicle -n "ribbon01_follicle0Shape1" -p "ribbon01_follicle01";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.083333333333333329;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "joint1" -p "ribbon01_follicle01";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".radi" 2;
createNode transform -n "ribbon01_follicle02" -p "hairSystem1Follicles";
createNode follicle -n "ribbon01_follicle0Shape2" -p "ribbon01_follicle02";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.25;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "joint2" -p "ribbon01_follicle02";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".radi" 2;
createNode transform -n "ribbon01_follicle03" -p "hairSystem1Follicles";
createNode follicle -n "ribbon01_follicle0Shape3" -p "ribbon01_follicle03";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.41666666666666669;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "joint3" -p "ribbon01_follicle03";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".radi" 2;
createNode transform -n "ribbon01_follicle04" -p "hairSystem1Follicles";
createNode follicle -n "ribbon01_follicle0Shape4" -p "ribbon01_follicle04";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.58333333333333337;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "joint4" -p "ribbon01_follicle04";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".radi" 2;
createNode transform -n "ribbon01_follicle05" -p "hairSystem1Follicles";
createNode follicle -n "ribbon01_follicle0Shape5" -p "ribbon01_follicle05";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.75;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "joint5" -p "ribbon01_follicle05";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".radi" 2;
createNode transform -n "ribbon01_follicle06" -p "hairSystem1Follicles";
createNode follicle -n "ribbon01_follicle0Shape6" -p "ribbon01_follicle06";
	setAttr -k off ".v";
	setAttr ".pu" 0.5;
	setAttr ".pv" 0.91666666666666663;
	setAttr -s 2 ".sts[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".cws[0:1]"  0 1 3 1 0.2 3;
	setAttr -s 2 ".ats[0:1]"  0 1 3 1 0.2 3;
createNode joint -n "joint6" -p "ribbon01_follicle06";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".dla" yes;
	setAttr ".radi" 2;
createNode transform -n "spineTop1_pos";
	setAttr ".t" -type "double3" -1.3877787807814457e-16 3 0 ;
createNode locator -n "spineTop1_posShape" -p "spineTop1_pos";
	setAttr -k off ".v";
createNode transform -n "spineTop1_aim" -p "spineTop1_pos";
createNode locator -n "spineTop1_aimShape" -p "spineTop1_aim";
	setAttr -k off ".v";
createNode aimConstraint -n "spineTop1_aim_aimConstraint1" -p "spineTop1_aim";
	addAttr -ci true -sn "w0" -ln "spineBttm1_posW0" -bt "W000" -dv 1 -at "double";
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
	setAttr ".a" -type "double3" 0 -1 0 ;
	setAttr ".u" -type "double3" 1 0 0 ;
	setAttr ".wut" 1;
	setAttr -k on ".w0";
createNode joint -n "spineTop01_fk" -p "spineTop1_aim";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -bt "lock" -min 0 -max 1 
		-at "bool";
	setAttr ".uoc" yes;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 -1.0000000000000002 0 0 1.0000000000000002 2.2204460492503131e-16 0 0
		 0 0 1 0 -1.3877787807814457e-16 3 0 1;
	setAttr ".radi" 2;
createNode joint -n "spineTop02_end" -p "spineTop01_fk";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.99999999999999956 -4.4408920985006262e-16 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 89.999999999999986 ;
	setAttr ".radi" 2;
createNode transform -n "spineTop1_up" -p "spineTop1_pos";
	setAttr ".t" -type "double3" 2 0 0 ;
createNode locator -n "spineTop1_upShape" -p "spineTop1_up";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 0.5 0.5 0.5 ;
createNode transform -n "spineBttm1_pos";
	setAttr ".t" -type "double3" -1.3877787807814457e-16 -3 0 ;
createNode locator -n "spineBttm1_posShape" -p "spineBttm1_pos";
	setAttr -k off ".v";
createNode transform -n "spineBttm1_aim" -p "spineBttm1_pos";
createNode locator -n "spineBttm1_aimShape" -p "spineBttm1_aim";
	setAttr -k off ".v";
createNode aimConstraint -n "spineBttm1_aim_aimConstraint1" -p "spineBttm1_aim";
	addAttr -ci true -sn "w0" -ln "spineTop1_posW0" -bt "W000" -dv 1 -at "double";
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
	setAttr ".a" -type "double3" 0 1 0 ;
	setAttr ".u" -type "double3" 1 0 0 ;
	setAttr ".wut" 1;
	setAttr -k on ".w0";
createNode joint -n "spineBttm01_fk" -p "spineBttm1_aim";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -bt "lock" -min 0 -max 1 
		-at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 89.999999999999986 ;
	setAttr ".bps" -type "matrix" 2.2204460492503131e-16 1.0000000000000002 0 0 -1.0000000000000002 2.2204460492503131e-16 0 0
		 0 0 1 0 -1.3877787807814457e-16 -3 0 1;
	setAttr ".radi" 2;
createNode joint -n "spineBttm02_end" -p "spineBttm01_fk";
	setAttr ".t" -type "double3" 0.99999999999999956 4.4408920985006262e-16 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
	setAttr ".radi" 2;
createNode transform -n "spineBttm1_up" -p "spineBttm1_pos";
	setAttr ".t" -type "double3" 2 0 0 ;
createNode locator -n "spineBttm1_upShape" -p "spineBttm1_up";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 0.5 0.5 0.5 ;
createNode transform -n "spineMid1_pos";
createNode locator -n "spineMid1_posShape" -p "spineMid1_pos";
	setAttr -k off ".v";
createNode transform -n "spineMid1_aim" -p "spineMid1_pos";
createNode locator -n "spineMid1_aimShape" -p "spineMid1_aim";
	setAttr -k off ".v";
createNode transform -n "spineMid1_off" -p "spineMid1_aim";
createNode locator -n "spineMid1_offShape" -p "spineMid1_off";
	setAttr -k off ".v";
createNode joint -n "mid01_fk" -p "spineMid1_off";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -bt "lock" -min 0 -max 1 
		-at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 2;
createNode aimConstraint -n "spineMid1_aim_aimConstraint1" -p "spineMid1_aim";
	addAttr -ci true -sn "w0" -ln "spineTop1_posW0" -bt "W000" -dv 1 -at "double";
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
	setAttr ".a" -type "double3" 0 1 0 ;
	setAttr ".u" -type "double3" 1 0 0 ;
	setAttr ".wut" 1;
	setAttr -k on ".w0";
createNode transform -n "spineMid1_up" -p "spineMid1_pos";
createNode locator -n "spineMid1_upShape" -p "spineMid1_up";
	setAttr -k off ".v";
	setAttr ".los" -type "double3" 0.5 0.5 0.5 ;
createNode pointConstraint -n "spineMid1_up_pointConstraint1" -p "spineMid1_up";
	addAttr -ci true -k true -sn "w0" -ln "spineTop1_upW0" -bt "W000" -dv 1 -min 0 
		-at "double";
	addAttr -ci true -k true -sn "w1" -ln "spineBttm1_upW1" -bt "W001" -dv 1 -min 0 
		-at "double";
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
	setAttr -s 2 ".tg";
	setAttr ".o" -type "double3" 2.2204460492503131e-16 0 0 ;
	setAttr ".rst" -type "double3" 2 0 0 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode pointConstraint -n "spineMid1_pos_pointConstraint1" -p "spineMid1_pos";
	addAttr -ci true -k true -sn "w0" -ln "spineTop1_posW0" -bt "W000" -dv 1 -min 0 
		-at "double";
	addAttr -ci true -k true -sn "w1" -ln "spineBttm1_posW1" -bt "W001" -dv 1 -min 0 
		-at "double";
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
	setAttr -s 2 ".tg";
	setAttr ".o" -type "double3" 1.3877787807814457e-16 0 0 ;
	setAttr -k on ".w0";
	setAttr -k on ".w1";
createNode lightLinker -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	setAttr -s 2 ".dli[1]"  1;
	setAttr -s 2 ".dli";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode polyCube -n "polyCube1";
	setAttr ".sh" 6;
	setAttr ".cuv" 4;
createNode displayLayer -n "layer1";
	setAttr ".v" no;
	setAttr ".do" 1;
createNode skinCluster -n "skinCluster1";
	setAttr -s 18 ".wl";
	setAttr -s 2 ".wl[0].w[1:2]"  1.4420867062489442e-08 0.99999998557913294;
	setAttr -s 3 ".wl[1].w[0:2]"  1.8829838315019006e-10 4.518384214786932e-08 
		0.99999995462785951;
	setAttr -s 3 ".wl[2].w[0:2]"  8.618524301550412e-10 7.0429578108384358e-07 
		0.99999929484236649;
	setAttr -s 3 ".wl[3].w[0:2]"  2.2532097405370266e-05 0.49998873395129878 
		0.49998873395129578;
	setAttr -s 3 ".wl[4].w[0:2]"  7.0429528565864638e-07 0.99999859140942871 
		7.0429528565864638e-07;
	setAttr -s 3 ".wl[5].w[0:2]"  0.49998873395129578 0.49998873395129889 
		2.2532097405370266e-05;
	setAttr -s 3 ".wl[6].w[0:2]"  0.99999929484236649 7.0429578108384358e-07 
		8.618524301550412e-10;
	setAttr -s 3 ".wl[7].w[0:2]"  0.99999995462785951 4.518384214786932e-08 
		1.8829838315019006e-10;
	setAttr -s 2 ".wl[8].w[0:1]"  0.99999998557913294 1.4420867062489442e-08;
	setAttr -s 2 ".wl[9].w[1:2]"  1.4420867062489483e-08 0.99999998557913294;
	setAttr -s 3 ".wl[10].w[0:2]"  1.8829838315019153e-10 4.518384214786979e-08 
		0.99999995462785951;
	setAttr -s 3 ".wl[11].w[0:2]"  8.6185243015504978e-10 7.0429578108384919e-07 
		0.99999929484236649;
	setAttr -s 3 ".wl[12].w[0:2]"  2.2532097405370201e-05 0.49998873395129878 
		0.49998873395129578;
	setAttr -s 3 ".wl[13].w[0:2]"  7.0429528565864247e-07 0.99999859140942871 
		7.0429528565864247e-07;
	setAttr -s 3 ".wl[14].w[0:2]"  0.49998873395129478 0.49998873395129989 
		2.2532097405370266e-05;
	setAttr -s 3 ".wl[15].w[0:2]"  0.99999929484236649 7.0429578108385067e-07 
		8.6185243015504978e-10;
	setAttr -s 3 ".wl[16].w[0:2]"  0.99999995462785951 4.518384214786979e-08 
		1.8829838315019153e-10;
	setAttr -s 2 ".wl[17].w[0:1]"  0.99999998557913294 1.4420867062489483e-08;
	setAttr -s 3 ".pm";
	setAttr ".pm[0]" -type "matrix" 2.2204460492503121e-16 0.99999999999999978 0 0 -0.99999999999999978 2.2204460492503121e-16 0 0
		 0 0 1 0 2.9999999999999996 -5.2735593669694916e-16 0 1;
	setAttr ".pm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".pm[2]" -type "matrix" 2.2204460492503121e-16 -0.99999999999999978 0 0 0.99999999999999978 2.2204460492503121e-16 0 0
		 0 0 1 0 2.9999999999999996 5.2735593669694916e-16 0 1;
	setAttr ".gm" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 3 ".ma";
	setAttr -s 3 ".dpf[0:2]"  10 10 10;
	setAttr -s 3 ".lw";
	setAttr -s 3 ".lw";
	setAttr ".mi" 5;
	setAttr ".bm" 0;
	setAttr ".ucm" yes;
createNode tweak -n "tweak1";
createNode objectSet -n "skinCluster1Set";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "skinCluster1GroupId";
	setAttr ".ihi" 0;
createNode groupParts -n "skinCluster1GroupParts";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode objectSet -n "tweakSet1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "cv[*][*]";
createNode dagPose -n "bindPose1";
	setAttr -s 10 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3877787807814457e-16 3 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3877787807814457e-16 3 0 1;
	setAttr ".wm[3]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[4]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[5]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[7]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3877787807814457e-16 -3 0 1;
	setAttr ".wm[8]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 -1.3877787807814457e-16 -3 0 1;
	setAttr -s 10 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.3877787807814457e-16
		 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 -0.70710678118654746 0.70710678118654768 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.3877787807814457e-16
		 -3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0.70710678118654746 0.70710678118654768 1 1 1 yes;
	setAttr -s 10 ".m";
	setAttr -s 10 ".p";
	setAttr -s 10 ".g[0:9]" yes yes no yes yes yes no yes yes no;
	setAttr ".bp" yes;
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
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
connectAttr "layer1.di" "pCube1.do";
connectAttr "polyCube1.out" "pCubeShape1.i";
connectAttr "skinCluster1GroupId.id" "ribbon01_planeShape.iog.og[0].gid";
connectAttr "skinCluster1Set.mwc" "ribbon01_planeShape.iog.og[0].gco";
connectAttr "groupId2.id" "ribbon01_planeShape.iog.og[1].gid";
connectAttr "tweakSet1.mwc" "ribbon01_planeShape.iog.og[1].gco";
connectAttr "skinCluster1.og[0]" "ribbon01_planeShape.cr";
connectAttr "tweak1.pl[0].cp[0]" "ribbon01_planeShape.twl";
connectAttr "ribbon01_follicle0Shape1.ot" "ribbon01_follicle01.t" -l on;
connectAttr "ribbon01_follicle0Shape1.or" "ribbon01_follicle01.r" -l on;
connectAttr "ribbon01_planeShape.wm" "ribbon01_follicle0Shape1.iwm";
connectAttr "ribbon01_planeShape.l" "ribbon01_follicle0Shape1.is";
connectAttr "ribbon01_follicle0Shape2.ot" "ribbon01_follicle02.t" -l on;
connectAttr "ribbon01_follicle0Shape2.or" "ribbon01_follicle02.r" -l on;
connectAttr "ribbon01_planeShape.wm" "ribbon01_follicle0Shape2.iwm";
connectAttr "ribbon01_planeShape.l" "ribbon01_follicle0Shape2.is";
connectAttr "ribbon01_follicle0Shape3.ot" "ribbon01_follicle03.t" -l on;
connectAttr "ribbon01_follicle0Shape3.or" "ribbon01_follicle03.r" -l on;
connectAttr "ribbon01_planeShape.wm" "ribbon01_follicle0Shape3.iwm";
connectAttr "ribbon01_planeShape.l" "ribbon01_follicle0Shape3.is";
connectAttr "ribbon01_follicle0Shape4.ot" "ribbon01_follicle04.t" -l on;
connectAttr "ribbon01_follicle0Shape4.or" "ribbon01_follicle04.r" -l on;
connectAttr "ribbon01_planeShape.wm" "ribbon01_follicle0Shape4.iwm";
connectAttr "ribbon01_planeShape.l" "ribbon01_follicle0Shape4.is";
connectAttr "ribbon01_follicle0Shape5.ot" "ribbon01_follicle05.t" -l on;
connectAttr "ribbon01_follicle0Shape5.or" "ribbon01_follicle05.r" -l on;
connectAttr "ribbon01_planeShape.wm" "ribbon01_follicle0Shape5.iwm";
connectAttr "ribbon01_planeShape.l" "ribbon01_follicle0Shape5.is";
connectAttr "ribbon01_follicle0Shape6.ot" "ribbon01_follicle06.t" -l on;
connectAttr "ribbon01_follicle0Shape6.or" "ribbon01_follicle06.r" -l on;
connectAttr "ribbon01_planeShape.wm" "ribbon01_follicle0Shape6.iwm";
connectAttr "ribbon01_planeShape.l" "ribbon01_follicle0Shape6.is";
connectAttr "spineTop1_aim_aimConstraint1.crx" "spineTop1_aim.rx";
connectAttr "spineTop1_aim_aimConstraint1.cry" "spineTop1_aim.ry";
connectAttr "spineTop1_aim_aimConstraint1.crz" "spineTop1_aim.rz";
connectAttr "spineTop1_aim.pim" "spineTop1_aim_aimConstraint1.cpim";
connectAttr "spineTop1_aim.t" "spineTop1_aim_aimConstraint1.ct";
connectAttr "spineTop1_aim.rp" "spineTop1_aim_aimConstraint1.crp";
connectAttr "spineTop1_aim.rpt" "spineTop1_aim_aimConstraint1.crt";
connectAttr "spineTop1_aim.ro" "spineTop1_aim_aimConstraint1.cro";
connectAttr "spineBttm1_pos.t" "spineTop1_aim_aimConstraint1.tg[0].tt";
connectAttr "spineBttm1_pos.rp" "spineTop1_aim_aimConstraint1.tg[0].trp";
connectAttr "spineBttm1_pos.rpt" "spineTop1_aim_aimConstraint1.tg[0].trt";
connectAttr "spineBttm1_pos.pm" "spineTop1_aim_aimConstraint1.tg[0].tpm";
connectAttr "spineTop1_aim_aimConstraint1.w0" "spineTop1_aim_aimConstraint1.tg[0].tw"
		;
connectAttr "spineTop1_up.wm" "spineTop1_aim_aimConstraint1.wum";
connectAttr "spineTop01_fk.s" "spineTop02_end.is";
connectAttr "spineBttm1_aim_aimConstraint1.crx" "spineBttm1_aim.rx";
connectAttr "spineBttm1_aim_aimConstraint1.cry" "spineBttm1_aim.ry";
connectAttr "spineBttm1_aim_aimConstraint1.crz" "spineBttm1_aim.rz";
connectAttr "spineBttm1_aim.pim" "spineBttm1_aim_aimConstraint1.cpim";
connectAttr "spineBttm1_aim.t" "spineBttm1_aim_aimConstraint1.ct";
connectAttr "spineBttm1_aim.rp" "spineBttm1_aim_aimConstraint1.crp";
connectAttr "spineBttm1_aim.rpt" "spineBttm1_aim_aimConstraint1.crt";
connectAttr "spineBttm1_aim.ro" "spineBttm1_aim_aimConstraint1.cro";
connectAttr "spineTop1_pos.t" "spineBttm1_aim_aimConstraint1.tg[0].tt";
connectAttr "spineTop1_pos.rp" "spineBttm1_aim_aimConstraint1.tg[0].trp";
connectAttr "spineTop1_pos.rpt" "spineBttm1_aim_aimConstraint1.tg[0].trt";
connectAttr "spineTop1_pos.pm" "spineBttm1_aim_aimConstraint1.tg[0].tpm";
connectAttr "spineBttm1_aim_aimConstraint1.w0" "spineBttm1_aim_aimConstraint1.tg[0].tw"
		;
connectAttr "spineBttm1_up.wm" "spineBttm1_aim_aimConstraint1.wum";
connectAttr "spineBttm01_fk.s" "spineBttm02_end.is";
connectAttr "spineMid1_pos_pointConstraint1.ctx" "spineMid1_pos.tx";
connectAttr "spineMid1_pos_pointConstraint1.cty" "spineMid1_pos.ty";
connectAttr "spineMid1_pos_pointConstraint1.ctz" "spineMid1_pos.tz";
connectAttr "spineMid1_aim_aimConstraint1.crx" "spineMid1_aim.rx";
connectAttr "spineMid1_aim_aimConstraint1.cry" "spineMid1_aim.ry";
connectAttr "spineMid1_aim_aimConstraint1.crz" "spineMid1_aim.rz";
connectAttr "spineMid1_aim.pim" "spineMid1_aim_aimConstraint1.cpim";
connectAttr "spineMid1_aim.t" "spineMid1_aim_aimConstraint1.ct";
connectAttr "spineMid1_aim.rp" "spineMid1_aim_aimConstraint1.crp";
connectAttr "spineMid1_aim.rpt" "spineMid1_aim_aimConstraint1.crt";
connectAttr "spineMid1_aim.ro" "spineMid1_aim_aimConstraint1.cro";
connectAttr "spineTop1_pos.t" "spineMid1_aim_aimConstraint1.tg[0].tt";
connectAttr "spineTop1_pos.rp" "spineMid1_aim_aimConstraint1.tg[0].trp";
connectAttr "spineTop1_pos.rpt" "spineMid1_aim_aimConstraint1.tg[0].trt";
connectAttr "spineTop1_pos.pm" "spineMid1_aim_aimConstraint1.tg[0].tpm";
connectAttr "spineMid1_aim_aimConstraint1.w0" "spineMid1_aim_aimConstraint1.tg[0].tw"
		;
connectAttr "spineMid1_up.wm" "spineMid1_aim_aimConstraint1.wum";
connectAttr "spineMid1_up_pointConstraint1.ctx" "spineMid1_up.tx";
connectAttr "spineMid1_up_pointConstraint1.cty" "spineMid1_up.ty";
connectAttr "spineMid1_up_pointConstraint1.ctz" "spineMid1_up.tz";
connectAttr "spineMid1_up.pim" "spineMid1_up_pointConstraint1.cpim";
connectAttr "spineMid1_up.rp" "spineMid1_up_pointConstraint1.crp";
connectAttr "spineMid1_up.rpt" "spineMid1_up_pointConstraint1.crt";
connectAttr "spineTop1_up.t" "spineMid1_up_pointConstraint1.tg[0].tt";
connectAttr "spineTop1_up.rp" "spineMid1_up_pointConstraint1.tg[0].trp";
connectAttr "spineTop1_up.rpt" "spineMid1_up_pointConstraint1.tg[0].trt";
connectAttr "spineTop1_up.pm" "spineMid1_up_pointConstraint1.tg[0].tpm";
connectAttr "spineMid1_up_pointConstraint1.w0" "spineMid1_up_pointConstraint1.tg[0].tw"
		;
connectAttr "spineBttm1_up.t" "spineMid1_up_pointConstraint1.tg[1].tt";
connectAttr "spineBttm1_up.rp" "spineMid1_up_pointConstraint1.tg[1].trp";
connectAttr "spineBttm1_up.rpt" "spineMid1_up_pointConstraint1.tg[1].trt";
connectAttr "spineBttm1_up.pm" "spineMid1_up_pointConstraint1.tg[1].tpm";
connectAttr "spineMid1_up_pointConstraint1.w1" "spineMid1_up_pointConstraint1.tg[1].tw"
		;
connectAttr "spineMid1_pos.pim" "spineMid1_pos_pointConstraint1.cpim";
connectAttr "spineMid1_pos.rp" "spineMid1_pos_pointConstraint1.crp";
connectAttr "spineMid1_pos.rpt" "spineMid1_pos_pointConstraint1.crt";
connectAttr "spineTop1_pos.t" "spineMid1_pos_pointConstraint1.tg[0].tt";
connectAttr "spineTop1_pos.rp" "spineMid1_pos_pointConstraint1.tg[0].trp";
connectAttr "spineTop1_pos.rpt" "spineMid1_pos_pointConstraint1.tg[0].trt";
connectAttr "spineTop1_pos.pm" "spineMid1_pos_pointConstraint1.tg[0].tpm";
connectAttr "spineMid1_pos_pointConstraint1.w0" "spineMid1_pos_pointConstraint1.tg[0].tw"
		;
connectAttr "spineBttm1_pos.t" "spineMid1_pos_pointConstraint1.tg[1].tt";
connectAttr "spineBttm1_pos.rp" "spineMid1_pos_pointConstraint1.tg[1].trp";
connectAttr "spineBttm1_pos.rpt" "spineMid1_pos_pointConstraint1.tg[1].trt";
connectAttr "spineBttm1_pos.pm" "spineMid1_pos_pointConstraint1.tg[1].tpm";
connectAttr "spineMid1_pos_pointConstraint1.w1" "spineMid1_pos_pointConstraint1.tg[1].tw"
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
connectAttr "layerManager.dli[1]" "layer1.id";
connectAttr "skinCluster1GroupParts.og" "skinCluster1.ip[0].ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1.ip[0].gi";
connectAttr "bindPose1.msg" "skinCluster1.bp";
connectAttr "spineTop01_fk.wm" "skinCluster1.ma[0]";
connectAttr "mid01_fk.wm" "skinCluster1.ma[1]";
connectAttr "spineBttm01_fk.wm" "skinCluster1.ma[2]";
connectAttr "spineTop01_fk.liw" "skinCluster1.lw[0]";
connectAttr "mid01_fk.liw" "skinCluster1.lw[1]";
connectAttr "spineBttm01_fk.liw" "skinCluster1.lw[2]";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "skinCluster1GroupId.msg" "skinCluster1Set.gn" -na;
connectAttr "ribbon01_planeShape.iog.og[0]" "skinCluster1Set.dsm" -na;
connectAttr "skinCluster1.msg" "skinCluster1Set.ub[0]";
connectAttr "tweak1.og[0]" "skinCluster1GroupParts.ig";
connectAttr "skinCluster1GroupId.id" "skinCluster1GroupParts.gi";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "ribbon01_planeShape.iog.og[1]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "ribbon01_planeShapeOrig.ws" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "spineTop1_pos.msg" "bindPose1.m[0]";
connectAttr "spineTop1_aim.msg" "bindPose1.m[1]";
connectAttr "spineTop01_fk.msg" "bindPose1.m[2]";
connectAttr "spineMid1_pos.msg" "bindPose1.m[3]";
connectAttr "spineMid1_aim.msg" "bindPose1.m[4]";
connectAttr "spineMid1_off.msg" "bindPose1.m[5]";
connectAttr "mid01_fk.msg" "bindPose1.m[6]";
connectAttr "spineBttm1_pos.msg" "bindPose1.m[7]";
connectAttr "spineBttm1_aim.msg" "bindPose1.m[8]";
connectAttr "spineBttm01_fk.msg" "bindPose1.m[9]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "bindPose1.w" "bindPose1.p[3]";
connectAttr "bindPose1.m[3]" "bindPose1.p[4]";
connectAttr "bindPose1.m[4]" "bindPose1.p[5]";
connectAttr "bindPose1.m[5]" "bindPose1.p[6]";
connectAttr "bindPose1.w" "bindPose1.p[7]";
connectAttr "bindPose1.m[7]" "bindPose1.p[8]";
connectAttr "bindPose1.m[8]" "bindPose1.p[9]";
connectAttr "spineTop01_fk.bps" "bindPose1.wm[2]";
connectAttr "mid01_fk.bps" "bindPose1.wm[6]";
connectAttr "spineBttm01_fk.bps" "bindPose1.wm[9]";
connectAttr "lightLinker1.msg" ":lightList1.ln" -na;
connectAttr "pCubeShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "ribbon01_planeShape.iog" ":initialShadingGroup.dsm" -na;
// End of test_constrainLocators.ma
