//Maya ASCII 2011 scene
//Name: werewolf_body_skeleton.ma
//Last modified: Fri, Jan 03, 2014 10:52:24 AM
//Codeset: 1252
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011 x64";
fileInfo "cutIdentifier" "201003190311-771506";
fileInfo "osv" "Microsoft Windows 7 Business Edition, 64-bit Windows 7 Service Pack 1 (Build 7601)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 17.256595225224345 13.422891103232272 28.76452254787597 ;
	setAttr ".r" -type "double3" -9.9383527297901164 388.20000000042205 0 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 38.694136677406476;
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
	setAttr ".t" -type "double3" -0.13111403464382224 15.282678925957871 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 8.3534301705875524;
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
createNode transform -n "BodyRig";
createNode transform -n "spaces" -p "BodyRig";
createNode transform -n "cog_ctrl_space" -p "spaces";
	setAttr ".t" -type "double3" 0 9.7720558958491708 0.63025663379520191 ;
createNode transform -n "main_ctrl_space" -p "spaces";
createNode transform -n "chest_space" -p "spaces";
	setAttr ".t" -type "double3" 0.00052782630593119738 12.405910437629112 0.72607193603002307 ;
createNode transform -n "hip_ctrl_space" -p "spaces";
	setAttr ".t" -type "double3" 0 9.7720558958491708 0.63025663379520191 ;
createNode transform -n "head_ctrl_space" -p "spaces";
	setAttr ".t" -type "double3" 4.5534039115268234e-007 16.83181431845421 1.4481352045840512 ;
	setAttr ".rp" -type "double3" 0.0023903584231549572 -0.42519597811933707 -0.037857726177846329 ;
	setAttr ".sp" -type "double3" 0.0023903584231549572 -0.42519597811933707 -0.037857726177846329 ;
createNode transform -n "geo" -p "BodyRig";
createNode transform -n "controls" -p "BodyRig";
createNode transform -n "modules" -p "controls";
createNode transform -n "unused_joints" -p "BodyRig";
	setAttr ".v" no;
