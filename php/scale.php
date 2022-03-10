<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->userTest;
	$collection = $db->user;

	$acc = $_POST["account"];
	$cursor = $collection->find();
	foreach($cursor as $document){
		if($acc == $document["account"]){
			for($i = 0; $i < 18; $i++){
				${"depGrade". $i} = $_POST["depGrade" . $i];
				$newdata = array(
					'$set' => array(
						('depGrade' . $i) => "${'depGrade' . $i}"
					)
				);
				$collection->update(array("account" => $acc), $newdata);
			}
			for($i = 0; $i < 25; $i++){
				${"anxGrade". $i} = $_POST["anxGrade" . $i];
				$newdata = array(
					'$set' => array(
						('anxGrade' . $i) => "${'anxGrade' . $i}"
					)
				);
				$collection->update(array("account" => $acc), $newdata);
			}
			$newdata = array('$set' => array('SumDep' => $_POST["SumDep"]));
			$collection->update(array("account" => $acc), $newdata);
			$newdata = array('$set' => array('SumAnx' => $_POST["SumAnx"]));
			$collection->update(array("account" => $acc), $newdata);
			return 0;
		}
	}
?>