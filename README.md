# UniFi POE CLI (Python)

Python CLI to update the POE state of a port on an Unifi Controler


```
usage: update_poe.py [-h] url username password device_mac port {on,off}

Switches the POE of a port of an Unifi Switch

positional arguments:
  url         The URL of your Unifi Controler
  username    Your username
  password    Your password
  device_mac  The MAC Address of the switch
  port        The port number
  {on,off}    The status of the port

optional arguments:
  -h, --help  show this help message and exit
```
