<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;
	$trackCollection = $db->emotionTrack;

	$acc = $_POST["account"];
	$pswd = $_POST["password"];
	$name = $_POST["username"];
	$happyNum = 30;
	$sadNum = 30;
	$neutralNum = 30;
	$fearNum = 30;
	$angerNum = 30;
	$hateNum = 30;
	$step = 0;
	$cal = 0;
	$SumAnx = -1;
	$SumDep = -1;
	$gift_0 = 0;
	$gift_1 = 0;
	$lifeValue = 0.5;
	$distortedNum = 0;

	for($i = 1; $i <= 25; $i++){
		${"anx". $i} = -1;
	
	}
	for($i = 1; $i <= 18; $i++){
		${"dep". $i} = -1;
	}
	
	$cursor = $collection->find();
	$response = array();

	foreach($cursor as $document){
		if($acc == $document["account"]){
			array_push($response,array("checkReg"=>'1'));
			echo json_encode($response,JSON_UNESCAPED_UNICODE);
			return 0;
		}
	}
	$information = array(
		"account" => $acc,
		"password" => $pswd,
		"username" => $name,
		"happyNum" => $happyNum,
		"sadNum" => $sadNum,
		"neutralNum" => $neutralNum,
		"fearNum" => $fearNum,
		"angerNum" => $angerNum,
		"hateNum" => $hateNum,
		"steps" => $step,
		"calories" => $cal,
		"heartRate" => 0,
		"distortedRes"=> $distortedNum,
		"giftListNum_0" => $gift_0,
		"giftListNum_1" => $gift_1,
		"lifeValue" => $lifeValue,
		"allEventsNum" => 0
	);
	
	$scale = array(
		"SumAnx" => $SumAnx,
		"SumDep" => $SumDep
	);
	
	for($i = 1; $i <= 25; $i++){
		$scaleAnx = array(
			('anx' . $i) => ${'anx' . $i}
		);
		$scale = array_merge($scale, $scaleAnx);
	}
	for($i = 1; $i <= 18; $i++){
		$scaleDep = array(
			('dep' . $i) => ${'dep' . $i}
		);
		$scale = array_merge($scale, $scaleDep);
	}
	date_default_timezone_set("Asia/Taipei");	
	$emoData = array(
		"account"=>$acc,
		"anxWeeksValue"=>0,
		"depWeeksValue"=>0,
		"saveTime"=>date(strtotime('now'))
	);
	for($i = 1; $i<=14; $i++){
		$happy = array(
			('happy'.date('Ymd', strtotime("-$i day")))=> 30);
		$sad = array(
			('sad'.date('Ymd', strtotime("-$i day"))) => 30);
		$anger = array(
			('anger'.date('Ymd', strtotime("-$i day"))) => 30);
		$fear = array(
			('fear'.date('Ymd', strtotime("-$i day"))) => 30);
		$hate= array(
			('hate'.date('Ymd', strtotime("-$i day"))) => 30);
		$anxScaleValue = array(
			('anxScaleValue'.date('Ymd',strtotime("-$i day"))) => 0);
		$depScaleValue = array(
			('depScaleValue'.date('Ymd',strtotime("-$i day"))) => 0);
		$step = array(
			('step'.date('Ymd',strtotime("-$i day"))) => 2000);
		$distortedRes = array(
			('distortedRes'.date('Ymd',strtotime("-$i day"))) => 0);
		$emoData = array_merge($emoData,$happy, $sad, $anger, $fear, $hate, $anxScaleValue, $depScaleValue,$step,$distortedRes);
	}

	$information = array_merge($information, $scale);
	$collection->insert($information);
	$trackCollection->insert($emoData);
	array_push($response,array("checkReg"=>'0'));
	echo json_encode($response,JSON_UNESCAPED_UNICODE);
	return 0;
?>
