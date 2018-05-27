//Maya ASCII 2015 scene
//Name: pointed_circle.ma
//Last modified: Thu, Oct 15, 2015 05:34:08 PM
//Codeset: UTF-8
requires maya "2015";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2015";
fileInfo "version" "2015";
fileInfo "cutIdentifier" "201410051530-933320";
fileInfo "osv" "Mac OS X 10.9.5";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 5.9257416092526487 8.5335468152729081 10.56923885789376 ;
	setAttr ".r" -type "double3" -41.738352729584747 37.399999999995806 2.0018228512207608e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 15.492762034278233;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0.00195344652792806 100.1 0.23062864450637216 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 4.2926368901171452;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
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
createNode transform -n "pointed_circle";
createNode nurbsCurve -n "pointed_circleShape1" -p "pointed_circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122504 4.7982373409884682e-17 -0.78361162489122382
		-1.2643170607829326e-16 6.7857323231109134e-17 -1.1081941875543879
		-0.78361162489122427 4.7982373409884713e-17 -0.78361162489122427
		-1.1081941875543879 1.9663354616187859e-32 -3.2112695072372299e-16
		-0.78361162489122449 -4.7982373409884694e-17 0.78361162489122405
		-3.3392053635905195e-16 -6.7857323231109146e-17 1.1081941875543881
		0.78361162489122382 -4.7982373409884719e-17 0.78361162489122438
		1.1081941875543879 -3.6446300679047921e-32 5.9521325992805852e-16
		0.78361162489122504 4.7982373409884682e-17 -0.78361162489122382
		-1.2643170607829326e-16 6.7857323231109134e-17 -1.1081941875543879
		-0.78361162489122427 4.7982373409884713e-17 -0.78361162489122427
		;
createNode nurbsCurve -n "pointed_circleShape2" -p "pointed_circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 13 0 no 3
		18 0 0 0 0.076923076923076927 0.15384615384615385 0.23076923076923078 0.30769230769230771
		 0.38461538461538464 0.46153846153846156 0.53846153846153844 0.61538461538461542 0.69230769230769229
		 0.76923076923076927 0.84615384615384615 0.92307692307692313 1 1 1
		16
		0.47541766285976206 0 1.1130841637767004
		0.44650684164425625 0 1.1623240228517884
		0.39921336682695985 0 1.2428725489897761
		0.31828260117408791 0 1.3807108871747173
		0.24111718655739139 0 1.512136207320516
		0.16213928553506693 0 1.6466485096732826
		0.084044324124597947 0 1.7796569849858401
		-7.7829021162514741e-15 0 1.9132049736051022
		-7.7829021162514741e-15 0 1.9132049736051022
		-0.08404432061913987 0 1.7796569718997044
		-0.16213928879960485 0 1.6466485175704064
		-0.24111717483483824 0 1.5121361963996718
		-0.31828260668643832 0 1.3807108910096593
		-0.39921336194630141 0 1.2428725442287984
		-0.44650684196292678 0 1.1623240214583059
		-0.47541766285976256 0 1.1130841629259658
		;
createNode nurbsCurve -n "pointed_circleShape3" -p "pointed_circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 13 0 no 3
		18 0 0 0 0.076923076923076927 0.15384615384615385 0.23076923076923078 0.30769230769230771
		 0.38461538461538464 0.46153846153846156 0.53846153846153844 0.61538461538461542 0.69230769230769229
		 0.76923076923076927 0.84615384615384615 0.92307692307692313 1 1 1
		16
		1.0690734378662266 0 -0.33029018592207793
		1.0891588517252533 0 -0.31020477206305153
		1.1220153731208355 0 -0.27734825071223751
		1.178240961903759 0 -0.22112266272395886
		1.2318506187197535 0 -0.16751300298352778
		1.2867194853784873 0 -0.11264414208448764
		1.3409749264701629 0 -0.058388691900572276
		1.3954504402478924 0 1.6653345369377348e-16
		1.3954504402478924 0 1.6653345369377348e-16
		1.3409749211322013 0 0.058388689465201149
		1.2867194885998006 0 0.11264414435248249
		1.2318506142650363 0 0.16751299483943771
		1.1782409634680686 0 0.22112266655359225
		1.1220153711787866 0 0.27734824732146396
		1.0891588511568382 0 0.31020477228444382
		1.069073437519203 0 0.33029018592207815
		;
createNode nurbsCurve -n "pointed_circleShape4" -p "pointed_circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 13 0 no 3
		18 0 0 0 0.076923076923076927 0.15384615384615385 0.23076923076923078 0.30769230769230771
		 0.38461538461538464 0.46153846153846156 0.53846153846153844 0.61538461538461542 0.69230769230769229
		 0.76923076923076927 0.84615384615384615 0.92307692307692313 1 1 1
		16
		-1.069099033558693 0 0.33121600254176597
		-1.0891844474177197 0 0.31113058868273913
		-1.1220409688133017 0 0.27827406733192533
		-1.178266557596225 0 0.22204847934364708
		-1.2318762144122188 0 0.16843881960321538
		-1.2867450810709533 0 0.11356995870417536
		-1.3410005221626291 0 0.059314508520260656
		-1.3954760359403577 0 0.00092581661968904605
		-1.3954760359403577 0 0.00092581661968904605
		-1.341000516824667 0 -0.057462872845512936
		-1.2867450842922661 0 -0.11171832773279472
		-1.2318762099575025 0 -0.16658717821974964
		-1.1782665591605344 0 -0.22019684993390398
		-1.1220409668712532 0 -0.27642243070177719
		-1.0891844468493037 0 -0.30927895566475472
		-1.0690990332116681 0 -0.32936436930239105
		;
createNode nurbsCurve -n "pointed_circleShape5" -p "pointed_circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 13 0 no 3
		18 0 0 0 0.076923076923076927 0.15384615384615385 0.23076923076923078 0.30769230769230771
		 0.38461538461538464 0.46153846153846156 0.53846153846153844 0.61538461538461542 0.69230769230769229
		 0.76923076923076927 0.84615384615384615 0.92307692307692313 1 1 1
		16
		-0.33029018592207771 0 -1.0690734378662261
		-0.31020477206305114 0 -1.0891588517252528
		-0.27734825071223718 0 -1.1220153731208358
		-0.22112266272395875 0 -1.178240961903759
		-0.16751300298352778 0 -1.2318506187197533
		-0.11264414208448761 0 -1.2867194853784873
		-0.058388691900572151 0 -1.3409749264701629
		2.2204460492503131e-16 0 -1.3954504402478927
		2.3592239273284576e-16 0 -1.3954504402478927
		0.058388689465201496 0 -1.3409749211322013
		0.11264414435248257 0 -1.2867194885998006
		0.16751299483943766 0 -1.2318506142650363
		0.2211226665535922 0 -1.1782409634680686
		0.27734824732146413 0 -1.1220153711787866
		0.31020477228444393 0 -1.0891588511568375
		0.33029018592207809 0 -1.069073437519203
		;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of pointed_circle.ma
