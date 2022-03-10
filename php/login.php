<?php

	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;

	$acc = $_POST["account"];
	$pswd = $_POST["password"];
	
	$cursor = $collection->find();
	$response = array();
	foreach($cursor as $document){
		if($acc == $document["account"] && $pswd == $document["password"]){
			$nowTime = time();
			if($nowTime - $document["lastChatTime"]>10){ //change 10 to anytime to define "chat too less"	
				array_push($response,array("check"=>"Login Success","username"=>$document["username"],"gift_0"=>$document["giftListNum_0"],"gift_1"=>$document["giftListNum_1"],"lifeValue"=>$document["lifeValue"],"chatTooLess"=>"yes"));
			}
			else{
				array_push($response,array("check"=>"Login Success","username"=>$document["username"],"gift_0"=>$document["giftListNum_0"],"gift_1"=>$document["giftListNum_1"],"lifeValue"=>$document["lifeValue"],"chatTooLess"=>"no"));
			}
		echo json_encode($response,JSON_UNESCAPED_UNICODE);
			return 0;
		}else if($acc == $document["account"] && $pswd != $document["password"]){
			array_push($response,array("check"=>"Wrong Password","username"=>"","gift_0"=>"0","gift_1"=>"0","lifeValue"=>$document["lifeValue"],"chatTooLess"=>"0"));
			echo json_encode($response,JSON_UNESCAPED_UNICODE);
			return 0;
		}	
	}
	array_push($response,array("check"=>"No Account","username"=>"","gift_0"=>"0","gift_1"=>"0","lifeValue"=>$document["lifeValue"],"chatTooLess"=>"0"));
	echo json_encode($response,JSON_UNESCAPED_UNICODE);
	return 0;
?>

