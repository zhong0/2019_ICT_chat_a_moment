<?php
  date_default_timezone_set("Asia/Taipei");
  $conn = new MongoClient("mongodb://28to27:27017");
  $db = $conn->userTest;
  $userCollection = $db->user;
  $emoCollection = $db->emotionTrack;
  $cursorE = $emoCollection->find();
  $cursorU = $userCollection->find();
  $acc = $_POST["account"];
  foreach ($cursorE as $documentE) {
    if($acc == $documentE["account"]){
      $lastTime = date('Y-m-d H:i:s',$documentE["saveTime"]);
      $emoCollection->update(array("account"=>$acc), array('$set' => array(
        "saveTime"=>date(strtotime('now')))));
    }
  }

  foreach ($cursorU as $documentU) {
    if($acc == $documentU["account"]){
        $happy = $documentU["happyNum"];
        $sad = $documentU["sadNum"];
        $fear = $documentU["fearNum"];
        $anger = $documentU["angerNum"];
        $hate = $documentU["hateNum"];
        $anxScaleValue = $documentU["SumAnx"];
        $depScaleValue = $documentU["SumDep"];
        $step = $documentU["steps"];
        $distortedRes = $documentU["distortedRes"];
    }
  }
  echo $anxScaleValue;
  $updateTime = date('Y-m-d  00:00:00',strtotime('now'));
  if($updateTime > $lastTime){
    foreach($cursorU as $documentU){
      $userCollection->update(array("account"=>$acc), array('$set' => array(
        "happyNum"=>30, "sadNum"=>30, "fearNum"=>30, "angerNum"=>30, "hateNum"=>30,"steps"=>0,"calories"=>0,"distortedRes"=>0)));
    }
  }


  foreach ($cursorE as $documentE) {
    if($acc == $documentE["account"]){
      $emoCollection->update(array("account"=>$acc), array('$set' => array(
        "saveTime"=>date(strtotime('now')),
        "happy".date('Ymd', strtotime('now'))=>$happy,
        "sad".date('Ymd', strtotime('now'))=>$sad,
        "fear".date('Ymd', strtotime('now'))=>$fear,
        "anger".date('Ymd', strtotime('now'))=>$anger,
        "hate".date('Ymd', strtotime('now'))=>$hate,
        "anxScaleValue".date('Ymd', strtotime('now'))=>$anxScaleValue,
        "depScaleValue".date('Ymd', strtotime('now'))=>$depScaleValue,
        "steps".date('Ymd', strtotime('now'))=>$step,
        "distortedRes".date('Ymd', strtotime('now'))=>$distortedRes
      )));
    }
  }
  $abnormalStep = 0;
  $totalDistortedRes = 0;
  foreach ($cursorE as $documentE){
    if($acc == $documentE["account"]){
      $totalHappy = $documentE["happy".date('Ymd',strtotime('now'))];
      $totalSad = $documentE["sad".date('Ymd',strtotime('now'))];
      $totalAnger = $documentE["anger".date('Ymd',strtotime('now'))];
      $totalFear = $documentE["fear".date('Ymd',strtotime('now'))];
      $totalHate = $documentE["hate".date('Ymd',strtotime('now'))];
      $nowAnxScaleValue = $documentE["anxScaleValue".date('Ymd',strtotime('now'))];
      $nowDepScaleValue = $documentE["depScaleValue".date('Ymd',strtotime('now'))];

      for($i = 1; $i <=13; $i++){
        $totalHappy = $totalHappy + $documentE["happy".date('Ymd', strtotime("-$i day"))];
        $totalSad = $totalSad + $documentE["sad".date('Ymd', strtotime("-$i day"))];
        $totalAnger = $totalAnger + $documentE["anger".date('Ymd', strtotime("-$i day"))];
        $totalFear = $totalFear + $documentE["fear".date('Ymd', strtotime("-$i day"))];
        $totalHate = $totalHate + $documentE["hate".date('Ymd', strtotime("-$i day"))];
        $totalDistortedRes = $totalDistortedRes + $documentE["distortedRes".date('Ymd', strtotime("-$i day"))];

        if($documentE["steps".date('Ymd', strtotime("-$i day"))]<2000){
          $abnormalStep = $abnormalStep+1;
        }
      }
    }
  }
  $angerPercentage =( $totalAnger/($totalHappy+$totalSad+$totalAnger+$totalFear+$totalHate))*100;
  $fearPercentage =( $totalFear/($totalHappy+$totalSad+$totalAnger+$totalFear+$totalHate))*100;
  $hatePercentage =( $totalHate/($totalHappy+$totalSad+$totalAnger+$totalFear+$totalHate))*100;
  $sadPercentage = ( $totalSad/($totalHappy+$totalSad+$totalAnger+$totalFear+$totalHate))*100;
  $anxEmotionValue = (($angerPercentage+$fearPercentage+$hatePercentage)/3)*0.6;
  $anxScaleValue = $nowAnxScaleValue*0.4;

  $depEmotionValue = (($angerPercentage+$sadPercentage)/2)*0.5;
  $depScaleValue = $nowDepScaleValue*(100/72)*0.3;
  $depAbnormalSteps = $abnormalStep*0.05;
  $depDistortedRes = $totalDistortedRes*0.15;

  echo $nowAnxScaleValue;
  $anxScaleValue = $anxEmotionValue + $anxScaleValue;
  $depScaleValue = $depEmotionValue + $depScaleValue + $depAbnormalSteps + $depDistortedRes;
  foreach($cursorE as $documentE){
    $emoCollection->update(array("account"=>$acc), array('$set' => array(
      "anxWeeksValue"=> $anxScaleValue, "depWeeksValue"=>$depScaleValue)));
  }

  return 0;
 ?>
