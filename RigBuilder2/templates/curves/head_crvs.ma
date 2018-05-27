//Maya ASCII 2011 scene
//Name: head_crvs.ma
//Last modified: Sat, Dec 28, 2013 01:43:26 AM
//Codeset: UTF-8
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011 x64";
fileInfo "cutIdentifier" "201003190347-771506";
fileInfo "osv" "Mac OS X 10.8.5";
createNode transform -n "curvesExport";
createNode transform -n "head_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "orient" -ln "orient" -at "double";
	addAttr -ci true -k true -sn "local" -ln "local" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "world" -ln "world" -min 0 -max 1 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 4.5917805552044849e-07 16.618162384110772 1.4506812079430047 ;
	setAttr ".r" -type "double3" -5.10490710312571e-15 -89.999999997818961 0 ;
	setAttr ".s" -type "double3" 1 0.99999999999999989 0.99999999999999989 ;
	setAttr -l on -k on ".orient";
	setAttr -k on ".local" 1;
	setAttr -k on ".world";
createNode nurbsCurve -n "head_ctrl_exportShape" -p "head_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		3.7279810844557193e-17 1.3336266429600898 0.78361162489122582
		1.0345642190184331e-16 1.658209205623254 -1.2643160019917483e-16
		9.279096207581502e-17 1.3336266429600905 -0.78361162489122405
		1.7605768892270176e-16 0.55001501806886621 -1.1081941875543877
		2.5932441576958848e-16 -0.23359660682235805 -0.78361162489122382
		4.3652332928939028e-16 -0.55817916948552249 -3.3392043047993344e-16
		5.091245963102487e-16 -0.23359660682235828 0.78361162489122449
		6.5035386460186106e-17 0.55001501806886521 1.1081941875543886
		3.7279810844557193e-17 1.3336266429600898 0.78361162489122582
		1.0345642190184331e-16 1.658209205623254 -1.2643160019917483e-16
		9.279096207581502e-17 1.3336266429600905 -0.78361162489122405
		;
createNode transform -n "neck1_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "orient" -ln "orient" -at "double";
	addAttr -ci true -k true -sn "local" -ln "local" -min 0 -max 1 -at "double";
	addAttr -ci true -k true -sn "world" -ln "world" -min 0 -max 1 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" -2.4820932331692887e-06 15.462670247034048 0.32716794369672891 ;
	setAttr ".r" -type "double3" -89.999790710401314 -40.605725111626533 89.999863783801459 ;
	setAttr -l on -k on ".orient";
	setAttr -k on ".local" 1;
	setAttr -k on ".world";
createNode nurbsCurve -n "neck1_ctrl_exportShape" -p "neck1_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		-0.43081555229731383 1.5113720904688777 -0.87974680412157569
		-0.62894425689553868 2.1346817567019647 -0.097997352989327616
		-0.45864594578102502 1.5075238012094634 0.68722459782773015
		-0.0196790599554253 -0.0027211514312984277 1.0159466790140323
		0.43081555229730611 -1.5113720904688748 0.69560795366214423
		0.62894425689552835 -2.134681756701958 -0.086141497470102912
		0.45864594578101736 -1.5075238012094625 -0.87136344828716261
		0.019679059955419693 0.0027211514313002891 -1.2000855294734578
		-0.43081555229731383 1.5113720904688777 -0.87974680412157569
		-0.62894425689553868 2.1346817567019647 -0.097997352989327616
		-0.45864594578102502 1.5075238012094634 0.68722459782773015
		;
createNode transform -n "neck2_ctrl_export" -p "curvesExport";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" -1.0363295278126946e-06 16.070793274912219 0.84849783071778995 ;
	setAttr ".r" -type "double3" -89.999777285440899 -47.729974692446291 89.999843457967785 ;
