# Demo 2 : take a snapshot of the state of your network!

In this demo you saw us using pyATS in order take a snapshot of the state of our network (in this example, the configuration data of one switch). 

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

## Take a snapshot

You can take a snapshot of your whole network through only one command by using PyATS! First make sure that you are in the `02-config-diff` folder. Then execute the followinf command: 
```bash
genie learn config --testbed-file testbed.yaml --output old
```

What we do here is that we instruct PyATS to learn about the `config` feature of the devices that you have listed in your testbed file (which we point to by using the `--testbed-file` option). But what is a feature? In pyATS, a device's functionality is modeled into a set of *features*. An example of a *feature* is our config, which captures the entire device's current running configuration. But if you have a routing protocol like OSPF or BGP configured on your device, these are *features* that could be learned as well (`genie learn bgp --testbed-file testbed.yaml --output bgp_only` - This won't work on the sandbox since BGP is not configured there). 

When we instruct pyATS to *learn* a feature, your device's BGP configuration for example, pyATS will issue a set of commands to the device and retrieve all information of your BGP configuration. This information is then summarized into a computer-readable structured data file. 

Let's have a look at each of the files that have been created. After running the command, your folder should have the following structure:

```
- 02-config_diff
  |- testbed.yaml
  |- old/
     |- config_iosxe_csr1000v-1_console.txt
     |- config_iosxe_csr1000v-1_ops.txt
     |- connection_csr1000v-1.txt
```
The `connection_csr1000v-1.txt` file contains the connection log from pyATS. `config_iosxe_csr1000v-1_console.txt` contains the raw text of the commands that have been issued. Here you can see all the commands (for this example only the `show running-config` command) and their output that was parsed for this feature. Finally, `config_iosxe_csr1000v-1_ops.txt` is a json-dump of the dictionary containing all the information parsed from the `show running-config` command. 

Now in order to see a difference between the two snapshots we'll have to make some changes to the device. The changes you do are up to you. For this example we will change the interface status as well as the description of our `GigabitEthernet 2` interface. SSH into the device, go into enable and then config mode and change the interface configuration before exiting. The username is `developer` and the password is `C1sco12345`.

```bash
$ ssh developer@sandbox-iosxe-latest-1.cisco.com
csr1000v-1# enable
csr1000v-1# conf t
csr1000v-1(config)# interface GigabitEthernet 2
csr1000v-1(config-if)# description New networking interface
csr1000v-1(config-if)# shutdown
csr1000v-1(config-if)# exit
csr1000v-1(config)# exit
```

With our changes done, disconnect from the device and come back to the terminal on your computer. We can now take another snapshot of the device configuration. The command is the same as in step 3 with the only difference being the output directory. 
```
$ genie learn config --testbed-file testbed.yaml --output new
```

We now have a new folder called `new` with the same structure as the `old` folder. We can instruct genie to calculate the diff between the two configuration snapshots. 
```
$ genie diff old new
```

The previous step will create a new file containing the diff for each device. In our example this diff file will be called `diff_config_iosxe_csr1000v-1_ops.txt`. You can show the content of the diff using the `cat` command.
```
$ cat diff_config_iosxe_csr1000v-1_ops.txt
```