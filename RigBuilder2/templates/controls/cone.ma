//Maya ASCII 2011 scene
//Name: cone.ma
//Last modified: Wed, Dec 11, 2013 02:39:55 PM
//Codeset: 1252
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011 x64";
fileInfo "cutIdentifier" "201003190311-771506";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -n "cone";
createNode nurbsCurve -n "curveShape4" -p "cone";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
		16
		0.80489488814990962 -3.7865033318023406e-008 1.3941193724439322
		1.6097902601825513 -3.7865033318023406e-008 -5.3721774814680021e-017
		0.80489537203264017 -3.7865033318023406e-008 -1.3941188885612021
		-0.80489488814991128 -3.7865033318023406e-008 -1.3941193724439322
		-1.6097902601825513 -3.7865033318023406e-008 -5.3721774814680021e-017
		-0.80489537203264017 -3.7865033318023406e-008 1.3941193724439322
		0.80489488814990962 -3.7865033318023406e-008 1.3941193724439322
		0 3.4186276547770573 -5.3721774814680021e-017
		-0.80489537203264017 -3.7865033318023406e-008 1.3941193724439322
		-1.6097902601825513 -3.7865033318023406e-008 -5.3721774814680021e-017
		0 3.4186276547770573 -5.3721774814680021e-017
		-0.80489488814991128 -3.7865033318023406e-008 -1.3941193724439322
		0.80489537203264017 -3.7865033318023406e-008 -1.3941188885612021
		0 3.4186276547770573 -5.3721774814680021e-017
		1.6097902601825513 -3.7865033318023406e-008 -5.3721774814680021e-017
		0.80489488814990962 -3.7865033318023406e-008 1.3941193724439322
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
// End of cone.ma
