'''
This module defines the job function apply_configuration()
'''
from genie.testbed import load

def apply_configuration(testbed, device, config):
    testbed = load('testbed-sandbox.yaml')
    device = testbed.devices[device]
    device.connect(log_stdout=True)

    print("Applying configuration: ")
    print("\n".join(config))
    device.configure(config)
