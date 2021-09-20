import requests
import argparse


parser = argparse.ArgumentParser(
    description="Switches the POE of a port of an Unifi Switch"
)
parser.add_argument("url", help="The URL of your Unifi Controler")
parser.add_argument("username", help="Your username")
parser.add_argument("password", help="Your password")
parser.add_argument("device_mac", help="The MAC Address of the switch")
parser.add_argument("port", help="The port number", type=int)
parser.add_argument("status", help="The status of the port", choices=["on", "off"])

args = parser.parse_args()
session = requests.Session()

# Parse the status
poe_mode = "auto" if args.status == "on" else "off"

# Cleanup and check base url
base_url = args.url
try:
    session.get(base_url)
except:
    raise Exception("Unable to access homepage of the controler, please check URL")

if base_url[-1] != "/":
    base_url = base_url + "/"


def check_response(response, message):
    if response.status_code != 200:
        raise Exception(f"{message}: API returned HTTP Code {response.status_code}")

    try:
        response_content = response.json()
    except:
        raise Exception(f"{message}: API return invalid JSON")

    code = response_content["meta"]["rc"]
    if code != "ok":
        error_message = response_content["meta"]["msg"]
        raise Exception(f"{message}: API returned {code} ({error_message})")

    return response_content["data"]


# Log in
session = requests.Session()
check_response(
    session.post(
        base_url + "api/login",
        json={"username": args.username, "password": args.password},
        headers={"referer": base_url + "login/"},
    ),
    "Unable to log-in, please check username/password",
)

# List devices to check we can find the correct one
data = check_response(
    session.get(base_url + "api/s/default/stat/device"),
    "Error while fetching device list",
)
devices = {device["mac"]: device for device in data}
if args.device_mac not in devices:
    raise Exception(
        f"Unable to find device {args.device_mac}, available devices : {list(devices.keys())}"
    )

# Get the port
device = devices[args.device_mac]
ports = {port["port_idx"]: port for port in device["port_table"]}
ports_overrides = {port["port_idx"]: port for port in device["port_overrides"]}
if args.port not in ports:
    raise Exception(
        f"Unable to find port {args.port} on device {args.device_mac}, available ports : {list(ports.keys())}"
    )
if not ports[args.port]["port_poe"]:
    raise Exception(
        f"Port {args.port} of device {args.device_mac} does not support POE"
    )

# Send the overrive
overrides = device["port_overrides"].copy()
modified = False
for port_overrides in overrides:
    if port_overrides["port_idx"] == args.port:
        port_overrides["poe_mode"] = poe_mode
        modified = True

if not modified:
    raise Exception("Unable to generate overrides for port...")

check_response(
    session.put(
        base_url + f"api/s/default/rest/device/{device['device_id']}",
        json={"port_overrides": overrides},
    ),
    "Unable to update overrides",
)
