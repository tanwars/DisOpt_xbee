import numpy as np
import math
import scipy.io as sio

def get_random_A_b(n):
    a_ns = np.random.rand(n,n)
    A = ((a_ns + a_ns.T) / 2)
    A = A @ A.T + np.eye(n)
    b = np.random.rand(n)
    return A,b

def get_random_adjacency_mat(N):
    a_ns = np.random.randint(2,size=(N,N))
    A = 1 * (((a_ns + a_ns.T) / 2) > 0 )
    # A = np.ones((N,N))

    for i in range(N):
        A[i,i] = 0
    return A

def get_A_b_from_file(node_num):
    mat = sio.loadmat("data/robot0%s_data.mat" % node_num) 
    GtQG = mat['GtQG']
    GtQz = mat['GtQz']
    # ztQz = mat['ztQz']
    # pinvH = mat['pinvH']
    # G = mat['G']
    # z = mat['z']
    A = GtQG
    b = 2 * GtQz
    b = np.reshape(b, (b.shape[0],))
    return A,b

def cb_network_modified(event_type, reason, node):
    print("  >>>> Network event:")
    print("         Type: %s (%d)" % (event_type.description, event_type.code))
    print("         Reason: %s (%d)" % (reason.description, reason.code))

    if not node:
        return
    print("         Node:")
    print("            %s" % node)

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

def recombine_packets(packets):
  tj = b''.join(packets)
  # return pickle.loads(tj)
  return np.frombuffer(tj)

def get_num_packets(n):
    return math.ceil(len(np.random.randn(n).tobytes())/72)

def not_all_ones(flags, degree):
    if not flags:
        return True
    if len(flags) != degree:
        return True
    for n in flags:
        if flags[n] != 1:
            return True
    return False

def set_all_zeros(flags):
    for n in flags:
        flags[n] = 0

def on_same_step(step_nums, s):
    arr = [step_nums[i] == s for i in step_nums]
    return all(i == True for i in arr)

def on_low_step(step_nums, s):
    arr = [step_nums[i] >= s for i in step_nums]
    return all(i == True for i in arr)