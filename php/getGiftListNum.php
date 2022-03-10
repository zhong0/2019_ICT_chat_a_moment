<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;

	$acc = $_POST["account"];
	


	$cursor = $collection->find();
	$response = array();

	foreach($cursor as $document){
		if($acc == $document["account"]){
			$gift_0 = $document["giftListNum_0"];
			$gift_1 = $document["giftListNum_1"];
			array_push($response,array("gift_0"=>"$gift_0","gift_1"=>"$gift_1"));
			echo json_encode($response,JSON_UNESCAPED_UNICODE);
			//$collection->insert(array("a"=>"isa"));
			return 0;
		}		

	}
	array_push($response,array("gift_0"=>"-1","gift_1"=>"-1"));
	echo json_encode($response,JSON_UNESCAPED_UNICODE);
	return 0;	
	
?>
