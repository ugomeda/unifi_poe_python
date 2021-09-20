# UniFi POE CLI (Python)

Python CLI to update the POE state of a port on an Unifi Controler


```
usage: update_poe.py [-h] [--set {on,off}] url username password device_mac port

Get and set the POE of a port of an Unifi Switch

positional arguments:
  url             The URL of your Unifi Controler
  username        Your username
  password        Your password
  device_mac      The MAC Address of the switch
  port            The port number

optional arguments:
  -h, --help      show this help message and exit
  --set {on,off}  Updates the status of the port
```
