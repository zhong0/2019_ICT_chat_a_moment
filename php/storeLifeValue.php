
<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;

	$acc = $_POST["account"];
	$lifeValue = $_POST["lifeValue"];

	$cursor = $collection->find();
	$response = array();

	foreach($cursor as $document){
		if($acc == $document["account"]){
			$collection->update(array("account"=>$acc),array('$set'=>array("lifeValue"=>$lifeValue,"lastChatTime"=>time())));
			array_push($response,array("uploadLifeValue"=>"ok"));
			echo json_encode($response,JSON_UNESCAPED_UNICODE);
			//$collection->insert(array("a"=>"isa"));
			return 0;
		}		

	}
	array_push($response,array("uploadLifeValue"=>"no"));
	echo json_encode($response,JSON_UNESCAPED_UNICODE);
	//$collection->insert(array("b"=>"isb"));
	return 0;	
	
?>
