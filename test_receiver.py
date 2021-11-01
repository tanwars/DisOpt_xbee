from digi.xbee.devices import XBeeDevice, DigiMeshDevice, DiscoveryOptions, \
    NetworkDiscoveryStatus, NeighborDiscoveryMode, NetworkEventReason, \
    NetworkEventType
import time
import keyboard

PARAM_TOTAL_TIME = 1
PARAM_TIME_STEP = 0.2
PARAM_NODE_NUM = 0

def cb_network_modified(event_type, reason, node):
  print("  >>>> Network event:")
  print("         Type: %s (%d)" % (event_type.description, event_type.code))
  print("         Reason: %s (%d)" % (reason.description, reason.code))

  if not node:
    return
  print("         Node:")
  print("            %s" % node)

def data_receive_callback(xbee_message):
  print("From %s >> %s" % (xbee_message.remote_device.get_node_id(),
                            xbee_message.data.decode()))

def setup(device, node_id):
  
  device.open()
  
  # setup
  device.set_node_id(node_id)  # sets node ID
  device.set_pan_id(bytearray(b'\xca\xfe')) # sets network ID
  # checks that it is API mode
  assert device.get_parameter('AP')==bytearray(b'\x02'), 'mode is incorrect' 

  # setup receiver callback
  device.add_data_received_callback(data_receive_callback)

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

def main():
  
  device = DigiMeshDevice("/dev/ttyUSB0", 9600)

  try:
    setup(device, 'Node ' + str(PARAM_NODE_NUM))

    neighbors = set_network(device)

    print('*' * 20)
    print('*' * 20)
    print("Receiving data ...")

    while True:
      try:
        if keyboard.is_pressed('q'):
          print('Exited by keypress\n')
          break
        time.sleep(0.1)
      except:
        break

  finally:
    if device is not None and device.is_open():
      device.close()


if __name__ == '__main__':
  main()
