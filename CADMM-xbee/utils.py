import numpy as np

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
