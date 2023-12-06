<?php
$output = shell_exec('sudo ./photo-day.sh');
header('Location: //192.168.1.159/photo-day.jpg');
exit()
?>
