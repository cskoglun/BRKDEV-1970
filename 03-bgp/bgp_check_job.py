# To run the job:
# pyats run job BGP_check_job.py --testbed-file <testbed_file.yaml> --liveview
# Description: This job file checks if all BGP neighbors are in the 'established' state
import os
from pyats.easypy import run

# All run() must be inside a main function
def main():
    print("main function is running")
    # Find the location of the script in relation to the job file
    pwd = os.path.dirname(__file__)
    bgp_tests = os.path.join(pwd, 'BGP_Neighbors_Established.py')
    # Execute the testscript
    run(testscript=bgp_tests)

