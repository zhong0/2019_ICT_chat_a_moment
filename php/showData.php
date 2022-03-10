<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;
	$collectionEmotion = $db->emotionTrack;

	$acc = $_POST["account"];
	$cursor = $collection->find();
	$cursorE = $collectionEmotion->find();

	$response = array();
	
	foreach($cursor as $document){
		if($acc == $document["account"]){
			$happyNum = $document["happyNum"];
			$sadNum = $document["sadNum"];
			$fearNum = $document["fearNum"];
			$angerNum = $document["angerNum"];
			$hateNum = $document["hateNum"];
			$steps = $document["steps"];
			$calories = $document["calories"];	
		}
	}
	foreach($cursorE as $documentE){
		if($acc == $documentE["account"]){
			$anxWeeksValue = $documentE["anxWeeksValue"];
			$depWeeksValue = $documentE["depWeeksValue"];
		}
		array_push($response, array("happyNum"=> $happyNum, "sadNum" => $sadNum, "fearNum" => $fearNum, "angerNum" => $angerNum, "hateNum"=> $hateNum, "steps" => $steps, "calories"=> $calories , "anxWeeksValue" => $anxWeeksValue, "depWeeksValue" => $depWeeksValue));
	}
	echo json_encode($response,JSON_UNESCAPED_UNICODE);
	return 0;	
?>
