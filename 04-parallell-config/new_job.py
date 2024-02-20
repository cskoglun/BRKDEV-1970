'''
This code leverages the REDIS server and RQ workder in order to put jobs into the queue.
'''
from redis import Redis
from rq import Queue

from genie.testbed import load

from job_tasks import apply_configuration

configuration = [
    "snmp-server community private RW"
]

testbed = load('testbed-sandbox.yaml')
queue = Queue(connection=Redis('localhost', port=6379))
for name, device in testbed.devices.items():
    queue.enqueue(apply_configuration,testbed="testbed-sandbox.yaml",device=name, config=configuration)