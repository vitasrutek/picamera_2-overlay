<html>
<head>
<meta content="text/html; charset=ISO-8859-1" http-equiv="content-type" name="viewport" content="width=device-width, initial-scale=1">
<title>PiCamera stream</title>
<style>
.container {
  position: relative;
  font-family: Arial;
}

.text-block {
  position: absolute;
  top: 920px;
  left: 10px;
  background-color: black;
  color: white;
  padding-left: 10px;
  padding-right: 10px;
  background: rgba(0, 0, 0, .5)
}

.a1 {
  position: absolute;
  top: 1025px;
  left: 900px;
  background-color: black;
  color: white;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 10px;
  padding-right: 10px;
  background: rgba(0, 0, 0, .5)
  width: 200px
  display: inline;
}

.a2 {
  position: absolute;
  top: 1025px;
  left: 1050px;
  background-color: black;
  color: white;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 10px;
  padding-right: 10px;
  outline: none;
  background: rgba(0, 0, 0, .5)
  white-space: nowrap;
}

.a3 {
  position: absolute;
  top: 1025px;
  left: 1200px;
  background-color: black;
  color: white;
  padding-top: 10px;
  padding-bottom: 10px;
  padding-left: 10px;
  padding-right: 10px;
  outline: none;
  background: rgba(0, 0, 0, .5)
  white-space: nowrap;
}

</style>
</head>
<body>
<div class="container">
    <img src="http://192.168.1.159:8000/stream.mjpg" alt="" width="1440" height="1080" />
    <div class="text-block">
        <p style="font-size:20px; font-family:verdana">Temperature:
        <?php
        $output = shell_exec('./temperature.sh');
        echo $output;
        ?></p>
        <p style="font-size:20px; font-family:verdana">CPU temperature:
        <?php
        $output = shell_exec('./temperature_cpu.sh');
        echo "$output";
        ?></p>
        <p style="font-size:20px; font-family:verdana">Uptime:
        <?php
        $output = shell_exec('./uptime_cpu.sh');
        echo "$output";
        ?></p>
</div>
<p style="font-size:20px; font-family:verdana">
<a class="a1" href="http://192.168.1.159/photo-day.php" target="_blank">Photo - day</a>
<a class="a2" href="http://192.168.1.159/photo-night.php" target="_blank">Photo - night</a>
</body>
</html>
