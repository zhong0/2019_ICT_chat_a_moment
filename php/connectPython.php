<?php
	header("Content-type: text/html; charset = utf-8");
	$output = shell_exec("python3 /var/www/html/getEmotion.py");
	echo $output;
?>