createNode joint -n "LeftFootIndex1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 1.747247255320197 0.92966823823504574 0.69789288258886839 ;
	setAttr ".jo" -type "double3" 75.393646532552239 -56.867569343426077 -77.689458796019565 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.11653555316664334 -0.53400827044980159 0.83740947686263734 -1.3877787807814457e-017
		 0.073604348041281381 0.84547925290406223 0.52891136578656139 -6.9388939039072284e-018
		 -0.99045538253752774 2.9976021664879227e-015 0.13783372302320551 1.1102230246251565e-016
		 1.7472472553202023 0.92966823823504818 0.69789288258887883 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootIndex2" -p "LeftFootIndex1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.86078152726721169 0.033661837795491145 -0.016129894650517951 ;
	setAttr ".jo" -type "double3" -0.093011989513853283 -5.1066553505972898 33.321525999611048 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.049103369487174121 0.018162617320126313 0.99862854877931895 0
		 -0.00089199284685022632 0.99983504606113993 -0.018140700556442992 0 -0.99879330366886498 7.5495165674510645e-015 0.049111470617696051 0
		 1.866012505357092 0.49846416909465568 1.4343003762023832 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootIndex3" -p "pasted__LeftFootIndex2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.40932934873289928 -0.12121464686731498 -0.086155963263705004 ;
	setAttr ".jo" -type "double3" -7.2189581042214996 11.866836728182548 -32.672289485682775 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.24631133591109133 -0.5132468691149793 0.82213647111982879 0
		 0.14729955663527469 0.85824102170874483 0.49165555958554996 0 -0.95793192159816054 8.1046280797636427e-015 0.28699552885585988 0
		 1.972272077386737 0.38470400937972016 1.8410360222538131 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootIndex4" -p "pasted__LeftFootIndex3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0.4671151756042875 -0.12693104843408443 -0.14222612180766969 ;
	setAttr ".jo" -type "double3" 5.5411223550122092e-015 73.321832071037363 30.88034511240788 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999956 1.3877787807814457e-016 1.1102230246251565e-016 0
		 1.1676237310863956e-018 0.99999999999999978 -2.8968855216614079e-014 0 0 2.8816418789829694e-014 1 0
		 2.2048738953212563 0.036021175290093917 2.1218438276396907 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftFootExtraFinger1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 1.3558726988876029 1.181142052818609 0.3672272303016233 ;
	setAttr ".jo" -type "double3" 170.14344816495546 -6.214562828209246 -121.9247791411396 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.52569791166639246 -0.84375541634770057 0.10825203487007068 5.5511151231257827e-017
		 -0.82641594016555142 0.53672786156852093 0.1701760748647404 1.1102230246251565e-016
		 -0.20168886808617018 -5.3845816694320092e-015 -0.9794496416305023 2.7755575615628914e-017
		 1.3558726988876082 1.1811420528186107 0.36722723030163346 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootExtraFinger2" -p "LeftFootExtraFinger1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.354360602671415 0.0040347346131415773 -0.041153971614893647 ;
	setAttr ".jo" -type "double3" 59.953419004598743 -14.280480300946941 -24.340907268897528 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.18382389755190109 -0.95938340953841783 -0.21399123391220334 0
		 -0.62514783120408068 0.28210542976419162 -0.72774082999265199 0 0.75855056774724106 -5.2180482157382357e-015 -0.65161417738592708 0
		 1.1745519990400215 0.88431392945527731 0.44658234466806362 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootExtraFinger3" -p "pasted__LeftFootExtraFinger2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.23830111546017807 -0.089639697467922885 -0.085787801015022147 ;
	setAttr ".jo" -type "double3" 109.79559346994861 -40.893075454098785 -29.644735163965173 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.6095573244188125 -0.73578239190517414 -0.29506633154204226 2.3656741326605687e-018
		 0.66227052532794417 0.67721803856830354 -0.3205830306169502 1.6650903758072238e-016
		 0.43570359136599568 4.5957802640577836e-015 0.90009020685194252 -1.5922276896918494e-018
		 1.1217102365012952 0.63040394743016281 0.51672301015183419 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootExtraFinger4" -p "pasted__LeftFootExtraFinger3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0.21818775986424704 -0.12136030487806582 -0.041594051213146299 ;
	setAttr ".jo" -type "double3" 0 -25.830072940977757 47.373368603371922 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999956 5.5511151231257827e-017 -1.6653345369377348e-016 0
		 -5.5511151231257827e-017 0.99999999999999956 -5.6621374255882984e-015 0 -1.1102230246251565e-016 5.1246347110087911e-015 0.99999999999999978 0
		 1.1562121532664951 0.38767784796324045 0.45381080443547051 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftFootMiddle1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 2.1000573647170313 0.88964476581435592 0.73893749106738649 ;
	setAttr ".jo" -type "double3" 57.853056754513155 -65.011125346209312 -60.333614013074246 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.20908737127140595 -0.36706940040931735 0.90638983139593832 0
		 0.082509253421952269 0.93019355796691272 0.35767606547909758 0 -0.97440992106739399 4.2188474935755949e-015 0.22477834799071444 0
		 2.1000573647170366 0.8896447658143587 0.73893749106739759 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootMiddle2" -p "LeftFootMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.78939657704902466 -0.075579977905392504 -0.081914358998106618 ;
	setAttr ".jo" -type "double3" -1.4963468257170149 2.7957527829653297 -6.6365346651339294 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.24544240188536484 -0.47155082184596608 0.84699341778619319 0
		 0.13124683890294694 0.88183888688149459 0.45291770208459481 0 -0.96048544738310593 -2.1649348980190553e-015 0.278330209221481 0
		 2.3386923364378718 0.5295774290329277 1.4089927980248838 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootMiddle3" -p "pasted__LeftFootMiddle2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.51266793885190975 0.054356337552470269 -0.00837133452472405 ;
	setAttr ".jo" -type "double3" 3.7095119313111566 -5.7128490378625578 -4.94180206682912 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.13645605484099443 -0.54305224394440266 0.82853726859096721 -1.3877787807814457e-017
		 0.088249211535056632 0.83969891053100043 0.53583375809712819 2.0816681711721685e-017
		 -0.98670756648597335 4.4408920985006262e-015 0.16250593293577853 5.5511151231257827e-017
		 2.4796974291835805 0.33576197333545754 1.8655081199507351 0.99999999999999978;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootMiddle4" -p "pasted__LeftFootMiddle3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0.44400377723162299 -0.040634706186603697 0.021905148998346391 ;
	setAttr ".jo" -type "double3" 0 80.647620431029949 32.891661037224686 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999933 2.5326962749261384e-016 3.3306690738754696e-016 0
		 -1.8114911978861652e-016 0.99999999999999978 -2.9096864136598284e-014 0 -3.3306690738754701e-016 2.8921646528334099e-014 1.0000000000000002 0
		 2.5150844759155113 0.060523807275395691 2.2151680661312314 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftFootRing1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 2.3456807958272061 0.86941853733486862 0.61811697627767681 ;
	setAttr ".jo" -type "double3" 45.443652129683123 -59.241109196980673 -49.764732170114108 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.3303445085997726 -0.39042221552297307 0.85932706187115249 0
		 0.14009211720182854 0.92063591806214728 0.36442242668608626 0 -0.93340596973443579 4.6074255521943996e-015 0.35882209472678323 0
		 2.345680795827211 0.86941853733487184 0.61811697627768825 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootRing2" -p "LeftFootRing1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 0.83773810289475237 0.0055482395654582461 -0.23072021836456291 ;
	setAttr ".jo" -type "double3" -0.6555034020905236 3.1901224817403766 11.362976447075848 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.4028696273709173 -0.20107011584457324 0.89289801873241237 0
		 0.082693912682568066 0.97957685176521503 0.18327822645092859 0 -0.91151400436157115 7.7993167479917247e-015 0.41126903585455377 0
		 2.8385558715506685 0.54745487980066365 1.2572423897326359 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootRing3" -p "pasted__LeftFootRing2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.48838107456599378 -0.035297366582665912 0.035105767227488371 ;
	setAttr ".jo" -type "double3" 8.1388928153639295 -12.378619140197877 -22.108986534768 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.13876740269654256 -0.54206656720186397 0.8287987962532537 -5.5511151231257827e-017
		 0.089513254095237221 0.84033555007626981 0.5346246726623215 0 -0.98627125340351296 4.6629367034256575e-015 0.16513332404412784 -5.5511151231257827e-017
		 3.0003914972642538 0.41467955732873135 1.7012855598939429 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootRing4" -p "pasted__LeftFootRing3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0.47185401987606079 -0.13597488590835893 0.12584974526552495 ;
	setAttr ".jo" -type "double3" 0 80.495020381669846 32.824430141483091 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999967 1.6653345369377348e-016 -3.3306690738754696e-016 5.5511151231257827e-017
		 -6.9388939039072259e-017 1 -2.8921309791485328e-014 -6.1629758220391547e-033 2.7755575615628899e-016 2.8740154187555053e-014 1 0
		 2.9295759135379482 0.044638738007756862 2.0404440614712303 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftFootPinky1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 2.5181735264503029 0.8241111066101432 0.29628058469405344 ;
	setAttr ".jo" -type "double3" 36.195568086615744 -45.329558543532066 -45.818256959879882 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.48996590256417416 -0.50416431798072625 0.71116225630969965 0
		 0.28603648588363667 0.86360774688224562 0.41516838543934309 0 -0.8234783197314991 5.7176485768195562e-015 0.5673477389856999 0
		 2.5181735264503087 0.82411110661014619 0.29628058469406482 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootPinky2" -p "LeftFootPinky1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 1.0109990005113467 0.083854483410161107 -0.16106813387323959 ;
	setAttr ".jo" -type "double3" 0.52380098361563465 -4.2829090529061338 23.296604061045741 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.50007275967998999 -0.12117124079614908 0.85746414818927585 0
		 0.061044233972061865 0.99263161868032423 0.10467125247575119 0 -0.86382917091563971 1.0880185641326534e-014 0.50378483847293087 0
		 3.1701501222317821 0.38681886652196984 0.9586970039381838 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootPinky3" -p "pasted__LeftFootPinky2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 0.29689639966845816 -0.017647733791034237 -0.016447616916739793 ;
	setAttr ".jo" -type "double3" 7.1821047509279863 -22.446259109930224 -11.304886890188008 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.11233462294205568 -0.28966141303219006 0.9505141757431399 0
		 0.033996461834787189 0.95712917926484409 0.28765947712967976 0 -0.99308870352611556 4.4131365228849972e-015 0.11736620863271463 0
		 3.3317505630471502 0.33332586282719934 1.2031417519494298 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__LeftFootPinky4" -p "pasted__LeftFootPinky3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0.39320538321118637 -0.21026380714205395 0.11202294746580543 ;
	setAttr ".jo" -type "double3" -1.3549703609395524e-014 83.259876758345456 16.83768640411051 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999989 4.6837533851373792e-017 0 0 -5.5319324219374861e-017 0.99999999999999978 -3.7966369875501939e-014 0
		 8.3266726846886741e-017 3.7601607401111644e-014 1 0 3.2575241923502318 0.01817981075540814 1.5295523744723212 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightFootExtraFinger1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -1.3558699999999917 1.1811399999999987 0.36722699999999531 ;
	setAttr ".jo" -type "double3" -9.8565518350445185 6.2145628282091376 121.92477914113957 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.52569791166639301 0.84375541634770113 -0.1082520348700696 0
		 -0.82641594016555098 -0.53672786156852104 -0.17017607486474134 0 -0.20168886808617092 4.3298697960381105e-015 0.97944964163050219 0
		 -1.3558699999999986 1.1811399999999996 0.36722700000000014 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootExtraFinger2" -p "RightFootExtraFinger1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -0.35435843078328788 -0.0040352764537716079 0.041154000750202924 ;
	setAttr ".jo" -type "double3" 59.953419004598729 -14.280480300946914 -24.340907268897514 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.18382389755190165 0.95938340953841805 0.21399123391220418 0
		 -0.62514783120408113 -0.28210542976419239 0.72774082999265177 0 0.75855056774723995 5.1070259132757201e-015 0.65161417738592731 0
		 -1.1745499999999984 0.88431399999999927 0.44658200000000009 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootExtraFinger3" -p "pasted__RightFootExtraFinger2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.2383007371247059 0.089641047827117126 0.085786682015788984 ;
	setAttr ".jo" -type "double3" 109.79559346994861 -40.893075454098799 -29.644735163965198 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.60955732441881261 0.73578239190517403 0.29506633154204298 0
		 0.66227052532794373 -0.67721803856830387 0.32058303061695026 0 0.43570359136599651 -4.4968539234899102e-015 -0.90009020685194274 0
		 -1.1217099999999989 0.63040399999999941 0.51672300000000049 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootExtraFinger4" -p "pasted__RightFootExtraFinger3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -0.21818645759999722 0.12136157288354255 0.041594701191343675 ;
	setAttr ".jo" -type "double3" 1.7667977371887416e-015 -25.830072940977747 47.373368603371915 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 -2.2204460492503131e-016 6.6613381477509392e-016 0
		 5.5511151231257821e-017 -1.0000000000000002 5.1625370645069779e-015 0 8.8817841970012513e-016 -5.1177895205120149e-015 -0.99999999999999989 0
		 -1.1562099999999986 0.38767799999999975 0.45381100000000035 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightFootIndex1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -1.7472499999999911 0.92966799999999816 0.69789299999999521 ;
	setAttr ".jo" -type "double3" -104.60635346744749 56.867569343426112 77.689458796019736 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.11653555316664392 0.53400827044980259 -0.83740947686263645 1.3877787807814457e-017
		 0.073604348041279716 -0.84547925290406156 -0.52891136578656361 0 -0.99045538253752852 -8.8817841970012523e-016 -0.13783372302320462 1.1102230246251565e-016
		 -1.7472499999999984 0.92966800000000038 0.69789299999999999 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootIndex2" -p "RightFootIndex1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -0.86078046517309148 -0.033661248748925177 0.016124762759808675 ;
	setAttr ".jo" -type "double3" -0.093011989514224236 -5.1066553505971894 33.321525999610941 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.049103369487175121 -0.018162617320124613 -0.99862854877931895 0
		 -0.00089199284684541907 -0.99983504606114004 0.018140700556441108 0 -0.99879330366886487 -1.2545520178264269e-014 -0.049111470617696718 0
		 -1.8660099999999984 0.49846399999999913 1.4342999999999992 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootIndex3" -p "pasted__RightFootIndex2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.40933372062587026 0.12121456654414797 0.086156176888812608 ;
	setAttr ".jo" -type "double3" -7.2189581042211053 11.866836728182667 -32.67228948568269 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.24631133591109136 0.51324686911498096 -0.82213647111982724 0
		 0.14729955663527267 -0.85824102170874472 -0.49165555958555252 0 -0.95793192159816087 -5.6621374255882984e-015 -0.28699552885585911 0
		 -1.9722699999999991 0.38470399999999982 1.8410399999999996 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootIndex4" -p "pasted__RightFootIndex3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -0.46710829323761249 0.12693512451927824 0.1422266204610092 ;
	setAttr ".jo" -type "double3" -5.5411223550122668e-015 73.321832071037548 30.880345112407465 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999967 2.6367796834847468e-016 1.4432899320127035e-015 0
		 3.3540215484971967e-016 -1 1.8302748454110067e-014 0 1.3877787807814453e-015 -1.8390363327370664e-014 -1.0000000000000002 0
		 -2.2048699999999983 0.036021199999999365 2.1218399999999993 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightFootMiddle1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -2.1000599999999912 0.8896449999999978 0.73893699999999596 ;
	setAttr ".jo" -type "double3" -122.14694324548626 65.011125346209283 60.33361401307446 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.20908737127140625 0.36706940040931868 -0.90638983139593754 0
		 0.082509253421946344 -0.93019355796691194 -0.35767606547910069 0 -0.97440992106739421 1.8873791418627661e-015 -0.22477834799071278 0
		 -2.1000599999999983 0.88964499999999958 0.73893699999999995 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootMiddle2" -p "RightFootMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -0.78939368996942061 0.07558183018348319 0.081910033058090859 ;
	setAttr ".jo" -type "double3" -1.4963468257178165 2.795752782965284 -6.6365346651339046 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.24544240188536537 0.47155082184596686 -0.84699341778619264 0
		 0.13124683890295472 -0.88183888688149425 -0.4529177020845937 0 -0.96048544738310526 -4.3298697960381105e-015 -0.27833020922148455 0
		 -2.3386899999999993 0.52957699999999897 1.4089900000000002 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootMiddle3" -p "pasted__RightFootMiddle2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.51267289071368372 -0.054359502248427338 0.008374745821699614 ;
	setAttr ".jo" -type "double3" 3.7095119313114746 -5.7128490378624717 -4.9418020668291804 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.13645605484099538 0.54305224394440366 -0.82853726859096644 6.9388939039072284e-018
		 0.088249211535059269 -0.83969891053099976 -0.53583375809712896 6.9388939039072284e-018
		 -0.9867075664859728 -5.9674487573602164e-015 -0.16250593293578031 -5.5511151231257827e-017
		 -2.479699999999998 0.33576199999999884 1.86551 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootMiddle4" -p "pasted__RightFootMiddle3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -0.44400287868501054 0.040635327716161296 -0.021912110808049778 ;
	setAttr ".jo" -type "double3" 0 80.647620431029921 32.89166103722507 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999922 2.9143354396410359e-016 7.7715611723760958e-016 5.5511151231257827e-017
		 3.3306690738754691e-016 -0.99999999999999978 3.3861802251067274e-014 2.4651903288156619e-032
		 6.3837823915946491e-016 -3.3762414519345113e-014 -0.99999999999999989 4.9303806576313238e-032
		 -2.5150799999999975 0.06052379999999908 2.2151699999999992 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightFootRing1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -2.3456799999999922 0.86941899999999761 0.6181169999999957 ;
	setAttr ".jo" -type "double3" -134.55634787031573 59.241109196980659 49.764732170114307 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.33034450859977399 0.39042221552297501 -0.85932706187115149 2.7755575615628914e-017
		 0.14009211720181394 -0.92063591806214651 -0.36442242668609404 6.9388939039072284e-018
		 -0.93340596973443823 1.1046719095020308e-014 -0.35882209472677762 -5.5511151231257827e-017
		 -2.3456799999999993 0.86941899999999961 0.61811699999999958 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootRing2" -p "RightFootRing1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -0.83773778936157162 -0.0055477346143653072 0.23072568071464339 ;
	setAttr ".jo" -type "double3" -0.65550340209241487 3.1901224817405667 11.3629764470758 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.40286962737091786 0.20107011584457515 -0.89289801873241204 -5.5511151231257827e-017
		 0.082693912682583845 -0.97957685176521458 -0.18327822645092362 6.9388939039072284e-018
		 -0.91151400436156893 -2.400857290751901e-014 -0.41126903585455737 5.5511151231257827e-017
		 -2.8385599999999989 0.54745499999999914 1.2572400000000001 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootRing3" -p "pasted__RightFootRing2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.48838484164682638 0.035296264148170997 -0.035113704045379723 ;
	setAttr ".jo" -type "double3" 8.1388928153649012 -12.378619140197525 -22.108986534768174 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.13876740269654281 0.54206656720186519 -0.82879879625325281 -5.5511151231257827e-017
		 0.089513254095236958 -0.84033555007626881 -0.53462467266232261 -2.7755575615628914e-017
		 -0.98627125340351285 -3.9135361618036768e-015 -0.16513332404412784 0 -3.0003899999999994 0.41467999999999922 1.7012899999999995 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootRing4" -p "pasted__RightFootRing3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -0.47184800917826486 0.1359793351754941 -0.12584283430306753 ;
	setAttr ".jo" -type "double3" -1.9260526001484824e-014 80.49502038166986 32.82443014148285 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999978 1.9255430583342559e-016 1.6653345369377348e-015 5.5511151231257827e-017
		 1.52655665885959e-016 -1 2.3592239273284576e-014 6.1629758220391547e-033 1.6930901125533633e-015 -2.3433384596379577e-014 -1.0000000000000002 9.8607613152626476e-032
		 -2.9295799999999979 0.044638699999999192 2.0404399999999998 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightFootPinky1" -p "unused_joints";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -2.5181699999999916 0.8241109999999976 0.29628099999999602 ;
	setAttr ".jo" -type "double3" -143.80443191338463 45.329558543532016 45.818256959879974 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.48996590256417477 0.50416431798072781 -0.71116225630969854 0
		 0.28603648588364378 -0.86360774688224451 -0.41516838543934015 0 -0.82347831973149666 -1.1990408665951691e-014 -0.56734773898570401 0
		 -2.5181699999999987 0.82411099999999959 0.29628099999999974 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootPinky2" -p "RightFootPinky1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -1.0110002492678649 -0.0838554904259734 0.16107117503059243 ;
	setAttr ".jo" -type "double3" 0.52380098361664718 -4.2829090529063034 23.296604061045755 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.50007275967999065 0.12117124079615035 -0.8574641481892753 0
		 0.061044233972053288 -0.99263161868032446 -0.10467125247575786 0 -0.86382917091564027 -2.2204460492503131e-016 -0.50378483847293054 0
		 -3.1701499999999974 0.3868189999999993 0.95869700000000091 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootPinky3" -p "pasted__RightFootPinky2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -0.29689467992402596 0.01764793999925085 0.016448116749129049 ;
	setAttr ".jo" -type "double3" 7.1821047509276585 -22.44625910993031 -11.304886890187756 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.11233462294205576 0.28966141303219123 -0.9505141757431399 0
		 0.033996461834782638 -0.95712917926484364 -0.28765947712968182 0 -0.99308870352611567 4.3021142204224816e-016 -0.11736620863271385 0
		 -3.3317499999999973 0.33332599999999929 1.2031400000000003 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "pasted__RightFootPinky4" -p "pasted__RightFootPinky3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -0.39320442664705491 0.21026425118653069 -0.112026478622548 ;
	setAttr ".jo" -type "double3" 0 83.259876758345513 16.837686404107867 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 5.8980598183211441e-016 9.9920072216264089e-016 0
		 6.4531713306337234e-016 -0.99999999999999978 -9.3258734068513165e-015 0 1.02695629777827e-015 9.4372638280490089e-015 -1.0000000000000002 0
		 -3.2575199999999991 0.018179799999999524 1.5295500000000006 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode transform -n "reference_joints" -p "BodyRig";
