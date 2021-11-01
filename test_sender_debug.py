from digi.xbee.devices import XBeeDevice, DigiMeshDevice, DiscoveryOptions, \
    NetworkDiscoveryStatus, NeighborDiscoveryMode, NetworkEventReason, \
    NetworkEventType
import time

import numpy as np
import pickle
import codecs

PARAM_TOTAL_TIME = 1
PARAM_TIME_STEP = 0.2
PARAM_NODE_NUM = 1

class A:

    def __init__(self):
        self.a = np.array([1,2,3])
        self.b = np.array([2,3,4])
        self.c = 10
        self.d = 'hello'

def cb_network_modified(event_type, reason, node):
  print("  >>>> Network event:")
  print("         Type: %s (%d)" % (event_type.description, event_type.code))
  print("         Reason: %s (%d)" % (reason.description, reason.code))

  if not node:
    return
  print("         Node:")
  print("            %s" % node)

def setup(device, node_id):
  
  device.open()
  
  # setup
  device.set_node_id(node_id)  # sets node ID
  device.set_pan_id(bytearray(b'\xca\xfe')) # sets network ID
  # checks that it is API mode
  assert device.get_parameter('AP')==bytearray(b'\x02'), 'mode is incorrect' 
  # device.set_sync_ops_timeout(100)

def set_network(device):
  # get network objects
  xnet = device.get_network()
  xnet.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF,
                              DiscoveryOptions.APPEND_DD})
  xnet.set_discovery_timeout(3.2)
  xnet.add_network_modified_callback(cb_network_modified)
  xnet.start_discovery_process()
  while xnet.is_discovery_running():
      time.sleep(0.5)

  nodes = xnet.get_devices()
  return(nodes)

def communicate_send(message_string, device, nodes):
  for node in nodes:
    # a = np.array([1.0,2.0,3.0], dtype=float)
    a = np.array([10, 10])
    # c = a.tobytes()
    # a = A()
    # device.send_data(node, message_string)  
    b = codecs.encode(pickle.dumps(a), "base64").decode()
    print(type(b))
    device.send_data(node, 'hello')

def main():
  
  device = DigiMeshDevice("/dev/ttyUSB1", 9600)

  try:
    setup(device, 'Node ' + str(PARAM_NODE_NUM))

    neighbors = set_network(device)

    print('*' * 20)
    print('*' * 20)
    input('Press enter to start sending data ...')

    i = 0
    while(i<PARAM_TOTAL_TIME):
      communicate_send("hello neighbors! my time is : " + str(i), device, neighbors)
      time.sleep(PARAM_TIME_STEP)
      i += PARAM_TIME_STEP

  finally:
    if device is not None and device.is_open():
      device.close()


if __name__ == '__main__':
  main()
