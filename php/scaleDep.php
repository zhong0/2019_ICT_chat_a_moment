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
			for($i = 1; $i <= 18; $i++){
				${"dep". $i} = $_POST["dep" . $i];
				$newdata = array(
					'$set' => array(
						('dep' . $i) => "${'dep' . $i}" + 0
					)
				);
				$collection->update(array("account" => $acc), $newdata);
			}
			$newdata = array('$set' => array('SumDep' => $_POST["SumDep"] +0));
			$collection->update(array("account" => $acc), $newdata);
		}
	}
	foreach($cursorE as $documentE){
		if($acc == $documentE["account"]){
			$collectionE->update(array("account"=>$acc),array('$set'=>array("depScaleValue".date('Ymd',strtotime('now')))));
		}
	}
	return 0;
?>
