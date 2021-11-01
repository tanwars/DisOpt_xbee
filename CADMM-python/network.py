import numpy as np

class NetGraph:

    def __init__(self, N):
        self.A = np.eye(N)

        for i in range(N):
            self.A[i,i] = 0

    def set_A(self, A):
        self.A = np.copy(A)

    def get_neighbors(self, agents, i):
        idx_arr = np.nonzero(self.A[i,:])
        return [agents[j] for j in idx_arr[0]]        
        