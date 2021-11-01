from cadmm import agent as ag
import numpy as np
from cost import cost

def get_random_A_b(N):
    a_ns = np.random.rand(N,N)
    A = ((a_ns + a_ns.T) / 2)
    b = np.random.rand(N)
    return A,b

init_y1 = np.array([1,2])
init_y2 = np.array([0,0])
A = np.array([[2,1],[1,2]])
b = np.ones(2)

c = cost()

params = {'A': A, 'b' : b}
c.set_cost('Affine', params)

ag1 = ag(init_y1,c,1)
ag2 = ag(init_y1,c,1)
ag3 = ag(init_y2,c,1)
ag4 = ag(init_y2,c,1)

ag1.set_neighbors([ag2, ag3, ag4])
ag2.set_neighbors([ag1, ag3, ag4])
ag3.set_neighbors([ag2, ag1, ag4])
ag4.set_neighbors([ag2, ag3, ag1])


for k in range (2):
    ag1.step()
    ag2.step()
    ag3.step()
    ag4.step()

    ag1.update_state()
    ag2.update_state()
    ag3.update_state()
    ag4.update_state()

print(2 % 4)