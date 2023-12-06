<?php
$output = shell_exec('sudo ./photo-night.sh');
header('Location: //192.168.1.159/photo-night.jpg');
exit()
?>
