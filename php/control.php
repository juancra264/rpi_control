<?php
	$setmode21 = shell_exec("/usr/local/bin/gpio -g mode 21 out");
	if(isset($_GET['on'])){
		$gpio_on = shell_exec("sw_telnet -s 10.40.1.4 -u admin -p rcnsistemas -c 'sys,int gi1/0/1,undo shutdown,quit,quit'");
		$gpio_on = shell_exec("/usr/local/bin/gpio -g write 21 1");
		echo "Control is on";
	}
	else if(isset($_GET['off'])){
		$gpio_off = shell_exec("sw_telnet -s 10.40.1.4 -u admin -p rcnsistemas -c 'sys,int gi1/0/1,shutdown,quit,quit'");
		$gpio_off = shell_exec("/usr/local/bin/gpio -g write 21 0");
		echo "Control is off";
	}
?>