createNode joint -n "RightAnkleFloor_if" -p "reference_joints";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -1.9843 0.062255499999999998 -0.373153 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -180 62.556999999999974 0 ;
	setAttr ".bps" -type "matrix" 0.46086595309007816 1.6653345369377348e-016 0.88746975908048464 0
		 -2.0649643628384233e-016 0.99999999999999978 -2.133258655895791e-016 0 -0.88746975908048475 0 0.4608659530900785 0
		 1.8599545470024954 1.0800460304403499 -0.078531422444566054 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftAnkleFloor_if" -p "reference_joints";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.9842972532454757 0.062255479174176731 -0.37315266105723865 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 -62.556999999999974 0 ;
	setAttr ".bps" -type "matrix" 0.46086595309007816 1.6653345369377348e-016 0.88746975908048464 0
		 -2.0649643628384233e-016 0.99999999999999978 -2.133258655895791e-016 0 -0.88746975908048475 0 0.4608659530900785 0
		 1.8599545470024954 1.0800460304403499 -0.078531422444566054 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode transform -n "sh" -p "BodyRig";
createNode joint -n "Reference" -p "sh";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	setAttr ".ove" yes;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 1.0434603204601249;
createNode joint -n "Hips" -p "Reference";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0 9.7720558958491708 0.63025663379520191 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -89.999999999999986 0 89.999999999999986 ;
	setAttr ".bps" -type "matrix" 0.00054970830853706687 0.98899965509713406 0.14791680106912963 0
		 -0.99999984553068277 0.00055582246241525624 1.389811659854856e-017 0 -8.2215480602818012e-005 -0.14791677822052246 0.98899980786725905 0
		 -1.9368772736496027e-018 9.772055895849169 0.63025663379520203 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "Spine" -p "Hips";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.84748149751601254 -0.1267510574263373 -0.00047104932556305457 ;
	setAttr ".r" -type "double3" 0 0 2.3969374552514943e-005 ;
	setAttr ".ra" -type "double3" 89.999999999999986 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0.00042651621269771273 -0.028912693934234786 -0.72645300603391638 ;
	setAttr ".bps" -type "matrix" -0.00058709076930562427 0.99992050299303969 0.012595357024498148 0
		 -0.99999982763485484 -0.00058713734376016969 -1.0354106691500865e-012 0 7.3952034317553986e-006 -0.012595354853498216 0.99992067534451212 0
		 0.00047104932556345713 10.61953739336518 0.75700769122153866 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "Spine1" -p "Spine";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.80234496979306869 -8.6736173798840355e-019 -1.1102230246251565e-016 ;
	setAttr ".ra" -type "double3" 89.999999999999986 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -90.002128471275441 3.1184293114931894 -0.055830935664109703 ;
	setAttr ".bps" -type "matrix" -5.6975275389585824e-014 0.99910980101698488 -0.042185370826872792 1.3877787807814457e-017
		 -0.99999999996221356 -3.6672702807377151e-007 -8.6854875000738622e-006 -6.6174449004242214e-024
		 -8.693226203593164e-006 0.042185370825278838 0.99910980097923252 4.3368086899420177e-019
		 -8.5489619791018631e-016 11.421818579134603 0.76711351257289262 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "Spine2" -p "Spine1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.98495099161027078 -2.3445871979999033e-017 -1.9984014443252818e-015 ;
	setAttr ".r" -type "double3" 8.0254805218288152e-016 3.1805542217135854e-015 -8.459136087580813e-017 ;
	setAttr ".ra" -type "double3" 89.999999999999986 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -89.999995553844442 7.6272699868986047 6.6700047811148902e-005 ;
	setAttr ".bps" -type "matrix" 2.4211511572771804e-016 0.98467097145377436 -0.17442212582204403 0
		 -0.99999999996221356 -1.5162909951725877e-006 -8.559967494735296e-006 0 -8.693226207374934e-006 0.1744221258154533 0.98467097141656679 0
		 -5.6949382527063351e-014 12.405892768373823 0.72556298974551448 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "Neck_nouse" -p "Spine2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 3.1668507108553019 2.3716922523120409e-020 -2.6645352591003757e-015 ;
	setAttr ".ra" -type "double3" 89.999999999999986 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.999999999999986 0.00049808517204066188 0 ;
	setAttr ".bps" -type "matrix" 7.5572424007592103e-011 0.98466945512557147 -0.1744306857829476 0
		 -0.99999999996221367 -1.516290995172587e-006 -8.5599674947352977e-006 0 -8.6932262070464529e-006 0.17443068577635715 0.98466945508836468 0
		 -5.6182645409946151e-014 15.524198734280782 0.17319415659707946 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "Neck1_nouse" -p "Neck_nouse";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 0.54668403100698093 0 0.28451372658305729 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 0.0058876317208462602 -84.363638455129447 -0.005819645064656453 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 1.3246485728225753e-006 0.27029615856332312 0.96277722587530901 0
		 -0.99999999999878342 -4.3507697507471729e-007 1.498008229810161e-006 0 8.2378807305504178e-007 -0.96277722587612247 0.27029615856241768 0
		 -1.0706670075861394e-006 16.112129725661081 0.35798766229365059 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "Head_nouse" -p "Neck1_nouse";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 1.0905763435915947 1.6940658945086007e-021 3.5527136788005009e-015 ;
	setAttr ".jo" -type "double3" -74.318387024049514 -4.7201484295151424e-005 -89.999924103768066 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.99999999999999978 -3.4552864394134345e-011 -1.000784462809859e-013 0
		 3.4552913706701777e-011 0.99999999998824685 -4.8483453826131395e-006 1.3877787807814457e-017
		 1.0017035740257638e-013 4.8483453827796721e-006 0.99999999998824662 0 3.739633895065328e-007 16.406908321953917 1.4079697289820052 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftShoulder" -p "Spine2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.9727120750421339 -0.87089120255857855 0.027196428109692139 ;
	setAttr ".r" -type "double3" -1.1927080055488188e-015 1.5902773407317584e-015 -2.981770013872047e-016 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" 10.488999100634887 16.73786007391244 -85.093821442029352 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 0 0 0.36000001459070508 ;
	setAttr ".bps" -type "matrix" 0.95412621725191371 0.030414472541004909 -0.29785587355733867 0
		 -0.031860597939045304 0.99949232228115015 -3.4694469519536142e-018 0 0.29770465876690499 0.0094898662311937113 0.95461085191160167 0
		 0.87089096610091243 14.353110063034116 0.40826534406806664 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftArm" -p "LeftShoulder";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" 1.4862818338201933 0 -1.1102230246251565e-016 ;
	setAttr ".r" -type "double3" -8.1501713712502619e-015 4.7708320221952759e-015 1.1976776222386055e-014 ;
	setAttr ".ra" -type "double3" -17.851759151399964 0 0 ;
	setAttr ".jo" -type "double3" 16.012083246489848 3.4959940120221749 -37.416248246451183 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -8.1501713712502619e-015 4.7708320221952759e-015 1.1976776222386055e-014 ;
	setAttr ".bps" -type "matrix" 0.75756606474017218 -0.5826296734419274 -0.29434048511722388 0
		 0.54307656777599389 0.81273775820034988 -0.21100990007133585 0 0.36216225519335199 4.5192032752990746e-006 0.93211506848287839 0
		 2.2889914299740117 14.398314541057029 -0.034432429896850712 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftForeArm" -p "LeftArm";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" 2.6610024174612885 -0.17150035625679116 0.030292099402773331 ;
	setAttr ".r" -type "double3" 3.1805546814635176e-015 3.9756933518293994e-016 -9.5416640443905519e-015 ;
	setAttr ".ra" -type "double3" 11.715942216633904 0 0 ;
	setAttr ".jo" -type "double3" 36.130360954961475 -39.744551375519073 -33.913672135703159 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 3.1805546814635176e-015 3.9756933518293994e-016 -9.5416640443905519e-015 ;
	setAttr ".bps" -type "matrix" 0.48197228097529576 -0.72043865768994075 0.4986690895547734 0
		 0.63820556260235817 0.67861056720787161 0.36356754246937184 0 -0.60033022598806296 0.14302390911916382 0.78685944182261358 0
		 4.2227093898201966 12.708550893364837 -0.75324917700525995 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHand" -p "LeftForeArm";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" 3.053518789979786 0.044987900419901194 -0.12060074885500915 ;
	setAttr ".r" -type "double3" -4.9099812895093038e-014 1.1927080055488201e-014 2.6736537791052683e-014 ;
	setAttr ".ra" -type "double3" -0.75162733974313678 0 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 13.885775242231968 9.8854764142517109 -33.536120039672021 ;
	setAttr ".pa" -type "double3" -4.9099812895093038e-014 1.1927080055488201e-014 2.6736537791052683e-014 ;
	setAttr ".bps" -type "matrix" 0.15149186404410631 -0.98549180336312081 0.076525294070303396 0
		 0.64488760254422139 0.15721191094945719 0.74793341624798815 0 -0.74911293889053077 -0.063955613981294929 0.65934777183749338 0
		 5.7955326091399177 10.521958389158288 0.69090656040143217 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandThumb1" -p "LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0.50042345238350272 -0.20002559413924459 0.41764808697941724 ;
	setAttr ".r" -type "double3" 8.7465253740246703e-015 4.7708320221952759e-015 -1.2722218725854067e-014 ;
	setAttr ".jo" -type "double3" 126.16147526340119 -31.744927743412706 -28.112004304917164 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 8.7465253740246703e-015 4.7708320221952759e-015 -1.2722218725854067e-014 ;
	setAttr ".bps" -type "matrix" -0.5389166515129028 -0.83583858558727686 0.10460736860078497 1.3877787807814457e-017
		 -0.81975736636413443 0.54897091428255029 0.16318331888866222 -6.9388939039072284e-018
		 -0.19382131723280172 0.0021895468117783591 -0.98103440452967816 -2.7105054312137611e-020
		 5.4294830790417796 9.9706378328993548 0.85497112185522783 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandThumb2" -p "LeftHandThumb1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.59513633102094765 4.4408920985006262e-016 -6.6613381477509392e-016 ;
	setAttr ".r" -type "double3" 2.1866313435061672e-015 2.385416011097638e-015 -2.6040791454482544e-014 ;
	setAttr ".jo" -type "double3" -17.98262811439858 -8.8232595929443498 -18.697525744130285 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 2.1866313435061672e-015 2.385416011097638e-015 -2.6040791454482544e-014 ;
	setAttr ".bps" -type "matrix" -0.27448215517413066 -0.95592366722115374 -0.10425684120203213 1.3877787807814457e-017
		 -0.85548357646762585 0.19324537581148057 0.48042072719819123 -3.4694469519536142e-018
		 -0.4390983908933439 0.22105693197441451 -0.87081940489457121 -3.4694469519536142e-018
		 5.1087542003342961 9.4731999237472024 0.91722676740205522 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandThumb3" -p "LeftHandThumb2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.8044430910038276 8.8817841970012523e-016 3.3306690738754696e-016 ;
	setAttr ".r" -type "double3" 2.5444437451708128e-014 -3.1805546814635093e-015 -3.0165573307005537e-014 ;
	setAttr ".jo" -type "double3" 15.279034543448264 8.421620934330166 -39.337096594241103 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 2.5444437451708128e-014 -3.1805546814635093e-015 -3.0165573307005537e-014 ;
	setAttr ".bps" -type "matrix" 0.39073329902289305 -0.88491686508985568 -0.25347510906246629 0
		 -0.90783718121733825 -0.41598300859096304 0.052818452864212204 0 -0.15218127819822219 0.20947620018310797 -0.96589884569907303 0
		 4.8879489270006289 8.7042137341241066 0.83335807180719779 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandThumb4" -p "LeftHandThumb3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.5419704708249693 1.7763568394002505e-015 -6.6613381477509392e-016 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 48.410465452040597 3.5188744130494469 -163.74134944513295 ;
	setAttr ".bps" -type "matrix" 0.390733299022893 -0.88491686508985568 -0.25347510906246634 0
		 -0.90783718121733803 -0.4159830085909631 0.052818452864212113 0 -0.15218127819822208 0.20947620018310803 -0.96589884569907303 0
		 5.0997148370390581 8.2246149241104032 0.69598204760620341 1;
	setAttr ".radi" 0.1;
