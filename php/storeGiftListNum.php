<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;

	$acc = $_POST["account"];
	$giftListNum_0 = $_POST["giftListNum_0"];
	$giftListNum_1 = $_POST["giftListNum_1"];


	$cursor = $collection->find();
	$response = array();
	$giftList = array("giftListNum_0"=>$giftListNum_0,"giftListNum_1"=>$giftListNum_1);

	foreach($cursor as $document){
		if($acc == $document["account"]){
			$collection->update(array("account"=>$acc),array('$set'=>$giftList));
			array_push($response,array("uploadGift"=>'1'));
			echo json_encode($response,JSON_UNESCAPED_UNICODE);
			//$collection->insert(array("a"=>"isa"));
			return 0;
		}		

	}
	array_push($response,array("uploadGift"=>"0"));
	echo json_encode($response,JSON_UNESCAPED_UNICODE);
	//$collection->insert(array("b"=>"isb"));
	return 0;	
	
?>
