//Maya ASCII 2011 scene
//Name: arrow_cross.ma
//Last modified: Wed, Dec 11, 2013 02:37:59 PM
//Codeset: 1252
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011 x64";
fileInfo "cutIdentifier" "201003190311-771506";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "arrow_cross";
createNode nurbsCurve -n "arrow_crossShape" -p "arrow_cross";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 24 2 no 3
		25 5.5999999999999996 6 7 8 9 10 10.4 10.800000000000001 11.800000000000001
		 12.800000000000001 13.800000000000001 14.800000000000001 15.200000000000001 15.600000000000001
		 16.600000000000001 17.600000000000001 18.600000000000001 19.600000000000001 20 20.400000000000002
		 21.400000000000002 22.400000000000002 23.400000000000002 24.400000000000002 24.800000000000004
		
		25
		-1 0 0.99999999999999645
		-1 0 5
		-2 0 5
		0 0 7
		2 0 5
		1 0 5
		1 0 0.99999999999999656
		5.0000000000000009 0 1.0000000000000013
		5 0 2.0000000000000018
		7.0000000000000018 0 1.5543122344752192e-015
		5.0000000000000018 0 -1.9999999999999993
		5.0000000000000009 0 -0.99999999999999911
		0.99999999999999689 0 -1
		1.0000000000000007 0 -5
		2.0000000000000004 0 -5
		8.5725275940314722e-016 0 -7
		-1.9999999999999993 0 -5
		-0.99999999999999933 0 -5
		-0.99999999999999989 0 -0.99999999999999667
		-5.0000000000000009 0 -1.000000000000002
		-5 0 -2.0000000000000022
		-7.0000000000000018 0 -2.4115649938783668e-015
		-5.0000000000000018 0 1.9999999999999987
		-5.0000000000000009 0 0.99999999999999845
		-0.999999999999997 0 0.99999999999999989
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
// End of arrow_cross.ma
