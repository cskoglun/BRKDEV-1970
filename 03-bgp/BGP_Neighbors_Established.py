#!/bin/env python
import logging
import json

from tabulate import tabulate

from pyats import aetest
from pyats.log.utils import banner

from genie.conf import Genie
from genie.abstract import Lookup

from genie.libs import ops # noqa

# Get your logger for your script
log = logging.getLogger(__name__)

class common_setup(aetest.CommonSetup):
    #print("this works")
    """ Common Setup section """
    @aetest.subsection
    def connect(self, testbed):
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            if not device.name.startswith("csr1000v"):
                continue

            try:
                device.connect(log_stdout=False)
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)

class BGP_Neighbors_Established(aetest.Testcase):
    @ aetest.test
    def learn_bgp(self):
        self.all_bgp_sessions = {}
        for dev in self.parent.parameters['dev']:

            log.info(banner("Gathering BGP Information from {}".format(
                dev.name)))
            abstract = Lookup.from_device(dev)
            bgp = abstract.ops.bgp.bgp.Bgp(dev)
            bgp.learn()
            self.all_bgp_sessions[dev.name] = bgp.info

    @ aetest.test
    def check_bgp(self):
        failed_dict = {}
        mega_tabular = []
        for device, bgp in self.all_bgp_sessions.items():
            # may need to change based on BGP config
            default = bgp['instance']['default']['vrf']['default']
            neighbors = default['neighbor']
            for nbr, props in neighbors.items():
                state = props.get('session_state')
                if state:
                    tr = []
                    tr.append(device)
                    tr.append(nbr)
                    tr.append(state)
                    if state == 'established' or state == 'Established':
                        tr.append('Passed')
                    else:
                        failed_dict[device] = {}
                        failed_dict[device][nbr] = props
                        tr.append('Failed')

                mega_tabular.append(tr)

        log.info(tabulate(mega_tabular,
                          headers=['Device', 'Peer',
                                   'State', 'Pass/Fail'],
                          tablefmt='orgtbl'))

        if failed_dict:
            log.error(json.dumps(failed_dict, indent=3))
            self.failed("Testbed has BGP Neighbors that are not established")

        else:
            self.passed("All BGP Neighbors are established")

class common_cleanup(aetest.CommonCleanup):
    @aetest.subsection
    def clean_everything(self):
        for dev in self.parent.parameters['dev']:
            dev.disconnect()

if __name__ == '__main__':  # pragma: no cover
    aetest.main()