createNode nurbsCurve -n "neck2_ctrl_exportShape" -p "neck2_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.10778954732018511 -1.0253026519723134 -1.3080636407161881
		0.0029153867432336888 0.21096671073709422 -1.821981582739999
		-0.10366656784834374 1.4470900110943357 -1.3080636407161885
		-0.14952205295902768 1.9589629845155334 -0.067355975135439033
		-0.10778954732017854 1.4467373853827901 1.1733516904453107
		-0.0029153867432266459 0.21046802267338516 1.6872696324691201
		0.10366656784834957 -1.0256552776838581 1.1733516904453107
		0.14952205295903395 -1.5375282511050554 -0.067355975135437549
		0.10778954732018511 -1.0253026519723134 -1.3080636407161881
		0.0029153867432336888 0.21096671073709422 -1.821981582739999
		-0.10366656784834374 1.4470900110943357 -1.3080636407161885
		;
createNode transform -n "face_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "Neutral" -ln "Neutral" -min -10 -max 10 -at "double";
	addAttr -ci true -k true -sn "L_Ear_Up_Down" -ln "L_Ear_Up_Down" -min -10 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "R_Ear_Up_Down" -ln "R_Ear_Up_Down" -min -10 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "R_Ear_BackL_Ear_Back" -ln "R_Ear_BackL_Ear_Back" -min 
		-10 -max 10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 3.0000004591780556 16.618162384110775 1.4506812079430043 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode nurbsCurve -n "face_ctrl_exportShape" -p "face_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.9367405251947305 6.1808594351369621e-16 -0.92411623169072687
		-1.2643170607829326e-16 6.9015775040579278e-16 -1.248698794353891
		-0.9367405251947305 6.1808594351369631e-16 -0.92411623169072732
		-0.95506528725088224 7.1304506904229069e-32 -3.2112695072372299e-16
		-0.69506583253254806 4.8047871261397635e-17 0.89966155634164025
		-3.3392053635905195e-16 -2.4023935630698855e-17 1.0389791250371461
		0.69506583253254806 4.8047871261397561e-17 0.89966155634164036
		0.95506528725088224 -1.3216389314686572e-31 5.9521325992805852e-16
		0.9367405251947305 6.1808594351369621e-16 -0.92411623169072687
		-1.2643170607829326e-16 6.9015775040579278e-16 -1.248698794353891
		-0.9367405251947305 6.1808594351369631e-16 -0.92411623169072732
		;
createNode transform -n "mouth_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "JawOpenClose" -ln "JawOpenClose" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "JawLeftRight" -ln "JawLeftRight" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "L_LipStretch" -ln "L_LipStretch" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "R_LipStretch" -ln "R_LipStretch" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "L_narrow" -ln "L_narrow" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "R_narrow" -ln "R_narrow" -min 0 -max 10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 2.9882169677465393 15.911132956363454 1.4758956082632444 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 0.45008998737082884 0.51286965812776386 0.095745753544860882 ;
createNode nurbsCurve -n "mouth_ctrl_exportShape" -p "mouth_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.93792276071411651 1.7399673366363362e-16 -0.78361162489122382
		-1.2643170607829326e-16 2.4606854055573011e-16 -1.1081941875543879
		-0.9379227607141164 1.7399673366363372e-16 -0.78361162489122427
		-0.95388305173149468 7.1304506904229069e-32 -3.2112695072372299e-16
		-0.93792276071411651 -1.7399673366363367e-16 0.78361162489122405
		-3.3392053635905195e-16 -2.4606854055573016e-16 1.1081941875543881
		0.9379227607141164 -1.7399673366363375e-16 0.78361162489122438
		0.95388305173149468 -1.3216389314686572e-31 5.9521325992805852e-16
		0.93792276071411651 1.7399673366363362e-16 -0.78361162489122382
		-1.2643170607829326e-16 2.4606854055573011e-16 -1.1081941875543879
		-0.9379227607141164 1.7399673366363372e-16 -0.78361162489122427
		;