createNode joint -n "LeftHandIndex1" -p "LeftHand";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 1.5285719203806405 0.27663510744069519 0.19854222790397991 ;
	setAttr ".r" -type "double3" 5.6852414931160356e-014 2.464929878134227e-014 -2.8624992133171641e-014 ;
	setAttr ".ra" -type "double3" -0.47569820809252245 -3.1118873897369803 -3.4215169434507486 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 19.165135875529586 -15.166863258233031 20.072386482576317 ;
	setAttr ".pa" -type "double3" 5.6852414931160356e-014 2.464929878134227e-014 -2.8624992133171641e-014 ;
	setAttr ".bps" -type "matrix" 0.12250206825597154 -0.89226309385519265 0.43458004397000188 0
		 0.24208246983050102 0.45151585946006323 0.85879538101739061 0 -0.96249120571243352 3.625032706620331e-016 0.27131288013329952 0
		 6.0567668180618295 9.0463557345617875 1.1456939926625569 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandIndex2" -p "LeftHandIndex1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.92122645703055817 0.064309609326505424 -0.047923312190309986 ;
	setAttr ".r" -type "double3" -1.2125864723079654e-014 3.0115877140107666e-014 6.5474699887940319e-015 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.3535957649883552 4.237050989792964 -42.020374967325836 ;
	setAttr ".pa" -type "double3" -1.2125864723079654e-014 3.0115877140107666e-014 6.5474699887940319e-015 ;
	setAttr ".bps" -type "matrix" -0.0454179439377983 -0.9678506021743728 -0.2473912331493722 0
		 0.29942477788853616 -0.24944993433210666 0.92093405445129872 0 -0.95303830602702566 -0.032248133781843547 0.30112795471813097 0
		 6.2007285569068502 8.257431294178744 1.60608925757209 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandIndex3" -p "LeftHandIndex2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.55788963908835321 0.016438715678056326 0.003074696356238249 ;
	setAttr ".r" -type "double3" 1.2722218725854062e-014 -1.7493050748049344e-014 2.4102640945465712e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.1495297935426576 -8.6149518848457252 -71.700455790742495 ;
	setAttr ".pa" -type "double3" 1.2722218725854062e-014 -1.7493050748049344e-014 2.4102640945465712e-014 ;
	setAttr ".bps" -type "matrix" -0.43793326154208267 -0.071129719930330876 -0.89618916606804944 0
		 0.11570793606121899 -0.99303350211042174 0.022274137890484186 0 -0.89153021932381316 -0.093941612871741076 0.44311267348552458 0
		 6.1773822119390331 7.7132776812744073 1.4841371019012628 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandIndex4" -p "LeftHandIndex3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.45150763947338213 0.0048670071651102376 0.03964329557591828 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.43793326154208251 -0.071129719930330973 -0.89618916606804955 4.6837533851373792e-017
		 0.1157079360612191 -0.9930335021104213 0.022274137890484186 0 -0.89153021932381304 -0.093941612871741229 0.44311267348552452 -2.0816681711721685e-017
		 5.9448719541276427 7.672604813036342 1.0971757020853907 0.99999999999999978;
	setAttr ".radi" 0.1;
