import pickle
import codecs

import numpy as np

# a = 10

# b = bytearray(a)

# print(b)

# c = pickle.dumps(a)

# a_dash = pickle.loads(c)

# print(a_dash)

# b = [2,2,3,4]


# a = np.array([1,2,3])
# c = bytearray(pickle.dumps(a))

# a_dash = pickle.loads(c)

# # print(c)
# print(a_dash)
# print(type(a_dash))


class A:

    def __init__(self):
        self.a = np.array([1,2,3])
        self.b = np.array([2,3,4])
        self.c = 10
        self.d = 'hello'

a = A()

# c = bytes(a)

a = [10,10]
b = np.array([10,10])

pickled = codecs.encode(pickle.dumps(a), "base64").decode()

print(type(pickled))

unpickled = pickle.loads(codecs.decode(pickled.encode(), "base64"))

print(unpickled)



# a = [np.array([1,2,3])] * 10

# for i in a:
#     print(i)