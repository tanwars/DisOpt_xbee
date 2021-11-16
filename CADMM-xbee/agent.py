import numpy as np
from cost import cost
from utils import get_random_A_b, cb_network_modified, convert_to_packets, \
    recombine_packets, get_num_packets, not_all_ones, get_A_b_from_file

from digi.xbee.devices import XBeeDevice, DigiMeshDevice, DiscoveryOptions, \
    NetworkDiscoveryStatus, NeighborDiscoveryMode, NetworkEventReason, \
    NetworkEventType
import time

class agent:

    def __init__(self, params):
        
        self.state_size = params['Xbee']['state_size']
        self.num_packets = get_num_packets(self.state_size)

        self.device = DigiMeshDevice(params['Xbee']['port'], 9600)
        
        # xbee
        self.setup_xbee(params)

        # cadmm
        # self.y = np.array(params['CADMM']['init_y'], dtype=float)
        self.init_y = [params['CADMM']['init_y_temp']] * self.state_size
        self.y = np.array(self.init_y, dtype=float)
        self.p = np.zeros_like(self.y)
        self.c = params['CADMM']['c']

        print(self.y)

        # cost
        # A,b = get_random_A_b(self.y.size)
        A,b = get_A_b_from_file((params['Xbee']['node_id'])[-1])
        cost_param = {'A': A, 'b' : b}
        self.cost = cost('Affine', cost_param)

        self.Jinv = np.linalg.inv(2 * A + 2 * self.c * self.degree * 
                                                        np.eye(self.y.size))

        # recording data
        self.all_y = [self.y] # store y
        self.all_p = [self.p] # store p
        self.step_num = 0
        self.avg_time = 0.0
    
    def __del__(self):
        if self.device is not None and self.device.is_open():
            self.device.close()

    def setup_xbee(self, params):
        self.device.open()
        # setup
        self.device.set_node_id(params['Xbee']['node_id'])  # sets node ID
        self.device.set_pan_id(bytearray(b'\xca\xfe')) # sets network ID
        # checks that it is API mode
        assert self.device.get_parameter('AP')==bytearray(b'\x01'), 'mode is incorrect' 
        self.device.flush_queues()
        self.device.set_sync_ops_timeout(params['Xbee']['timeout_sender'])
        self.PARAM_TIMEOUT = params['Xbee']['timeout_receiver']

        self.setup_network(params)
        self.device.add_data_received_callback(self.data_receive_callback)

    def setup_network(self, params):
        xnet = self.device.get_network()
        # xnet.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF,
        #                             DiscoveryOptions.APPEND_DD})
        xnet.set_discovery_options({DiscoveryOptions.APPEND_DD})
        xnet.set_discovery_timeout(3.2)
        xnet.add_network_modified_callback(cb_network_modified)
        xnet.start_discovery_process()
        while xnet.is_discovery_running():
            time.sleep(0.5)
        self.nodes = xnet.get_devices()

        self.neighbor_packet_arr = {}
        self.neighbors = {}
        for n in self.nodes:
            self.neighbor_packet_arr[n.get_node_id()] = []
            # self.neighbors[n.get_node_id()] = np.array(params['CADMM']['init_y'], dtype=float)
        
        self.degree = len(self.nodes)
        self.flag_received = {}

    def send_state(self):
        packets = convert_to_packets(self.y, 72)
        for node in self.nodes:
            for i in range(len(packets)):
                self.device.send_data(node, packets[i])

    def data_receive_callback(self, xbee_message):
        # append message to nodeid's list of packets
        # ts = time.time()
        remote_id = xbee_message.remote_device.get_node_id()
        print('got message from:', remote_id)
        # print(self.flag_received)
        self.neighbor_packet_arr[remote_id].append(xbee_message.data)
        # check if node ID messge list is len full 
        # if it is full: evaluate it, print reception and empty it
        if (len(self.neighbor_packet_arr[remote_id]) == self.num_packets):
            self.neighbors[remote_id] = recombine_packets(self.neighbor_packet_arr[remote_id])
            self.neighbor_packet_arr[remote_id] = []
            self.flag_received[remote_id] = 1
            
        
        # te = time.time()
        # print('time to entire reception:', te-ts)

    # def receive_state(self):
    #     for idx, node in enumerate(self.nodes):
    #         try:
    #             xbee_message = self.device.read_data_from(node, self.PARAM_TIMEOUT)
    #         except:
    #             print('Timeout because of no reception from', node.get_node_id())
    #             return False
    #         else:
    #             # TODO: decide on structure of neighbor object
    #             self.neighbors[idx] = np.frombuffer(xbee_message.data)
    #             return True

    def step(self):

        ts = time.time()
        self.send_state()
        # successful = self.receive_state()  
        te = time.time()
        
        # TODO: need some sort of synchronization here

        # time.sleep(1)
        # if not successful:
        if not_all_ones(self.flag_received, self.degree):
            # TODO: decide on behavior when no data received when no data received
            print('Did not step')
            return
        else:
            print(self.flag_received)
            for n in self.flag_received:
                self.flag_received[n] = 0
            print('Comm. time is:', te-ts)

            self.avg_time = (self.avg_time * self.step_num + te-ts)/(self.step_num + 1)
            print('Avg time is:', self.avg_time)
            print('Stepping in', self.device.get_node_id(), 'step', self.step_num)
        
        # print([self.neighbors[n] for n in self.neighbors])
        yjsum = np.sum(np.array([self.neighbors[n] for n in self.neighbors]), axis = 0)

        self.p += self.c * (self.degree * self.y - yjsum)

        rhs = self.c * (self.degree * self.y + yjsum) - self.p - self.cost.b
        self.y = self.Jinv @ rhs

        # reset the neighbor packets to nothing after done updating
        for n in self.nodes:
            self.neighbor_packet_arr[n] = []
            self.neighbors = {}

        # # recorder
        self.all_p.append(self.p)
        self.all_y.append(self.y)
        self.step_num += 1

        