from digi.xbee.devices import XBeeDevice, DigiMeshDevice
import sys

# device = XBeeDevice("/dev/ttyUSB0", 9600)

# device = DigiMeshDevice("/dev/ttyUSB1", 9600)
node = str(sys.argv[1])

device = DigiMeshDevice("/dev/ttyUSB" + node, 9600)

device.open()
# device2.open() 

# if device is open, I cannot see on console if it received
# a message or not. Need to figure out how to check this in code.

# device.refresh_device_info() #no def for this

# device.send_data_broadcast("Hello XBee World!")


print(device.get_64bit_addr()) # to get unique ID of device
print(device.get_protocol())
print(device.get_pan_id())
print(device.get_node_id()) 
print(device.get_parameter('AP'))

print(device.get_dest_address()) # might be useful if want to have a single connection??

##################
# all we need to worry about params
##################

device.set_node_id('Node ' + node)  # sets the node id

# sets the network id (make sure all on one net)
device.set_pan_id(bytearray(b'\xca\xfe'))

# sets it in API mode
device.set_parameter('AP',bytearray(b'\x02'))


##################


device.close()


device.open()

print('\r\r Opened again \r\r')
print(device.get_64bit_addr()) # to get unique ID of device
print(device.get_protocol())
print(device.get_pan_id())
print(device.get_node_id()) 
print(device.get_parameter('AP'))

device.send_data_broadcast("Hello XBee World!")

device.close()

# id2 = device2.get_64bit_addr()
# print(id2)
# device2.close()