createNode transform -n "nose_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "L_sneerA" -ln "L_sneerA" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "R_sneerA" -ln "R_sneerA" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "L_sneerB" -ln "L_sneerB" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "R_sneerB" -ln "R_sneerB" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "L_Nostril_Dialate" -ln "L_Nostril_Dialate" -min 0 
		-max 10 -at "double";
	addAttr -ci true -k true -sn "R_Nostril_Dialate" -ln "R_Nostril_Dialate" -min 0 
		-max 10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 2.9760268051991723 16.15817038794528 1.485878983588484 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 0.28814614971423425 0.70121403056110476 0.70121403056110476 ;
createNode nurbsCurve -n "nose_ctrl_exportShape" -p "nose_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.37215347152503953 1.7399673366363362e-16 -0.70232132874213826
		-1.2643170607829324e-16 2.4606854055573011e-16 -0.72142845632709451
		-0.37215347152503919 1.7399673366363372e-16 -0.70232132874213826
		-0.52630448671494023 7.1304506904229069e-32 -0.22118986359868001
		-0.37215347152504097 -1.7399673366363367e-16 -0.21710706649321493
		-3.3392053635905155e-16 -2.4606854055573016e-16 -0.19779789766412265
		0.37215347152504064 -1.7399673366363375e-16 -0.21710706649321493
		0.52630448671494023 -1.3216389314686572e-31 -0.22118986359867954
		0.37215347152503953 1.7399673366363362e-16 -0.70232132874213826
		-1.2643170607829324e-16 2.4606854055573011e-16 -0.72142845632709451
		-0.37215347152503919 1.7399673366363372e-16 -0.70232132874213826
		;
createNode transform -n "Left_eye_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "UpperLidOpenClose" -ln "UpperLidOpenClose" -min 0 
		-max 10 -at "double";
	addAttr -ci true -k true -sn "LowerLidSquint" -ln "LowerLidSquint" -min 0 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "Squint" -ln "Squint" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "EyeBallUpDown" -ln "EyeBallUpDown" -min 0 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "EyeBallLeftRight" -ln "EyeBallLeftRight" -min 0 -max 
		10 -at "double";
	addAttr -ci true -k true -sn "PupilDialate" -ln "PupilDialate" -min 0 -max 10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 3.4026824943570411 16.825395147416032 1.2673969839887822 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 0.70121403056110465 0.70121403056110476 0.70121403056110476 ;
createNode nurbsCurve -n "Left_eye_ctrl_exportShape" -p "Left_eye_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.2554092587947337 0.33703071095315401 -0.25540925879473303
		-4.1208970505118536e-17 0.33703071095315401 -0.36120323774317165
		-0.25540925879473336 0.33703071095315401 -0.25540925879473325
		-0.3612032377431717 0.33703071095315396 4.5004040415937535e-17
		-0.25540925879473347 0.33703071095315384 0.25540925879473331
		-1.0883758481715246e-16 0.33703071095315384 0.36120323774317181
		0.25540925879473314 0.33703071095315384 0.25540925879473353
		0.3612032377431717 0.33703071095315396 3.4367466572585357e-16
		0.2554092587947337 0.33703071095315401 -0.25540925879473303
		-4.1208970505118536e-17 0.33703071095315401 -0.36120323774317165
		-0.25540925879473336 0.33703071095315401 -0.25540925879473325
		;
createNode transform -n "Right_eye_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "UpperLidOpenClose" -ln "UpperLidOpenClose" -min 0 
		-max 10 -at "double";
	addAttr -ci true -k true -sn "LowerLidSquint" -ln "LowerLidSquint" -min 0 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "Squint" -ln "Squint" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "EyeBallUpDown" -ln "EyeBallUpDown" -min 0 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "EyeBallLeftRight" -ln "EyeBallLeftRight" -min 0 -max 
		10 -at "double";
	addAttr -ci true -k true -sn "PupilDialate" -ln "PupilDialate" -min 0 -max 10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 2.5493711160413035 16.849775472510778 1.764773159153906 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 0.70121403056110465 0.70121403056110476 0.70121403056110476 ;
