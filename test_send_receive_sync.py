from digi.xbee.devices import XBeeDevice, DigiMeshDevice, DiscoveryOptions, \
    NetworkDiscoveryStatus, NeighborDiscoveryMode, NetworkEventReason, \
    NetworkEventType
import time
import keyboard
import sys
import numpy as np

PARAM_NODE_NUM = sys.argv[1]
PARAM_TIMEOUT_WAIT = 0.2
PARAM_LOOP_RATE = 0.1

def cb_network_modified(event_type, reason, node):
  print("  >>>> Network event:")
  print("         Type: %s (%d)" % (event_type.description, event_type.code))
  print("         Reason: %s (%d)" % (reason.description, reason.code))

  if not node:
    return
  print("         Node:")
  print("            %s" % node)

# def data_receive_callback(xbee_message):
#   print("From %s >> %s" % (xbee_message.remote_device.get_node_id(),
#                             xbee_message.data.decode()))

def setup(device, node_id):
  
  device.open()
  
  # setup
  device.set_node_id(node_id)  # sets node ID
  device.set_pan_id(bytearray(b'\xca\xfe')) # sets network ID
  # checks that it is API mode
  assert device.get_parameter('AP')==bytearray(b'\x01'), 'mode is incorrect' 

  device.flush_queues()
  # setup receiver callback
  # device.add_data_received_callback(data_receive_callback)

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

def data_receive(device, nodes):
  for node in nodes:
    try:
      xbee_message = device.read_data_from(node, PARAM_TIMEOUT_WAIT)
    except:
      print('Timeout because of no reception from', node.get_node_id())
    else:
      # print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
      #                       xbee_message.data.decode()))
      print('received data')

def data_send(message_string, device, nodes):
  for node in nodes:
    # device.send_data(node, message_string)
    k = 9
    a = [1.1] * k
    b = np.array(a).tobytes()
    device.send_data(node, b)

def main():
  
  print("/dev/ttyUSB" + str(sys.argv[1]))
  device = DigiMeshDevice("/dev/ttyUSB" + str(sys.argv[1]), 9600)

  try:
    setup(device, 'Node ' + str(PARAM_NODE_NUM))

    neighbors = set_network(device)

    print('*' * 20)
    print('*' * 20)
    print("Ready to send and receive data ...")
    input('Press enter to start')

    i = 0
    k = 4
    while True:
      try:
        ts = time.time()
        for i in range(k):
          data_send("hello neighbors! Synced at idx: " + str(i) + " : " + str(device.get_node_id()),
                       device, neighbors)
          data_receive(device, neighbors)
        te = time.time()
        print('time taken:', te-ts)
        if keyboard.is_pressed('q'):
          print('Exited by keypress\n')
          break
        time.sleep(PARAM_LOOP_RATE)
        i += 1
      except:
        break

  finally:
    if device is not None and device.is_open():
      print('Closing device')
      device.close()


if __name__ == '__main__':
  main()
