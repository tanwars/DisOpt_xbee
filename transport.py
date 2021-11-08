import math
import numpy as np
import pickle

class message:
  def __init__(self, **kwargs):
    self.data = kwargs['data']
    self.step_num = kwargs['step']
    self.node_id = kwargs['node_id']

class transporter:

  def __init__(self, **kwargs):
    if 'message' in kwargs:
      self.message = kwargs['message']

  def convert_to_packets(self, size):
    ### converts a given np array into packets of size size each

    assert isinstance(self.data, np.ndarray), 'input should be array'
    ti = pickle.dumps(self.message)
    len_ti = len(ti)

    self.packets = []
    num_packets = math.ceil(len_ti/size)
    for i in range(num_packets):
        if ((i+1) * size < len_ti):
            self.packets.append(ti[i * size : (i+1) * size])
    self.packets.append(ti[(num_packets - 1) * size :])
    return num_packets

  def send_data(self, device, node):
    for i in range(len(self.packets)):
      device.send_data(node, self.packets[i])

  def recombine_packets(self, packets):
    ### converts a packet list into a single numpy array
    ti = packets[0]
    tj = ti.join(packets[1:])
    self.message = pickle.loads(tj)