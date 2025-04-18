The APSA is a board designed to regulate voltages to various subsystems such as payloads or radios.  It is capable of turning these outputs on or off automatically from a web interface for easy scripting in the future.  This code is designed to run on a Banana Pi M2 Zero.

# Hardware Design

### Voltage Regulators
The APSA includes 8 voltage regulators, each capable of outputting up to 24v at 6.48A.  These regulators have their voltages set by the potentiometers on the APSA main board and can be adjusted from 0.3 to 24v.  Each regulator is capable of 6.48A independently, however the board must never exceed 5A when powered via a barrel jack adapter.  If using the XT60 connector to power the APSA, the outputs must never draw more than 20A total.

> The APSA does not include any current monitoring systems.  It is only capable of controlling power enable/disable states to each output.  If a regulator overheats or reaches its current limit, the regulator will turn off the output with no feedback to the Banana Pi.

> The inputs to the APSA are current protected by a pair of fuses.  The barrel jack is fused at up to 5A to prevent the connector from melting.  The XT60 is fused at 20A.  The user is expected to know the current consumed by each output and ensure they do not overload the board.  If any individual output channel exceeds 6.48A, the regulator for that output will go into thermal protection mode and shut down with no feedback to the Pi.

The APSA includes an onboard Banana Pi M2 Zero for control of the voltage regulators.  The GPIO of this board operates at 3.3v logic and can enable or disable each of the regulators independently.

# Software Design

The APSA code runs on a Banana Pi M2 Zero running Armbian.  The APSA server is written in Python using Flask to host the webpage.  

### APSA Service
All APSA software can be found in the following folder of the APSA.  
```/home/apsa/apsa_server```

On boot, systemd will launch the apsa_server service.  If the Python server or the templates files are ever changed, restart the server by calling the following command: 
```sudo systemctl restart apsa_server```  

Changes can be made to the systemctl service (changing ports, etc.) using this command: 
```sudo nano /etc/systemd/system/gpio_server.service```

### Manual control of GPIO
If there is ever a need to manually trigger the GPIO on the Pi, shut down the apsa_erver using the following command:
```sudo systemctl stop apsa_server```  

After doing this, the GPIO can be controlled via the command line using the following commands:
```gpioset gpiochip0 14=1```
Please see this link for details on what GPIO number corresponds to the GPIO pin name:
https://wiki.banana-pi.org/%E9%A6%99%E8%95%89%E6%B4%BE_BPI-M2_ZERO#GPIO_PIN_.E5.AE.9A.E4.B9.89



### Hostname Changes
Changing the hostname is encouraged and can be done by running the following command:
```sudo hostnamectl hostname <new_hostname>```

If updating the hostname, it is recommended to adjust the mdns (avahi-daemon) settings as well to avoid conflict on the network.  To do this, adjust the /etc/hosts file using the following command.  Note that the hostname must be alphanumeric and cannot have spaces or capitalization.
```sudo nano /etc/hosts```

After adjusting hostname and mdns settings, restart the device:
```sudo reboot```

### WiFi settings
If the WiFi settings need to be changed, use the following commands:
```sudo armbian-config```
