<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;
	
	$acc = $_GET["account"];
	$cursor = $collection->find();
	foreach($cursor as $document){
		if($acc == $document["account"]){
			for($i = 0; $i < 25; $i++){
				${"anxGrade". $i} = $_GET["anxGrade" . $i];
				$newdata = array(
					'$set' => array(
						('anxGrade' . $i) => "${'anxGrade' . $i}"
					)
				);
				$collection->update(array("account" => $acc), $newdata);
			}
			$newdata = array('$set' => array('SumAnx' => $GET["SumAnx"]));
			$collection->update(array("account" => $acc), $newdata);
			return 0;
		}
	}
?>
