import numpy as np
from cost import cost
from utils import get_random_A_b

from digi.xbee.devices import XBeeDevice, DigiMeshDevice, DiscoveryOptions, \
    NetworkDiscoveryStatus, NeighborDiscoveryMode, NetworkEventReason, \
    NetworkEventType
import time

def cb_network_modified(event_type, reason, node):
    print("  >>>> Network event:")
    print("         Type: %s (%d)" % (event_type.description, event_type.code))
    print("         Reason: %s (%d)" % (reason.description, reason.code))

    if not node:
        return
    print("         Node:")
    print("            %s" % node)

class agent:

    def __init__(self, params):
        
        self.device = DigiMeshDevice(params['Xbee']['port'], 9600)
        
        # xbee
        self.setup_xbee(params)
        self.setup_network(params)

        # cadmm
        # self.y = np.array(params['CADMM']['init_y'], dtype=float)
        self.init_y = [params['CADMM']['init_y_temp']] * params['CADMM']['init_y_n_temp']
        self.y = np.array(self.init_y, dtype=float)
        self.p = np.zeros_like(self.y)
        self.c = params['CADMM']['c']

        print(self.y)

        # TODO intialize neibhbors
        self.neighbors = [np.array(self.init_y)] * len(self.nodes)
        self.degree = len(self.neighbors)

        # cost
        A,b = get_random_A_b(self.y.size)
        cost_param = {'A': A, 'b' : b}
        self.cost = cost('Affine', cost_param)
        
        # recording data
        self.all_y = [self.y] # store y
        self.all_p = [self.p] # store p
        self.step_num = 0
    
    def __del__(self):
        if self.device is not None and self.device.is_open():
            self.device.close()

    def setup_xbee(self, params):
        self.device.open()
        # setup
        self.device.set_node_id(params['Xbee']['node_id'])  # sets node ID
        self.device.set_pan_id(bytearray(b'\xca\xfe')) # sets network ID
        # checks that it is API mode
        assert self.device.get_parameter('AP')==bytearray(b'\x02'), 'mode is incorrect' 
        self.device.flush_queues()
        self.device.set_sync_ops_timeout(params['Xbee']['timeout_sender'])
        self.PARAM_TIMEOUT = params['Xbee']['timeout_receiver']

    def setup_network(self, params):
        xnet = self.device.get_network()
        xnet.set_discovery_options({DiscoveryOptions.DISCOVER_MYSELF,
                                    DiscoveryOptions.APPEND_DD})
        xnet.set_discovery_timeout(3.2)
        xnet.add_network_modified_callback(cb_network_modified)
        xnet.start_discovery_process()
        while xnet.is_discovery_running():
            time.sleep(0.5)
        self.nodes = xnet.get_devices()

    def send_state(self):
        message = self.y.tobytes()  # TODO: may need to change this
        for node in self.nodes:
            self.device.send_data(node, message)
            # TODO: should check message type

    def receive_state(self):
        for idx, node in enumerate(self.nodes):
            try:
                xbee_message = self.device.read_data_from(node, self.PARAM_TIMEOUT)
            except:
                print('Timeout because of no reception from', node.get_node_id())
                return False
            else:
                # TODO: decide on structure of neighbor object
                self.neighbors[idx] = np.frombuffer(xbee_message.data)
                return True

    def minimizer(self, p_k):
        # depends on cost

        A = self.cost.A
        b = self.cost.b

        yjsum = np.sum(np.array([n for n in self.neighbors]), axis = 0)
        Jinv = np.linalg.inv(2 * A + 2 * self.c * self.degree * 
                                                        np.eye(self.y.size))


        rhs = self.c * (self.degree * self.y + yjsum) - self.p - b
        
        y_k = Jinv @ rhs

        return y_k

    def step(self):

        ts = time.time()
        self.send_state()
        successful = self.receive_state()  
        te = time.time()

        if not successful:
            # TODO: decide on behavior when no data received when no data received
            print('Did not step')
            return
        else:
            print('Comm. time is:', te-ts)
            print('Stepping in', self.device.get_node_id(), 'step', self.step_num)
        
        yjsum = np.sum(np.array([n for n in self.neighbors]), axis = 0)

        self.p += self.c * (self.degree * self.y - yjsum)

        self.y = self.minimizer(self.p)

        # # recorder
        self.all_p.append(self.p)
        self.all_y.append(self.y)
        self.step_num += 1

        