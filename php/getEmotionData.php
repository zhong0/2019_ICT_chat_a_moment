<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;

	$acc = $_POST["account"];
	$getHappy = $_POST["happyTimes"];
	$getSad = $_POST["sadTimes"];
	$getNeutral = $_POST["neutralTimes"];
	$getFear = $_POST["fearTimes"];
	$getAnger = $_POST["angerTimes"];
	$getHate = $_POST["hateTimes"];

	$cursor = $collection ->find();
	$response = array();

	foreach($cursor as $document){
		if($acc == $document["account"]){
			$newHappy = $document["happyNum"] + $getHappy;
			$newSad = $document["sadNum"] + $getSad;
			$newNeutral = $document["neutralNum"] + $getNeutral;
			$newFear = $document["fearNum"] + $getFear;
			$newAnger = $document["angerNum"] + $getAnger;
			$newHate = $document["hateNum"] + $getHate;
			
			$collection->update(array("account"=>$acc),array('$set'=>array("happyNum"=>$newHappy)));
			$collection->update(array("account"=>$acc),array('$set'=>array("sadNum"=>$newSad)));
			$collection->update(array("account"=>$acc),array('$set'=>array("neutralNum"=>$newNeutral)));
			$collection->update(array("account"=>$acc),array('$set'=>array("fearNum"=>$newFear)));
			$collection->update(array("account"=>$acc),array('$set'=>array("angerNum"=>$newAnger)));	
			$collection->update(array("account"=>$acc),array('$set'=>array("hateNum"=>$newHate)));
		}
	}

	array_push($response,array("checkSavedBack"=>'1'));
	echo json_encode($response,JSON_UNESCAPED_UNICODE);
	return 0;
?>
