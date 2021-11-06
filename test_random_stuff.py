import numpy as np
import math

k = 20
a = [1.1] * k
b = np.array(a).tobytes()

c = np.array(a)
print(type(c))

print(len(b))

def convert_to_packets(input, size):
    ### converts a given np array into packets of size 72 each

    assert isinstance(input, np.ndarray), 'input should be array'
    ti = input.tobytes()
    len_ti = len(ti)

    packets = []
    num_packets = math.ceil(len_ti/size)
    for i in range(num_packets):
        if ((i+1) * size < len_ti):
            packets.append(ti[i * size : (i+1) * size])
    packets.append(ti[(num_packets - 1) * size :])
    return packets

def recombine_packets(packets):
    ### converts a packet list into a single numpy array

    ti = packets[0]
    tj = ti.join(packets[1:])
    print(np.frombuffer(tj).shape)

packs = convert_to_packets(c,72)
recombine_packets(packs)

