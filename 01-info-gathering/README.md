# Demo 1 : retrieve data using pyATS 

In this demo you saw us using pyATS in order to retrieve data from your networking devices, in the demo it was showcased on a switch. In the example we retrieved the version data which is running on the switch. However, it is up to you which type of data you want to retrieve, as you can choose to use whichever CLI command you want. 

## Getting started
* Setup your workstation and development environment. Learn how to do that [here](https://developer.cisco.com/learning/modules/dev-setup/)
* Ensure your virtual environment is enabled
* Install the required libraries

```bash
pip install -r requirements.txt
```

## The testbed file
The testbed file in the PyATS framework is a YAML file that describes the network topology, devices, connections, and credentials necessary to run tests against network infrastructure.

A testbed file typically contains the following information:

* Device hostnames or IP addresses.
* Device types (e.g., router, switch, firewall).
* Connection information (e.g., interfaces, port numbers).
* Credentials for accessing devices (e.g., usernames, passwords, SSH keys).
* Additional parameters such as device attributes and custom configurations.

Make sure you update the **testbed-yaml** file with the correct information against the device you want to test.
```yaml
---
testbed:
  name: ciscolab
  credentials: 
    default:
      username: "USERNAME"
      password: "PASSWORD"
      enable: "PASSWORD"

devices:
  switch:
    os: iosxe
    type: iosxe
    connections:
      defaults:
        class: unicon.Unicon
      ssh:
        protocol: ssh
        ip: "HOST"
        port: "22"
```

## Run the script

The next step is to run the script itself **gather_info.py**. Make sure you are in the correct directoty.
```bash
python gather_info.py
```

## Breaking down the script

The first thing we do is to import the modules that we need in order to work with PyATS for this use case. In this case we need the load() module, in order to help us pass the testbed data to PyATS. We also import the pprint module which will help us print the output data in a nice way.

```python
from genie.testbed import load
from pprint import pprint
```

We then use the load() module in order to load our testbed data to PyATS
```python
testbed = load("testbed.yaml")
```

The next step is that we loop through each of the devices in the testbed file (in our example we only have one switch), and then we use the connect() function in order to connect to each of the devices.
```python
for name, device in testbed.devices.items():
    device.connect(log_stdout=False)
```

Once we have a connection established to the device, then we use the parse() function of PyATS to execute the CLI command "show version", in order to retrive parsed data in JSON format. We then choose which data point we want to work with and print it out.
```python
    data = device.parse("show version")
    print("the version is ", data["version"]["version_short"])
```

The whole code looks like this:
```python
from genie.testbed import load

testbed = load("testbed.yaml")

for name, device in testbed.devices.items():
    device.connect(log_stdout=False)

    data = device.parse("show version")

    print("the version is ", data["version"]["version_short"])

```