createNode joint -n "LeftHandMiddle1" -p "LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 1.6135681496494172 0.28989685468627613 -0.23583309727338619 ;
	setAttr ".r" -type "double3" -2.2661452105427557e-014 5.3671860249696843e-015 -1.0614065301092491e-030 ;
	setAttr ".jo" -type "double3" -11.31846361390239 20.526170411467611 13.326514962974125 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -2.2661452105427557e-014 5.3671860249696843e-015 -1.0614065301092491e-030 ;
	setAttr ".bps" -type "matrix" 0.53992836080158257 -0.84171097486139279 -1.8041124150158794e-016 1.3877787807814457e-017
		 0.69839274500670101 0.44799469327257102 0.55816514448827759 -6.9388939039072284e-018
		 -0.46981372790087794 -0.30136919152013442 0.82972987862218117 6.9388939039072284e-018
		 6.4035915680823727 8.9924582925476866 0.87571285522814035 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandMiddle2" -p "LeftHandMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.72689528935090308 0.0083106350854809108 0.012354017997793676 ;
	setAttr ".jo" -type "double3" -0.66564937925979628 -7.1110830674996555 -17.685975833462255 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -4.2539918864574541e-014 4.4726550208081163e-016 1.2250105140324327e-014 ;
	setAttr ".bps" -type "matrix" 0.24175283177392393 -0.96812118404258196 -0.065551059009586632 1.3877787807814457e-017
		 0.8352087651174338 0.17322256375028813 0.52193894478069769 -3.4694469519536142e-018
		 -0.49394522672083774 -0.18092903696136434 0.8504603439220042 3.4694469519536142e-018
		 6.7960629501360001 8.3806225499259828 0.89060205991522567 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandMiddle3" -p "LeftHandMiddle2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.72472802680258042 0 0 ;
	setAttr ".jo" -type "double3" 0.92703677854686983 -2.5082830192738368 -58.455059956625377 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -4.3732626870123391e-015 -2.2065098102653147e-014 
		1.9365975038012723e-014 ;
	setAttr ".bps" -type "matrix" -0.6063690289976883 -0.66140614402948028 -0.44142781211932608 0
		 0.63532916936513706 -0.73680282165560795 0.23125407791894115 0 -0.4781981254942409 -0.14022665452897723 0.86698502762931584 0
		 6.9712680028814473 7.6789979945090279 0.84309537026438564 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandMiddle4" -p "LeftHandMiddle3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.53274819755162817 -4.4408920985006262e-016 2.6645352591003757e-015 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.60636902899768841 -0.66140614402948028 -0.44142781211932608 0
		 0.63532916936513717 -0.73680282165560784 0.23125407791894126 0 -0.47819812549424101 -0.14022665452897734 0.86698502762931584 0
		 6.6482259956318028 7.3266350634277515 0.60792549900865889 1;
	setAttr ".radi" 0.1;
createNode joint -n "LeftHandRing1" -p "LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 1.4975969637092446 0.0283538028869188 -0.5867442278884285 ;
	setAttr ".r" -type "double3" 8.2992598719438676e-015 -1.4461584567279426e-014 -2.0673605429512861e-014 ;
	setAttr ".jo" -type "double3" -35.141917312315954 34.239566226360793 -9.9057541279201633 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 8.2992598719438676e-015 -1.4461584567279426e-014 -2.0673605429512861e-014 ;
	setAttr ".bps" -type "matrix" 0.45314960546110972 -0.78892579625916293 -0.41503195427254314 0
		 0.88485313427807477 0.34160989928957924 0.31676112050823241 0 -0.10812199511990123 -0.51078250234733902 0.85288385461742822 0
		 6.4802290736563375 9.0880719995604515 0.4398488658081679 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandRing2" -p "LeftHandRing1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.69198598520212329 0 0 ;
	setAttr ".jo" -type "double3" -3.0743775263028454 0.068288059887899849 -32.321822832593192 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 1.0088321880267094e-014 -6.6592863643142385e-015 -1.7083057371141995e-016 ;
	setAttr ".bps" -type "matrix" -0.090041448750515674 -0.8487288890462974 -0.52110633310788523 1.3877787807814457e-017
		 0.99441954309311131 -0.10549773606333034 7.8496237287950521e-017 1.7347234759768071e-018
		 -0.054975538391145662 -0.51819832167207003 0.85349176305038466 6.9388939039072284e-018
		 6.7938022498352941 8.5421464051846829 0.15265257004051852 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandRing3" -p "LeftHandRing2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.53371088191440919 0 0 ;
	setAttr ".jo" -type "double3" -2.3859824370944756 3.3606119871537379 -68.081160209302212 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -1.3517357396219947e-014 2.3605679276487015e-015 -1.9461484858769561e-014 ;
	setAttr ".bps" -type "matrix" -0.95128142137711147 -0.18819937902882214 -0.24422254415984448 0
		 0.2920458022515543 -0.80397162104815756 -0.5180143646043458 0 -0.09885801297814778 -0.56410160989166125 0.81976610504926872 0
		 6.7457461488138089 8.0891705613055489 -0.12546755057367676 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandRing4" -p "LeftHandRing3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.44879684935861075 -8.8817841970012523e-016 -8.8817841970012523e-016 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.95128142137711169 -0.18819937902882228 -0.24422254415984454 3.4694469519536142e-018
		 0.29204580225155452 -0.80397162104815756 -0.51801436460434591 1.3877787807814457e-017
		 -0.098858012978147669 -0.56410160989166114 0.81976610504926872 1.3877787807814457e-017
		 6.3188140440463805 8.004707272946165 -0.23507385893495941 0.99999999999999989;
	setAttr ".radi" 0.1;
createNode joint -n "LeftHandPinky1" -p "LeftHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" 0.9821452583569581 -0.11965544577864051 -0.70787765843010408 ;
	setAttr ".r" -type "double3" -1.5902773407317566e-015 -9.5416640443905503e-015 -2.2263882770244617e-014 ;
	setAttr ".jo" -type "double3" -73.613871135055632 39.126245692302618 -58.605094014785863 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -1.5902773407317566e-015 -9.5416640443905503e-015 
		-2.2263882770244617e-014 ;
	setAttr ".bps" -type "matrix" 0.10689983178532525 -0.46200046500587821 -0.88041353709414416 0
		 0.97425965380468205 0.22542876251352972 -1.9775847626135601e-016 0 0.19847053416729299 -0.85775138785429617 0.47420670988649966 0
		 6.3974356246124726 9.5805237763177207 0.20983365196362708 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandPinky2" -p "LeftHandPinky1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" 0.40654334007020099 0 0 ;
	setAttr ".jo" -type "double3" -1.960215150105387 15.893695689276083 -25.076153035108042 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" 2.7034714792439897e-014 -9.6410563781862743e-015 -4.5049575292916842e-014 ;
	setAttr ".bps" -type "matrix" -0.35835732603131959 -0.25944904309812777 -0.89680890992181184 0
		 0.92362637390233471 0.041402938165584158 -0.38105133268797453 0 0.13599392748099914 -0.96486889821712196 0.22479693267829537 0
		 6.4408950392794209 9.3927005641602435 -0.14809260804964622 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandPinky3" -p "LeftHandPinky2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 0.26513842955238154 0 0 ;
	setAttr ".jo" -type "double3" -6.1955946603537386 -5.5226735794296831 -63.444395262757453 ;
	setAttr ".ssc" no;
	setAttr ".pa" -type "double3" -8.4483483726374669e-015 -7.9513867036588254e-016 
		-4.44283732066935e-014 ;
	setAttr ".bps" -type "matrix" -0.96872739365183591 -0.24517417407889999 -0.038168850562340151 3.4694469519536142e-018
		 0.066977712358717578 -0.11026145227693963 -0.99164328172431704 1.7347234759768071e-018
		 0.23891676968290476 -0.96318847403117858 0.1232344945937488 1.3877787807814457e-017
		 6.3458807406368845 9.3239106523243365 -0.38587111403489766 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftHandPinky4" -p "LeftHandPinky3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 0.32697540657311741 -4.7184478546569153e-016 -5.3290705182007514e-015 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.96872739365183569 -0.24517417407890016 -0.038168850562340144 0
		 0.066977712358717537 -0.11026145227693955 -0.99164328172431715 0 0.23891676968290476 -0.96318847403117791 0.12323449459374877 0
		 6.029130707239057 9.2437447270736612 -0.39835138946594761 1;
	setAttr ".radi" 0.1;
createNode joint -n "RightShoulder" -p "Spine2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.972702226277633 0.87089076349472416 0.027209475804685468 ;
	setAttr ".r" -type "double3" 4.7708320221952767e-015 -7.9513867036587903e-015 -1.9083328088781101e-014 ;
	setAttr ".jot" -type "string" "xzy";
	setAttr ".jo" -type "double3" -169.51108986501799 -16.736867553438387 -94.906152937190342 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.95412621725191371 0.030414472541004909 -0.29785587355733867 0
		 -0.031860597939045304 0.99949232228115015 -3.4694469519536142e-018 0 0.29770465876690499 0.0094898662311937113 0.95461085191160167 0
		 0.87089096610091243 14.353110063034116 0.40826534406806664 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightArm" -p "RightShoulder";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 5;
	setAttr ".t" -type "double3" -1.4862801895161382 4.4291096479298631e-006 1.2130671112053903e-007 ;
	setAttr ".r" -type "double3" -1.3020395727241272e-014 -2.3854160110976368e-015 6.410805529824901e-015 ;
	setAttr ".jo" -type "double3" 16.012083246489762 3.4959940120221336 -37.41624824645119 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.75756606474017218 -0.5826296734419274 -0.29434048511722388 0
		 0.54307656777599389 0.81273775820034988 -0.21100990007133585 0 0.36216225519335199 4.5192032752990746e-006 0.93211506848287839 0
		 2.2889914299740117 14.398314541057029 -0.034432429896850712 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightForeArm" -p "RightArm";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 6;
	setAttr ".t" -type "double3" -2.660966836678504 0.15390636702504423 -0.081392610978598512 ;
	setAttr ".r" -type "double3" -2.1468744099878734e-014 -8.8459177078204053e-015 1.5902773407317598e-015 ;
	setAttr ".jo" -type "double3" 13.902261771656946 -47.739566572993461 -18.406569256598608 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.48197228097529576 -0.72043865768994075 0.4986690895547734 0
		 0.63820556260235817 0.67861056720787161 0.36356754246937184 0 -0.60033022598806296 0.14302390911916382 0.78685944182261358 0
		 4.2227093898201966 12.708550893364837 -0.75324917700525995 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHand" -p "RightForeArm";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 7;
	setAttr ".t" -type "double3" -3.0535227695634539 -0.068532680394000067 0.10895334878540064 ;
	setAttr ".r" -type "double3" 1.1131941385122306e-014 -1.5902773407317562e-015 -1.8685758753598154e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 24.036408529068147 16.177858907687245 -31.238096724036218 ;
	setAttr ".bps" -type "matrix" 0.15149186404410631 -0.98549180336312081 0.076525294070303396 0
		 0.64488760254422139 0.15721191094945719 0.74793341624798815 0 -0.74911293889053077 -0.063955613981294929 0.65934777183749338 0
		 5.7955326091399177 10.521958389158288 0.69090656040143217 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandThumb1" -p "RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -0.5004622097152911 0.19453656780184847 -0.42023868055042257 ;
	setAttr ".r" -type "double3" -2.2263882770244611e-014 -1.590277340731758e-015 3.0897344086351093e-031 ;
	setAttr ".jo" -type "double3" 125.37890297111886 -32.096702056883565 -27.698215186957892 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.5389166515129028 -0.83583858558727686 0.10460736860078497 1.3877787807814457e-017
		 -0.81975736636413443 0.54897091428255029 0.16318331888866222 -6.9388939039072284e-018
		 -0.19382131723280172 0.0021895468117783591 -0.98103440452967816 -2.7105054312137611e-020
		 5.4294830790417796 9.9706378328993548 0.85497112185522783 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandThumb2" -p "RightHandThumb1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.59513871999388002 1.7078600866859972e-007 1.3497837292320014e-007 ;
	setAttr ".r" -type "double3" -7.1562480332929135e-015 2.782985346280578e-015 4.174478019420866e-015 ;
	setAttr ".jo" -type "double3" -17.982628114398555 -8.8232595929443391 -18.697525744130314 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.27448215517413066 -0.95592366722115374 -0.10425684120203213 1.3877787807814457e-017
		 -0.85548357646762585 0.19324537581148057 0.48042072719819123 -3.4694469519536142e-018
		 -0.4390983908933439 0.22105693197441451 -0.87081940489457121 -3.4694469519536142e-018
		 5.1087542003342961 9.4731999237472024 0.91722676740205522 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandThumb3" -p "RightHandThumb2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.8044453177336166 5.3938306052714324e-006 2.892740652349346e-006 ;
	setAttr ".r" -type "double3" -1.5703988739726117e-014 8.746525374024664e-015 -4.7956801056442089e-014 ;
	setAttr ".jo" -type "double3" 15.279034543448205 8.421620934330166 -39.337096594241089 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.39073329902289305 -0.88491686508985568 -0.25347510906246629 0
		 -0.90783718121733825 -0.41598300859096304 0.052818452864212204 0 -0.15218127819822219 0.20947620018310797 -0.96589884569907303 0
		 4.8879489270006289 8.7042137341241066 0.83335807180719779 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandThumb4" -p "RightHandThumb3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.54196920848074814 -5.8616449667425741e-006 -6.2674768258608182e-007 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.390733299022893 -0.88491686508985568 -0.25347510906246634 0
		 -0.90783718121733803 -0.4159830085909631 0.052818452864212113 0 -0.15218127819822208 0.20947620018310803 -0.96589884569907303 0
		 5.0997148370390581 8.2246149241104032 0.69598204760620341 1;
	setAttr ".radi" 0.1;
