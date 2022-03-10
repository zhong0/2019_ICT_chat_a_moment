<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;

	$acc = $_POST["account"];

	$cursor = $collection->find();
	$response = array();
	foreach($cursor as $document){
		if($acc == $document["account"]){
			$num = $document["allEventsNum"];
			if($num == 0){
				array_push($response,array("allEvent"=>'0',"allTime"=>'0', "allPeople"=>'0', "allEmotion"=> '0', "allEventsNum"=> '0',"allDate=" => '0'));
				echo json_encode($response,JSON_UNESCAPED_UNICODE);
				return 0;
			}
			for($i = 0; $i <= $num ; $i++){
				$allEvent = $allEvent.$document["event".$i].'#';
				$allTime = $allTime.$document["eventTime".$i].'#';
				$allPeople = $allPeople.$document["eventPeople".$i].'#';
				$allEmotion = $allEmotion.$document["eventEmotion".$i].'#';
				$allDate = $allDate.$document["eventDate".$i].'#';
			}

			array_push($response,array("allEvent"=>$allEvent,"allTime"=>$allTime,"allPeople"=>$allPeople,"allEmotion"=>$allEmotion,"allEventsNum"=>$num, "allDate"=>$allDate));
			echo json_encode($response,JSON_UNESCAPED_UNICODE);
			return 0;
		}
	}
	return 0;
?>
