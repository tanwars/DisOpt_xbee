import numpy as np
import math
import pickle

k = 9
a = [1.1] * k
b = np.array(a).tobytes()

c = np.array(a)
# print(type(c))

# print(len(b))

val = 20
val2 = 30
d = b + val.to_bytes(1, 'big') + val2.to_bytes(1, 'big')

# print(len(d))

k = 8
myarray = np.array([1.2] * k)
# ti = pickle.dumps(myarray)
ti = myarray.tobytes()
num_packets = math.ceil(len(ti)/72)

# print(num_packets)

# print(np.frombuffer(d[:160]))
# print(int.from_bytes(d[160:], 'big'))

def convert_to_packets(input, size):
    ### converts a given np array into packets of size 72 each

    assert isinstance(input, np.ndarray), 'input should be array'
    ti = input.tobytes()
    len_ti = len(ti)

    print(len_ti)
    packets = []
    num_packets = math.ceil(len_ti/size)
    for i in range(num_packets):
        if ((i+1) * size < len_ti):
            packets.append(ti[i * size : (i+1) * size])
    packets.append(ti[(num_packets - 1) * size :])
    return packets

def recombine_packets(packets):
    ### converts a packet list into a single numpy array

    # ti = packets[0]
    # tj = ti.join(packets[1:])
    tj = b''.join(packets)
    print(np.frombuffer(tj))
    print(np.frombuffer(tj).shape)

packs = convert_to_packets(myarray,72)

recombine_packets(packs)

print(len(packs))


at = {}

for i in range(10):
    at[i] = 10

yjsum = np.sum(np.array([at[n] for n in at]), axis = 0)

# print(np.array([at[n] for n in at]))