createNode joint -n "RightHandIndex1" -p "RightHand";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -1.5286092620908072 -0.2792102655204971 -0.19489144611079556 ;
	setAttr ".r" -type "double3" 1.7493050748049341e-014 -9.5416640443905503e-015 -7.9513867036588057e-016 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 18.434573972846913 -14.907728424087665 20.261932000903624 ;
	setAttr ".bps" -type "matrix" 0.12250206825597154 -0.89226309385519265 0.43458004397000188 0
		 0.24208246983050102 0.45151585946006323 0.85879538101739061 0 -0.96249120571243352 3.625032706620331e-016 0.27131288013329952 0
		 6.0567668180618295 9.0463557345617875 1.1456939926625569 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandIndex2" -p "RightHandIndex1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.92467515429726355 -0.0087403134275065852 -0.0016286333298571876 ;
	setAttr ".r" -type "double3" 6.9276456655627224e-014 2.6317226382851937e-014 -1.1610266991514267e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.62347065133152624 1.6055341865021036 -45.36660919836833 ;
	setAttr ".bps" -type "matrix" -0.0454179439377983 -0.9678506021743728 -0.2473912331493722 0
		 0.29942477788853616 -0.24944993433210666 0.92093405445129872 0 -0.95303830602702566 -0.032248133781843547 0.30112795471813097 0
		 6.2007285569068502 8.257431294178744 1.60608925757209 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandIndex3" -p "RightHandIndex2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.55788577504670123 -0.016438705262781239 -0.0030787123652462611 ;
	setAttr ".r" -type "double3" -2.7829853462805862e-015 2.7034714792439894e-014 -3.7272125173400586e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.1495297935390711 -8.614951884834344 -71.70045579074305 ;
	setAttr ".bps" -type "matrix" -0.43793326154208267 -0.071129719930330876 -0.89618916606804944 0
		 0.11570793606121899 -0.99303350211042174 0.022274137890484186 0 -0.89153021932381316 -0.093941612871741076 0.44311267348552458 0
		 6.1773822119390331 7.7132776812744073 1.4841371019012628 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandIndex4" -p "RightHandIndex3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.45150677934960814 -0.0048741502541549409 -0.039644355974644441 ;
	setAttr ".jo" -type "double3" 1.9090959104164228e-006 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.43793326154208251 -0.071129719930330973 -0.89618916606804955 4.6837533851373792e-017
		 0.1157079360612191 -0.9930335021104213 0.022274137890484186 0 -0.89153021932381304 -0.093941612871741229 0.44311267348552452 -2.0816681711721685e-017
		 5.9448719541276427 7.672604813036342 1.0971757020853907 0.99999999999999978;
	setAttr ".radi" 0.1;
createNode joint -n "RightHandMiddle1" -p "RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -1.6136076092626421 -0.28677245186518086 0.23961401673719429 ;
	setAttr ".r" -type "double3" -1.4312496066585827e-014 3.1805546814635156e-015 -1.1927080055488189e-014 ;
	setAttr ".jo" -type "double3" -12.100315002307267 20.697666133812238 13.051270801243758 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.53992836080158257 -0.84171097486139279 -1.8041124150158794e-016 1.3877787807814457e-017
		 0.69839274500670101 0.44799469327257102 0.55816514448827759 -6.9388939039072284e-018
		 -0.46981372790087794 -0.30136919152013442 0.82972987862218117 6.9388939039072284e-018
		 6.4035915680823727 8.9924582925476866 0.87571285522814035 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandMiddle2" -p "RightHandMiddle1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.7268981266229888 -0.0083076483371744558 -0.012355780513228609 ;
	setAttr ".r" -type "double3" 1.5703988739726117e-014 1.4113711398994352e-014 2.148116814160321e-014 ;
	setAttr ".jo" -type "double3" -0.66564937926039858 -7.111083067499635 -17.685975833462251 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.24175283177392393 -0.96812118404258196 -0.065551059009586632 1.3877787807814457e-017
		 0.8352087651174338 0.17322256375028813 0.52193894478069769 -3.4694469519536142e-018
		 -0.49394522672083774 -0.18092903696136434 0.8504603439220042 3.4694469519536142e-018
		 6.7960629501360001 8.3806225499259828 0.89060205991522567 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandMiddle3" -p "RightHandMiddle2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.72472483296343349 -4.7591080569731048e-006 3.5318196269784607e-006 ;
	setAttr ".r" -type "double3" 1.05355873823479e-014 2.5096564283423062e-014 5.9309269182173709e-015 ;
	setAttr ".jo" -type "double3" 0.92703677854322786 -2.5082830192733332 -58.455059956625448 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.6063690289976883 -0.66140614402948028 -0.44142781211932608 0
		 0.63532916936513706 -0.73680282165560795 0.23125407791894115 0 -0.4781981254942409 -0.14022665452897723 0.86698502762931584 0
		 6.9712680028814473 7.6789979945090279 0.84309537026438564 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandMiddle4" -p "RightHandMiddle3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.5327450986137432 9.141373413790177e-007 1.482498095395357e-006 ;
	setAttr ".jo" -type "double3" 1.9090959104164224e-006 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.60636902899768841 -0.66140614402948028 -0.44142781211932608 0
		 0.63532916936513717 -0.73680282165560784 0.23125407791894126 0 -0.47819812549424101 -0.14022665452897734 0.86698502762931584 0
		 6.6482259956318028 7.3266350634277515 0.60792549900865889 1;
	setAttr ".radi" 0.1;
createNode joint -n "RightHandRing1" -p "RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -1.4976404536287724 -0.020649650121267626 0.58706568445827401 ;
	setAttr ".r" -type "double3" -1.4511280734177294e-014 1.7493050748049337e-014 7.9513867036587872e-015 ;
	setAttr ".jo" -type "double3" -36.036166591621246 34.107017795957098 -10.408059278037404 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.45314960546110972 -0.78892579625916293 -0.41503195427254314 0
		 0.88485313427807477 0.34160989928957924 0.31676112050823241 0 -0.10812199511990123 -0.51078250234733902 0.85288385461742822 0
		 6.4802290736563375 9.0880719995604515 0.4398488658081679 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandRing2" -p "RightHandRing1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.69198000961750195 8.0567007820775416e-007 2.2618389925455062e-006 ;
	setAttr ".r" -type "double3" -1.6747608244581331e-014 -5.7647553601526259e-015 -1.2893049299565487e-014 ;
	setAttr ".jo" -type "double3" -3.0743775263026811 0.068288059887877478 -32.321822832593213 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.090041448750515674 -0.8487288890462974 -0.52110633310788523 1.3877787807814457e-017
		 0.99441954309311131 -0.10549773606333034 7.8496237287950521e-017 1.7347234759768071e-018
		 -0.054975538391145662 -0.51819832167207003 0.85349176305038466 6.9388939039072284e-018
		 6.7938022498352941 8.5421464051846829 0.15265257004051852 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandRing3" -p "RightHandRing2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.5337143182429509 -6.5054363469485565e-006 -1.0677393724733975e-006 ;
	setAttr ".r" -type "double3" -1.9878466759147e-015 -1.837515771048649e-014 1.2295918794183298e-014 ;
	setAttr ".jo" -type "double3" -2.3859824371021645 3.3606119871535745 -68.081160209302197 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.95128142137711147 -0.18819937902882214 -0.24422254415984448 0
		 0.2920458022515543 -0.80397162104815756 -0.5180143646043458 0 -0.09885801297814778 -0.56410160989166125 0.81976610504926872 0
		 6.7457461488138089 8.0891705613055489 -0.12546755057367676 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandRing4" -p "RightHandRing3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.4488036657707033 5.1092527275642396e-006 8.2167768944430009e-007 ;
	setAttr ".jo" -type "double3" 1.4787793334710986e-006 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.95128142137711169 -0.18819937902882228 -0.24422254415984454 3.4694469519536142e-018
		 0.29204580225155452 -0.80397162104815756 -0.51801436460434591 1.3877787807814457e-017
		 -0.098858012978147669 -0.56410160989166114 0.81976610504926872 1.3877787807814457e-017
		 6.3188140440463805 8.004707272946165 -0.23507385893495941 0.99999999999999989;
	setAttr ".radi" 0.1;
