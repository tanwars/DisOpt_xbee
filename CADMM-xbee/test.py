from cadmm import agent
from cost import cost
from network import NetGraph
import numpy as np
import matplotlib.pyplot as plt

def get_random_A_b(n):
    a_ns = np.random.rand(n,n)
    A = ((a_ns + a_ns.T) / 2)
    A = A @ A.T
    b = np.random.rand(n)
    return A,b

def get_random_adjacency_mat(N):
    a_ns = np.random.randint(2,size=(N,N))
    A = 1 * (((a_ns + a_ns.T) / 2) > 0 )
    # A = np.ones((N,N))

    for i in range(N):
        A[i,i] = 0
    return A

## params

N = 10 # number of agents
d = 2 # dimension of y
c = 1 # param in net
init_y = np.random.rand(d,N)

num_iter = 100
k = 2 # how often to change graph

## initialize costs

all_costs = [cost()] * N
for i in range(N):
    # A,b = get_random_A_b(d)
    A = np.array([[3,1],[1,3]])
    b = np.ones(2)
    params = {'A': A, 'b' : b}
    all_costs[i].set_cost('Affine', params)

## intialize agents

all_agents = [agent(init_y[:,i], all_costs[i], c) for i in range(N)]

## intitalize the graph

# get a randon Adjacency matrix
A = get_random_adjacency_mat(N)
print(A)

G = NetGraph(N)
G.set_A(A)

# set neighbors
# for i in range(N):
    

# main loop
for t in range(num_iter):

    if t % k == 0:
        A = get_random_adjacency_mat(N)
        G.set_A(A)
    
    for i in range(N):

        # random connectivity at each kth step

        neighbors = G.get_neighbors(all_agents,i)
        all_agents[i].set_neighbors(neighbors)
        all_agents[i].step()

    for i in range(N):
        all_agents[i].update_state()

## central optima
total_A = np.zeros((d,d))
total_b = np.zeros(d)
for i in range(N):
    total_A += all_costs[i].A
    total_b += all_costs[i].b

central_y = -0.5 * (np.linalg.inv(total_A) @ total_b)

## plotting

iteration = [i for i in range(len(all_agents[0].all_y))]

plt.plot(iteration, [central_y[0]] * len(iteration), 'r--', \
    iteration, [all_agents[0].all_y[i][0] for i in range(len(iteration))], 'b',
    iteration, [all_agents[1].all_y[i][0] for i in range(len(iteration))], 'g')
plt.show()
