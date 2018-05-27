//Maya ASCII 2011 scene
//Name: arrow_01.ma
//Last modified: Wed, Dec 11, 2013 02:38:34 PM
//Codeset: 1252
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011 x64";
fileInfo "cutIdentifier" "201003190311-771506";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "arrow_01";
createNode nurbsCurve -n "curveShape1" -p "arrow_01";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 7 0 no 3
		8 0 1 2 3 4 5 6 7
		8
		1 0 -1.2246467991473532e-016
		-1 0 1.2246467991473532e-016
		-0.99999999999999956 8.8817841970012523e-016 4
		-1.9999999999999996 8.8817841970012523e-016 4
		7.3478807948841188e-016 1.3322676295501878e-015 6
		2.0000000000000004 8.8817841970012523e-016 3.9999999999999996
		1.0000000000000004 8.8817841970012523e-016 4
		1 0 -1.2246467991473532e-016
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
// End of arrow_01.ma