createNode joint -n "RightHandPinky1" -p "RightHand";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".t" -type "double3" -0.98219103812281539 0.12893381682641714 0.70624946395646848 ;
	setAttr ".r" -type "double3" -2.7034714792439894e-014 2.544443745170814e-014 1.2722218725854061e-014 ;
	setAttr ".jo" -type "double3" -74.114060907533997 38.483585218668743 -58.918554412712979 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.10689983178532525 -0.46200046500587821 -0.88041353709414416 0
		 0.97425965380468205 0.22542876251352972 -1.9775847626135601e-016 0 0.19847053416729299 -0.85775138785429617 0.47420670988649966 0
		 6.3974356246124726 9.5805237763177207 0.20983365196362708 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandPinky2" -p "RightHandPinky1";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.40654257011828854 -1.294379060823303e-006 2.9899678377631744e-006 ;
	setAttr ".r" -type "double3" -7.036977232738029e-014 3.5284278497485719e-015 -2.6115335704829337e-014 ;
	setAttr ".jo" -type "double3" -1.9602151501050817 15.893695689276061 -25.07615303510806 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.35835732603131959 -0.25944904309812777 -0.89680890992181184 0
		 0.92362637390233471 0.041402938165584158 -0.38105133268797453 0 0.13599392748099914 -0.96486889821712196 0.22479693267829537 0
		 6.4408950392794209 9.3927005641602435 -0.14809260804964622 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandPinky3" -p "RightHandPinky2";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -0.2651400417776042 5.4623807272946578e-006 5.7653927321155152e-007 ;
	setAttr ".r" -type "double3" -4.1446603192821488e-014 -6.2020816288538601e-014 1.7853347958058911e-014 ;
	setAttr ".jo" -type "double3" -6.1955946603540379 -5.5226735794299504 -63.444395262757389 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.96872739365183591 -0.24517417407889999 -0.038168850562340151 3.4694469519536142e-018
		 0.066977712358717578 -0.11026145227693963 -0.99164328172431704 1.7347234759768071e-018
		 0.23891676968290476 -0.96318847403117858 0.1232344945937488 1.3877787807814457e-017
		 6.3458807406368845 9.3239106523243365 -0.38587111403489766 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightHandPinky4" -p "RightHandPinky3";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -0.32697636273014297 -1.7839533708596811e-007 -3.9666734874543863e-006 ;
	setAttr ".jo" -type "double3" 1.9090959104164224e-006 0 0 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.96872739365183569 -0.24517417407890016 -0.038168850562340144 0
		 0.066977712358717537 -0.11026145227693955 -0.99164328172431715 0 0.23891676968290476 -0.96318847403117791 0.12323449459374877 0
		 6.029130707239057 9.2437447270736612 -0.39835138946594761 1;
	setAttr ".radi" 0.1;
createNode joint -n "LeftUpLeg" -p "Hips";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.041511429875702888 0.06803041506298646 -0.92900065762026629 ;
	setAttr ".jo" -type "double3" -11.254692804378649 9.7668239707682094 -159.95748188299592 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.16963888899973284 -0.9258226052535804 0.3377501309258204 -1.3877787807814457e-017
		 0.19234190560359074 0.36723011367569852 0.91002562324283631 -6.9388939039072284e-018
		 -0.96655431233206701 -0.089412231888069807 0.24037099263654593 1.7347234759768071e-018
		 0.93012747776898375 9.7326958551364662 0.56755753332485093 0.99999999999999989;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftLeg" -p "LeftUpLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" 4.5594513144596194 0.12665738547052108 0.13585049235989533 ;
	setAttr ".jo" -type "double3" 1.6942470147842237 4.4400371476360885 -74.433984306202589 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.064518875901000888 -0.5934747178862928 -0.80226247193936218 0
		 0.18612634340826276 -0.796986718328071 0.57460347640622622 0 -0.98040517080538658 -0.11224940996921008 0.16188196631998134 0
		 1.5955155567108443 5.5436670818328153 2.2500974809906866 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftFoot" -p "LeftLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" 3.5001129340212103 0.2168509926922364 -0.14725782426121992 ;
	setAttr ".r" -type "double3" 1.0535587382347899e-014 1.6896696745274908e-015 2.5382317243085801e-014 ;
	setAttr ".ra" -type "double3" 12.056824627864795 1.1096104638190589 -1.5681613850991341 ;
	setAttr ".jo" -type "double3" -2.6985371475999527 -1.3382296231880704 65.633631076869889 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.13385413610296432 -0.97702039476045721 0.16587410427866273 0
		 -0.022514834346713739 0.16433898108662054 0.98614693708886536 0 -0.99074525105219036 -0.13573447431485794 -1.4953316362920077e-015 0
		 1.5544262193627507 3.3101407885991136 -0.45714682540841117 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftToeBase" -p "LeftFoot";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 2.2825467821534358 -3.677613769070831e-016 5.773159728050814e-015 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -8.7757128656190631 27.167976971109212 76.420023936855131 ;
	setAttr ".bps" -type "matrix" 0.46086595309007816 1.6653345369377348e-016 0.88746975908048464 0
		 -2.0649643628384233e-016 0.99999999999999978 -2.133258655895791e-016 0 -0.88746975908048475 0 0.4608659530900785 0
		 1.8599545470024954 1.0800460304403499 -0.078531422444566054 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftToeBase1" -p "LeftToeBase";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.2376895923152984 -1.0019243495633261 1.9984014443252818e-015 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.0503070941224893e-014 3.1805546814635176e-015 6.6394078975550903e-014 ;
	setAttr ".bps" -type "matrix" 0.46086595309007894 -5.7565912589376415e-016 0.88746975908048442 0
		 1.238978617703047e-015 1.0000000000000004 -2.743570409377459e-016 0 -0.88746975908048487 1.4687973319025281e-016 0.46086595309007922 0
		 2.4303635405945432 0.078121680877014654 1.019880661863914 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "LeftToeBase2" -p "LeftToeBase1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" 1.118492923774391 -1.3877787807814457e-017 0 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.8249000307521015e-030 0 -1.1299600123008409e-029 ;
	setAttr ".bps" -type "matrix" 0.46086595309007816 1.6653345369377348e-016 0.88746975908048464 0
		 -2.0649643628384233e-016 0.99999999999999978 -2.133258655895791e-016 0 -0.88746975908048475 0 0.4608659530900785 0
		 1.8599545470024954 1.0800460304403499 -0.078531422444566054 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightUpLeg" -p "Hips";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 1;
	setAttr ".t" -type "double3" -0.037204506686173033 0.057367319202566658 0.93125382014871783 ;
	setAttr ".r" -type "double3" 4.7708320221952783e-015 1.7493050748049347e-014 1.5902773407317587e-014 ;
	setAttr ".jo" -type "double3" -11.254692804378692 9.7668239707681259 20.042518117004089 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.16963888899973256 0.9258226052535804 -0.33775013092582035 0
		 0.19234190560359155 -0.36723011367569869 -0.91002562324283587 0 -0.96655431233206701 0.08941223188806903 -0.24037099263654657 0
		 -0.9301269999999997 9.7326999999999995 0.56755799999999879 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightLeg" -p "RightUpLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 2;
	setAttr ".t" -type "double3" -4.5594539781417964 -0.1149429041801957 -0.13584633889318765 ;
	setAttr ".r" -type "double3" -1.987846675914698e-015 2.1983322382867006e-031 1.2672522558956201e-014 ;
	setAttr ".jo" -type "double3" 1.6942470147838067 4.4400371476360823 -74.433984306202589 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" -0.064518875901002012 0.59347471788629302 0.80226247193936162 0
		 0.18612634340826989 0.79698671832807033 -0.57460347640622489 0 -0.98040517080538536 0.11224940996921594 -0.16188196631998591 0
		 -1.5955199999999992 5.5436699999999988 2.2501000000000002 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightFoot" -p "RightLeg";
	addAttr -ci true -sn "ch" -ln "Character" -at "message";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 3;
	setAttr ".t" -type "double3" -3.50011733762177 -0.21685227584632694 0.14725719455694719 ;
	setAttr ".r" -type "double3" 7.9513867036587939e-016 -7.2556403670886469e-015 -6.5474699887940351e-015 ;
	setAttr ".jo" -type "double3" -2.6985371475990791 -1.3382296231884481 65.633631076869889 ;
	setAttr ".ssc" no;
	setAttr ".bps" -type "matrix" 0.1199930340005782 0.97320238159848238 -0.19616012908431851 0
		 0.18171467473357963 -0.21577988982126695 -0.95938460282370108 0 -0.97600279137808033 0.079474295214002219 -0.20273723787807785 0
		 -1.5544299999999986 3.3101399999999996 -0.45714700000000047 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightToeBase" -p "RightFoot";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -2.2812584558961557 0.062453130038046922 0.044194060846485472 ;
	setAttr ".r" -type "double3" 1.8288189418415217e-014 6.3611093629270241e-015 4.8105889557135688e-014 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.7344071122567 15.657321987899429 76.218094287158607 ;
	setAttr ".bps" -type "matrix" 0.46086595309007905 1.0547118733938987e-015 -0.88746975908048453 0
		 -1.0324796573257789e-015 -0.99999999999999989 -1.7089282211557586e-015 0 -0.88746975908048398 1.3322676295501878e-015 -0.46086595309007916 0
		 -1.859949999999998 1.0800499999999995 -0.078531399999999543 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightToeBase1" -p "RightToeBase";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -1.2376894488313783 1.0019282999999968 1.2085310967524521e-006 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -4.0805321222446931e-014 1.272221872585407e-014 8.9254315748569939e-014 ;
	setAttr ".bps" -type "matrix" 0.46086595309007949 8.120840423633711e-016 -0.88746975908048431 0
		 -1.2389755887909372e-015 -1 -1.3845800506118166e-015 0 -0.88746975908048342 1.6785514629562868e-015 -0.46086595309007927 0
		 -2.4303600000000127 0.07812170000000096 1.0198800000000037 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode joint -n "RightToeBase2" -p "RightToeBase1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" yes;
	setAttr ".oc" 4;
	setAttr ".t" -type "double3" -1.118496288454935 1.3877787807814457e-017 3.5403950040535648e-006 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.46086595309007816 1.6653345369377348e-016 0.88746975908048464 0
		 -2.0649643628384233e-016 0.99999999999999978 -2.133258655895791e-016 0 -0.88746975908048475 0 0.4608659530900785 0
		 1.8599545470024954 1.0800460304403499 -0.078531422444566054 1;
	setAttr ".radi" 0.1;
	setAttr ".liw" yes;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n"
		+ "                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -joints 1\n                -ikHandles 1\n"
		+ "                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n"
		+ "            -maximumNumHardwareLights 0\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n"
		+ "            -shadows 0\n            $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n"
		+ "                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n"
		+ "                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n"
		+ "                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n"
		+ "            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 0\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -shadows 0\n            $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n"
		+ "            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n"
		+ "                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n"
		+ "                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n"
		+ "            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n"
		+ "            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 0\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n"
		+ "            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -shadows 0\n            $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n"
		+ "                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -rendererName \"base_OpenGL_Renderer\" \n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n"
		+ "                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n"
		+ "                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -shadows 0\n                $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n"
		+ "            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -shadows 0\n            $editorName;\nmodelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -docTag \"isolOutln_fromSeln\" \n                -showShapes 0\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n"
		+ "                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n"
		+ "            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n"
		+ "                -showShapes 1\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n"
		+ "                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n"
		+ "                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n"
		+ "                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -stackedCurves 0\n"
		+ "                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n"
		+ "                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n"
		+ "                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n"
		+ "                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n"
		+ "                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n"
		+ "                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n"
		+ "                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range -1 -1 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showUnderworld 0\n                -showInvisible 0\n"
		+ "                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range -1 -1 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Texture Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Texture Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tblendShapePanel -unParent -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n"
		+ "                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n"
		+ "                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -shadows 0\n                -displayMode \"centerEye\" \n"
		+ "                -viewColor 0 0 0 1 \n                $editorName;\nstereoCameraView -e -viewSelected 0 $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n"
		+ "                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -maxConstantTransparency 1\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n"
		+ "                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -shadows 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                $editorName;\nstereoCameraView -e -viewSelected 0 $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-defaultImage \"vacantCell.xpm\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 31 100 -ps 2 69 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"wireframe\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -shadows 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 0.5 -size 12 -divisions 1 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 24 -ast 1 -aet 48 ";
	setAttr ".st" 6;
