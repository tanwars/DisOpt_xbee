from digi.xbee.devices import XBeeDevice, DigiMeshDevice

from digi.xbee.devices import DiscoveryOptions, NetworkDiscoveryStatus, NeighborDiscoveryMode, NetworkEventReason, NetworkEventType

import time 

def callback(remote):
    print('dicovered new node: ', remote.get_node_id())

def fin_callback(status):
    if status == NetworkDiscoveryStatus.ERROR_READ_TIMEOUT:
        print('some error')
    else:
        print('discovery ended successfully')

def cb_network_modified(event_type, reason, node):
  print("  >>>> Network event:")
  print("         Type: %s (%d)" % (event_type.description, event_type.code))
  print("         Reason: %s (%d)" % (reason.description, reason.code))

  if not node:
    return

  print("         Node:")
  print("            %s" % node)

device = DigiMeshDevice("/dev/ttyUSB1", 9600)

device.open()

# do something
xnet = device.get_network()

## set discovery parameters

xnet.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF,
                            DiscoveryOptions.APPEND_DD})

xnet.set_discovery_timeout(3.2)

# callback everytime a new node is found (may be redundant because of modified callback)(may be useful to setup this new node)
xnet.add_device_discovered_callback(callback)

xnet.add_discovery_process_finished_callback(fin_callback) # callback at the finish of the discovery process
xnet.add_network_modified_callback(cb_network_modified) # callback if there is modification to net

## discover nodes

xnet.start_discovery_process()

while xnet.is_discovery_running():
    time.sleep(0.5)

nodes = xnet.get_devices() # list of nodes discovered (does not include self)
spec_node = xnet.get_device_by_node_id('Node 2') # gets a specific node with ID

for i in range(len(nodes)):
    print(nodes[i].get_node_id())

## to discover a single node

# remote = xnet.discover_device("Node 2")
# print('dicovered new node: ', remote.get_node_id())

## deep discovery - does not work for whatever reason

# xnet.set_deep_discovery_options(deep_mode=NeighborDiscoveryMode.CASCADE,
#                                 del_not_discovered_nodes_in_last_scan=False)

# xnet.set_deep_discovery_timeouts(node_timeout=10, time_bw_requests=10,
#                                 time_bw_scans=20)


# xnet.start_discovery_process(deep=True, n_deep_scans=1)
# while xnet.is_discovery_running():
#     time.sleep(0.5)

# print("%s" % '\n'.join(map(str, xnet.get_connections())))

device.close()