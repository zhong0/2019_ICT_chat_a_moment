<?php
	$conn = new MongoClient("mongodb://28to27:27017");
	$db = $conn->test;
	$collection = $db->one;

	$acc = $_GET["account"];
	$cursor = $collection->find();
	foreach($cursor as $document){
		if($acc == $document["_id"]){
			/*
			for($i = 0; $i < 5; $i++){
				${"depGrade". $i} = $_GET["depGrade" . $i];
			}
			for($i = 0; $i < 5; $i++){
				$newdata = array(
					'$set' => array(
						('depGrade' . $i) => "${'depGrade' . $i}"

					)
				);
				$collection->update(array("_id" => $acc), $newdata);
			}*/
			for($i = 0; $i < 5; $i++){
				${"depGrade". $i} = $_GET["depGrade" . $i];
				$newdata = array(
					'$set' => array(
						('depGrade' . $i) => "${'depGrade' . $i}"

					)
				);
				$collection->update(array("_id" => $acc), $newdata);
			}
			for($i = 0; $i < 5; $i++){
				${"anxGrade". $i} = $_GET["anxGrade" . $i];
				$newdata = array(
					'$set' => array(
						('anxGrade' . $i) => "${'anxGrade' . $i}"

					)
				);
				$collection->update(array("_id" => $acc), $newdata);
			}
			$newdata = array('$set' => array('SumDep' => $_GET["SumDep"]));
			$collection->update(array("_id" => $acc), $newdata);
			$newdata = array('$set' => array('SumAnx' => $_GET["SumAnx"]));
			$collection->update(array("_id" => $acc), $newdata);
			return 0;
		}
	}
?>