createNode nurbsCurve -n "Right_eye_ctrl_exportShape" -p "Right_eye_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.2554092587947337 -0.33703071095315384 -0.25540925879473303
		-4.1208970505118536e-17 -0.33703071095315384 -0.36120323774317165
		-0.25540925879473336 -0.33703071095315384 -0.25540925879473325
		-0.3612032377431717 -0.33703071095315396 4.5004040415937535e-17
		-0.25540925879473347 -0.33703071095315401 0.25540925879473331
		-1.0883758481715246e-16 -0.33703071095315401 0.36120323774317181
		0.25540925879473314 -0.33703071095315401 0.25540925879473353
		0.3612032377431717 -0.33703071095315396 3.4367466572585357e-16
		0.2554092587947337 -0.33703071095315384 -0.25540925879473303
		-4.1208970505118536e-17 -0.33703071095315384 -0.36120323774317165
		-0.25540925879473336 -0.33703071095315384 -0.25540925879473325
		;
createNode transform -n "Left_brow_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "BrowLower" -ln "BrowLower" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "BrowInnerRaise" -ln "BrowInnerRaise" -min 0 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "BrowOutterRaise" -ln "BrowOutterRaise" -min 0 -max 
		10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 3.4026824943570402 17.288621324215999 1.4853670595742141 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode nurbsCurve -n "Left_brow_ctrl_exportShape" -p "Left_brow_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.18573159900006997 -6.7574338902737355e-16 -0.0653085118247025
		-1.2643170607829326e-16 -6.6132902764895421e-16 -0.071243765369914877
		-0.18573159900006994 -6.7574338902737345e-16 -0.0653085118247025
		-0.19262956348905266 -7.1054273576010023e-16 -6.4225390144744601e-17
		-0.18573159900006994 -7.4534208249282691e-16 0.062677569642920747
		-3.3392053635905195e-16 -7.5975644387124624e-16 0.072387735941933234
		0.18573159900006991 -7.45342082492827e-16 0.062677569642920775
		0.19262956348905266 -7.1054273576010023e-16 1.1904265198561171e-16
		0.18573159900006997 -6.7574338902737355e-16 -0.0653085118247025
		-1.2643170607829326e-16 -6.6132902764895421e-16 -0.071243765369914877
		-0.18573159900006994 -6.7574338902737345e-16 -0.0653085118247025
		;
createNode transform -n "Right_brow_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "BrowLower" -ln "BrowLower" -min 0 -max 10 -at "double";
	addAttr -ci true -k true -sn "BrowInnerRaise" -ln "BrowInnerRaise" -min 0 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "BrowOutterRaise" -ln "BrowOutterRaise" -min 0 -max 
		10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 2.5371809534939356 17.300811486763365 1.4953504348994549 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 1 1.0000000000000002 1.0000000000000002 ;
createNode nurbsCurve -n "Right_brow_ctrl_exportShape" -p "Right_brow_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.18573159900006997 3.4799346732726723e-17 -0.0653085118247025
		-1.2643170607829326e-16 4.9213708111146037e-17 -0.071243765369914877
		-0.18573159900006994 3.4799346732726742e-17 -0.0653085118247025
		-0.19262956348905266 1.4260901380845814e-32 -6.4225390144744601e-17
		-0.18573159900006994 -3.4799346732726723e-17 0.062677569642920747
		-3.3392053635905195e-16 -4.9213708111146037e-17 0.072387735941933234
		0.18573159900006991 -3.479934673272676e-17 0.062677569642920775
		0.19262956348905266 -2.6432778629373145e-32 1.1904265198561171e-16
		0.18573159900006997 3.4799346732726723e-17 -0.0653085118247025
		-1.2643170607829326e-16 4.9213708111146037e-17 -0.071243765369914877
		-0.18573159900006994 3.4799346732726742e-17 -0.0653085118247025
		;
