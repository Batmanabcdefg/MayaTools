//Maya ASCII 2011 scene
//Name: pin_circle.ma
//Last modified: Wed, Dec 11, 2013 02:42:32 PM
//Codeset: 1252
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011 x64";
fileInfo "cutIdentifier" "201003190311-771506";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "pin_circle";
createNode nurbsCurve -n "pin_circleShape" -p "pin_circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.21106317830669494 1.9437101466652837 -3.8472491156373612e-016
		-3.405395846102548e-017 1.8562849156930796 -3.4590030982033082e-016
		-0.21106317830669474 1.9437101466652835 -3.8472491156373607e-016
		-0.29848840927889858 2.1547733249719783 -4.7845579164639891e-016
		-0.2110631783066948 2.3658365032786728 -5.7218667172906186e-016
		-8.994038305085259e-017 2.4532617342508773 -6.1101127347246721e-016
		0.21106317830669463 2.3658365032786728 -5.7218667172906196e-016
		0.29848840927889858 2.1547733249719783 -4.7845579164639911e-016
		0.21106317830669494 1.9437101466652837 -3.8472491156373612e-016
		-3.405395846102548e-017 1.8562849156930796 -3.4590030982033082e-016
		-0.21106317830669474 1.9437101466652835 -3.8472491156373607e-016
		;
createNode nurbsCurve -n "curveShape5" -p "pin_circle";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 1.8854266593504809 -4.1864881769059912e-016
		0 0 0
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
// End of pin_circle.ma
