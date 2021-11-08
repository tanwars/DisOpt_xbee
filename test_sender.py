from digi.xbee.devices import XBeeDevice, DigiMeshDevice, DiscoveryOptions, \
    NetworkDiscoveryStatus, NeighborDiscoveryMode, NetworkEventReason, \
    NetworkEventType
import time

import numpy as np
import pickle
import math

PARAM_TOTAL_TIME = 1
PARAM_TIME_STEP = 0.2
PARAM_NODE_NUM = 1

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
  assert device.get_parameter('AP')==bytearray(b'\x01'), 'mode is incorrect' 

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

# def communicate_send(message_string, device, nodes):
#   for node in nodes:
#     device.send_data(node, message_string)  

def convert_to_packets(data, size):
  
  # ti = pickle.dumps(data)
  ti = data.tobytes()
  len_ti = len(ti)

  packets = []
  num_packets = math.ceil(len_ti/size)
  for i in range(num_packets):
      if ((i+1) * size < len_ti):
          packets.append(ti[i * size : (i+1) * size])
  packets.append(ti[(num_packets - 1) * size :])
  return packets

def communicate_send(data, device, nodes):
  packets = convert_to_packets(data, 72)
  for node in nodes:
    for i in range(len(packets)):
      device.send_data(node, packets[i])

def main():
  
  device = DigiMeshDevice("/dev/ttyUSB1", 9600)

  try:
    setup(device, 'Node ' + str(PARAM_NODE_NUM))

    neighbors = set_network(device)

    print('*' * 20)
    print('*' * 20)
    input('Press enter to start sending data ...')

    i = 0

    k = 25
    myarray = np.array([1.2] * k)
    # myarray = np.random.randn(k)
    while(i<PARAM_TOTAL_TIME):
      # communicate_send("hello neighbors! my time is : " + str(i), device, neighbors)
      ts = time.time()
      communicate_send(myarray, device, neighbors)
      te = time.time()
      print('time taken to send:', te-ts)
      time.sleep(PARAM_TIME_STEP)
      i += PARAM_TIME_STEP

  finally:
    if device is not None and device.is_open():
      device.close()


if __name__ == '__main__':
  main()
