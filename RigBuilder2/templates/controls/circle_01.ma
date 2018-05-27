//Maya ASCII 2011 scene
//Name: circle_01.ma
//Last modified: Wed, Dec 11, 2013 02:40:48 PM
//Codeset: 1252
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011 x64";
fileInfo "cutIdentifier" "201003190311-771506";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "circle_01";
createNode nurbsCurve -n "circle_01Shape" -p "circle_01";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122504 1.7399673366363362e-016 -0.78361162489122382
		-1.2643170607829326e-016 2.4606854055573011e-016 -1.1081941875543879
		-0.78361162489122427 1.7399673366363372e-016 -0.78361162489122427
		-1.1081941875543879 7.1304506904229069e-032 -3.2112695072372299e-016
		-0.78361162489122449 -1.7399673366363367e-016 0.78361162489122405
		-3.3392053635905195e-016 -2.4606854055573016e-016 1.1081941875543881
		0.78361162489122382 -1.7399673366363375e-016 0.78361162489122438
		1.1081941875543879 -1.3216389314686572e-031 5.9521325992805852e-016
		0.78361162489122504 1.7399673366363362e-016 -0.78361162489122382
		-1.2643170607829326e-016 2.4606854055573011e-016 -1.1081941875543879
		-0.78361162489122427 1.7399673366363372e-016 -0.78361162489122427
		;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 11 ".st";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -s 11 ".s";
select -ne :defaultTextureList1;
	setAttr -s 8 ".tx";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 12 ".u";
select -ne :renderGlobalsList1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
// End of circle_01.ma