createNode transform -n "Left_cheek_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "L_CheekRaise" -ln "L_CheekRaise" -min -10 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "R_CheekRaise" -ln "R_CheekRaise" -min -10 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "L_CheekPuff" -ln "L_CheekPuff" -min -10 -max 10 -at "double";
	addAttr -ci true -k true -sn "R_CheekPuff" -ln "R_CheekPuff" -min -10 -max 10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 3.4026824943570402 16.362168970616054 1.5205648352196961 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 0.11328616992325767 0.1132861699232577 0.1132861699232577 ;
createNode nurbsCurve -n "Left_cheek_ctrl_exportShape" -p "Left_cheek_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122504 1.7399673366363362e-16 -0.78361162489122382
		-1.2643170607829326e-16 2.4606854055573011e-16 -1.1081941875543879
		-0.78361162489122427 1.7399673366363372e-16 -0.78361162489122427
		-1.1081941875543879 7.1304506904229069e-32 -3.2112695072372299e-16
		-0.78361162489122449 -1.7399673366363367e-16 0.78361162489122405
		-3.3392053635905195e-16 -2.4606854055573016e-16 1.1081941875543881
		0.78361162489122382 -1.7399673366363375e-16 0.78361162489122438
		1.1081941875543879 -1.3216389314686572e-31 5.9521325992805852e-16
		0.78361162489122504 1.7399673366363362e-16 -0.78361162489122382
		-1.2643170607829326e-16 2.4606854055573011e-16 -1.1081941875543879
		-0.78361162489122427 1.7399673366363372e-16 -0.78361162489122427
		;
createNode transform -n "Right_cheek_ctrl_export" -p "curvesExport";
	addAttr -ci true -k true -sn "L_CheekRaise" -ln "L_CheekRaise" -min -10 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "R_CheekRaise" -ln "R_CheekRaise" -min -10 -max 10 
		-at "double";
	addAttr -ci true -k true -sn "L_CheekPuff" -ln "L_CheekPuff" -min -10 -max 10 -at "double";
	addAttr -ci true -k true -sn "R_CheekPuff" -ln "R_CheekPuff" -min -10 -max 10 -at "double";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".t" -type "double3" 2.561561278588671 16.37435913316342 1.5153171855499452 ;
	setAttr ".r" -type "double3" 90.000000000000028 0 0 ;
	setAttr ".s" -type "double3" 0.1132861699232577 0.11328616992325773 0.11328616992325773 ;
createNode nurbsCurve -n "Right_cheek_ctrl_exportShape" -p "Right_cheek_ctrl_export";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78361162489122504 1.7399673366363362e-16 -0.78361162489122382
		-1.2643170607829326e-16 2.4606854055573011e-16 -1.1081941875543879
		-0.78361162489122427 1.7399673366363372e-16 -0.78361162489122427
		-1.1081941875543879 7.1304506904229069e-32 -3.2112695072372299e-16
		-0.78361162489122449 -1.7399673366363367e-16 0.78361162489122405
		-3.3392053635905195e-16 -2.4606854055573016e-16 1.1081941875543881
		0.78361162489122382 -1.7399673366363375e-16 0.78361162489122438
		1.1081941875543879 -1.3216389314686572e-31 5.9521325992805852e-16
		0.78361162489122504 1.7399673366363362e-16 -0.78361162489122382
		-1.2643170607829326e-16 2.4606854055573011e-16 -1.1081941875543879
		-0.78361162489122427 1.7399673366363372e-16 -0.78361162489122427
		;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -s 5 ".st";
select -ne :initialShadingGroup;
	setAttr -s 17 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 31 ".gn";
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 3 ".u";
select -ne :renderGlobalsList1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
// End of head_crvs.ma
