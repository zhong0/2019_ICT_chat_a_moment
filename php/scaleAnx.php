<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;
	$collectionE = $db->emotionTrack;

	$acc = $_POST["account"];
	$cursor = $collection->find();
	$cursorE = $collectionE->find();
	foreach($cursor as $document){
		if($acc == $document["account"]){
			for($i = 1; $i <= 25; $i++){
				${"anx". $i} = $_POST["anx" . $i];
				$newdata = array(
					'$set' => array(
						('anx' . $i) => "${'anx' . $i}" +0
					)
				);
				$collection->update(array("account" => $acc), $newdata);
			}
			$newdata = array('$set' => array('SumAnx' => $_POST["SumAnx"] + 0));
			$collection->update(array("account" => $acc), $newdata);
		}
	}
	
	foreach($cursorE as $documentE){
		if($acc == $documentE["account"]){
			$collectionE->update(array("account"=>$acc), array('$set'=>array("anxScaleValue".date('Ymd',strtotime('now')))));
		}
	}
	return 0;
?>
