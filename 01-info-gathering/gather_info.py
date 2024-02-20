from genie.testbed import load
from pprint import pprint

testbed = load("testbed.yaml")

for name, device in testbed.devices.items():
    device.connect(log_stdout=False)

    data = device.parse("show version")

    print("the version is ", data["version"]["version_short"])
