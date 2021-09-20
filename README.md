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

## Home Assistant switch

This can be used as a switch on Home Assistant using the [command line switch](https://www.home-assistant.io/integrations/switch.command_line/) :

```
switch:
  - platform: command_line
    switches:
      poe_entrance_camera:
        command_on: "python3 /config/scripts/update_poe.py https://unifi.local/ Administrator MySuperPassword 01:02:03:04:05:06 5 --set on"
        command_off: "python3 /config/scripts/update_poe.py https://unifi.local/ Administrator MySuperPassword 01:02:03:04:05:06 5 --set off"
        command_state: "python3 /config/scripts/update_poe.py https://unifi.local/ Administrator MySuperPassword 01:02:03:04:05:06 5"
        value_template: '{{ value == "on" }}'
        friendly_name: Entrance Camera Power
```
