<?php
function callPy(){
	$return = exec("php-mongo:var/www/html testConnPyt.py");
	return $return;
}
$output = callPy();
echo $output;
?>