createNode curveInfo -n "curveInfo1";
	addAttr -ci true -sn "normalizedScale" -ln "normalizedScale" -at "double";
createNode multiplyDivide -n "multiplyDivide1";
	setAttr ".op" 2;
	setAttr ".i2" -type "float3" 2.6533232 1 1 ;
select -ne :time1;
	setAttr ".o" 16;
	setAttr ".unw" 16;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
select -ne :renderGlobalsList1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "LeftFootIndex1.s" "pasted__LeftFootIndex2.is";
connectAttr "pasted__LeftFootIndex2.s" "pasted__LeftFootIndex3.is";
connectAttr "pasted__LeftFootIndex3.s" "pasted__LeftFootIndex4.is";
connectAttr "LeftFootExtraFinger1.s" "pasted__LeftFootExtraFinger2.is";
connectAttr "pasted__LeftFootExtraFinger2.s" "pasted__LeftFootExtraFinger3.is";
connectAttr "pasted__LeftFootExtraFinger3.s" "pasted__LeftFootExtraFinger4.is";
connectAttr "LeftFootMiddle1.s" "pasted__LeftFootMiddle2.is";
connectAttr "pasted__LeftFootMiddle2.s" "pasted__LeftFootMiddle3.is";
connectAttr "pasted__LeftFootMiddle3.s" "pasted__LeftFootMiddle4.is";
connectAttr "LeftFootRing1.s" "pasted__LeftFootRing2.is";
connectAttr "pasted__LeftFootRing2.s" "pasted__LeftFootRing3.is";
connectAttr "pasted__LeftFootRing3.s" "pasted__LeftFootRing4.is";
connectAttr "LeftFootPinky1.s" "pasted__LeftFootPinky2.is";
connectAttr "pasted__LeftFootPinky2.s" "pasted__LeftFootPinky3.is";
connectAttr "pasted__LeftFootPinky3.s" "pasted__LeftFootPinky4.is";
connectAttr "RightFootExtraFinger1.s" "pasted__RightFootExtraFinger2.is";
connectAttr "pasted__RightFootExtraFinger2.s" "pasted__RightFootExtraFinger3.is"
		;
connectAttr "pasted__RightFootExtraFinger3.s" "pasted__RightFootExtraFinger4.is"
		;
connectAttr "RightFootIndex1.s" "pasted__RightFootIndex2.is";
connectAttr "pasted__RightFootIndex2.s" "pasted__RightFootIndex3.is";
connectAttr "pasted__RightFootIndex3.s" "pasted__RightFootIndex4.is";
connectAttr "RightFootMiddle1.s" "pasted__RightFootMiddle2.is";
connectAttr "pasted__RightFootMiddle2.s" "pasted__RightFootMiddle3.is";
connectAttr "pasted__RightFootMiddle3.s" "pasted__RightFootMiddle4.is";
connectAttr "RightFootRing1.s" "pasted__RightFootRing2.is";
connectAttr "pasted__RightFootRing2.s" "pasted__RightFootRing3.is";
connectAttr "pasted__RightFootRing3.s" "pasted__RightFootRing4.is";
connectAttr "RightFootPinky1.s" "pasted__RightFootPinky2.is";
connectAttr "pasted__RightFootPinky2.s" "pasted__RightFootPinky3.is";
connectAttr "pasted__RightFootPinky3.s" "pasted__RightFootPinky4.is";
connectAttr "Reference.s" "Hips.is";
connectAttr "Hips.s" "Spine.is";
connectAttr "Spine.s" "Spine1.is";
connectAttr "Spine1.s" "Spine2.is";
connectAttr "Spine2.s" "Neck_nouse.is";
connectAttr "Neck1_nouse.s" "Head_nouse.is";
connectAttr "Spine2.s" "LeftShoulder.is";
connectAttr "LeftShoulder.s" "LeftArm.is";
connectAttr "LeftArm.s" "LeftForeArm.is";
connectAttr "LeftForeArm.s" "LeftHand.is";
connectAttr "LeftHand.s" "LeftHandThumb1.is";
connectAttr "LeftHandThumb1.s" "LeftHandThumb2.is";
connectAttr "LeftHandThumb2.s" "LeftHandThumb3.is";
connectAttr "LeftHandThumb3.s" "LeftHandThumb4.is";
connectAttr "LeftHand.s" "LeftHandIndex1.is";
connectAttr "LeftHandIndex1.s" "LeftHandIndex2.is";
connectAttr "LeftHandIndex2.s" "LeftHandIndex3.is";
connectAttr "LeftHandIndex3.s" "LeftHandIndex4.is";
connectAttr "LeftHand.s" "LeftHandMiddle1.is";
connectAttr "LeftHandMiddle1.s" "LeftHandMiddle2.is";
connectAttr "LeftHandMiddle2.s" "LeftHandMiddle3.is";
connectAttr "LeftHandMiddle3.s" "LeftHandMiddle4.is";
connectAttr "LeftHand.s" "LeftHandRing1.is";
connectAttr "LeftHandRing1.s" "LeftHandRing2.is";
connectAttr "LeftHandRing2.s" "LeftHandRing3.is";
connectAttr "LeftHandRing3.s" "LeftHandRing4.is";
connectAttr "LeftHand.s" "LeftHandPinky1.is";
connectAttr "LeftHandPinky1.s" "LeftHandPinky2.is";
connectAttr "LeftHandPinky2.s" "LeftHandPinky3.is";
connectAttr "LeftHandPinky3.s" "LeftHandPinky4.is";
connectAttr "Spine2.s" "RightShoulder.is";
connectAttr "RightShoulder.s" "RightArm.is";
connectAttr "RightArm.s" "RightForeArm.is";
connectAttr "RightForeArm.s" "RightHand.is";
connectAttr "RightHand.s" "RightHandThumb1.is";
connectAttr "RightHandThumb1.s" "RightHandThumb2.is";
connectAttr "RightHandThumb2.s" "RightHandThumb3.is";
connectAttr "RightHandThumb3.s" "RightHandThumb4.is";
connectAttr "RightHand.s" "RightHandIndex1.is";
connectAttr "RightHandIndex1.s" "RightHandIndex2.is";
connectAttr "RightHandIndex2.s" "RightHandIndex3.is";
connectAttr "RightHandIndex3.s" "RightHandIndex4.is";
connectAttr "RightHand.s" "RightHandMiddle1.is";
connectAttr "RightHandMiddle1.s" "RightHandMiddle2.is";
connectAttr "RightHandMiddle2.s" "RightHandMiddle3.is";
connectAttr "RightHandMiddle3.s" "RightHandMiddle4.is";
connectAttr "RightHand.s" "RightHandRing1.is";
connectAttr "RightHandRing1.s" "RightHandRing2.is";
connectAttr "RightHandRing2.s" "RightHandRing3.is";
connectAttr "RightHandRing3.s" "RightHandRing4.is";
connectAttr "RightHand.s" "RightHandPinky1.is";
connectAttr "RightHandPinky1.s" "RightHandPinky2.is";
connectAttr "RightHandPinky2.s" "RightHandPinky3.is";
connectAttr "RightHandPinky3.s" "RightHandPinky4.is";
connectAttr "Hips.s" "LeftUpLeg.is";
connectAttr "LeftUpLeg.s" "LeftLeg.is";
connectAttr "LeftLeg.s" "LeftFoot.is";
connectAttr "LeftFoot.s" "LeftToeBase.is";
connectAttr "LeftToeBase.s" "LeftToeBase1.is";
connectAttr "LeftToeBase1.s" "LeftToeBase2.is";
connectAttr "Hips.s" "RightUpLeg.is";
connectAttr "RightUpLeg.s" "RightLeg.is";
connectAttr "RightLeg.s" "RightFoot.is";
connectAttr "RightFoot.s" "RightToeBase.is";
connectAttr "RightToeBase.s" "RightToeBase1.is";
connectAttr "RightToeBase1.s" "RightToeBase2.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "multiplyDivide1.ox" "curveInfo1.normalizedScale";
connectAttr "curveInfo1.al" "multiplyDivide1.i1x";
connectAttr "multiplyDivide1.msg" ":defaultRenderUtilityList1.u" -na;
// End of werewolf_body_skeleton.ma
