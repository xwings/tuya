<?php

$admin_user = "pr0_adm1n";
$admin_pw = clean_hash("0e408306536730731920197920342119");

function clean_hash($hash) {
    return preg_replace("/[^0-9a-f]/","",$hash);
	print preg_replace("/[^0-9a-f]/","",$hash);
}

function myhash($str) {
	
    print clean_hash(md5(md5($str) . "SALT"));
}



?>
