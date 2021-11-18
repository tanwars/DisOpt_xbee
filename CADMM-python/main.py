from cadmm import agent
from cost import cost
from network import NetGraph
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio

def get_random_A_b(n):
    a_ns = np.random.rand(n,n)
    A = ((a_ns + a_ns.T) / 2)
    A = A @ A.T + np.eye(n) * 10
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
## params

N = 3 # number of agents
d = 8 # dimension of y
c = 5 # param in net
init_y = np.random.rand(d,N)

num_iter = 100
k = 1000 # how often to change graph

## initialize costs

# all_costs = [cost()] * N
# for i in range(N):
#     A,b = get_random_A_b(d)
#     # A = np.array([[3,1],[1,3]])
#     # b = np.ones(2)
#     params = {'A': A, 'b' : b}
#     all_costs[i].set_cost('Affine', params)
A0,b0 = get_A_b_from_file(0)
params0 = {'A': A0, 'b' : b0}
cost0 = cost()
cost0.set_cost('Affine', params0)
# all_costs[0].set_cost('Affine', params0)
# print(A0)

A1,b1 = get_A_b_from_file(1)
params1 = {'A': A1, 'b' : b1}
cost1 = cost()
cost1.set_cost('Affine', params1)
# all_costs[1].set_cost('Affine', params1)
# print(A1)

A2,b2 = get_A_b_from_file(2)
params2 = {'A': A2, 'b' : b2}
cost2 = cost()
cost2.set_cost('Affine', params2)
# all_costs[2].set_cost('Affine', params2)
# print(A2)

all_costs = [cost0, cost1, cost2]

## intialize agents

all_agents = [agent(init_y[:,i], all_costs[i], c) for i in range(N)]

## intitalize the graph

# get a randon Adjacency matrix
# A = get_random_adjacency_mat(N)
# print(A)
Adj = np.ones((N,N))

G = NetGraph(N)
G.set_A(Adj)

# set neighbors
# for i in range(N):
    

# main loop
for t in range(num_iter):

    # if t % k == 0:
    #     A = get_random_adjacency_mat(N)
    #     G.set_A(A)
    
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

# print(total_A)
central_y = -0.5 * (np.linalg.inv(total_A) @ total_b)

## plotting

iteration = [i for i in range(len(all_agents[0].all_y))]

all_p_sum = np.zeros((d,))
for i in range(N):
    all_p_sum += all_agents[0].all_p[-1]

print(all_p_sum)
# print(all_agents[0].all_p[-1])
# print(all_agents[1].all_p[-1])
# print(all_agents[2].all_p[-1])

print(np.linalg.norm(all_agents[0].all_y[-1] - central_y))

plt.figure(1)
plt.plot(iteration, [central_y[0]] * len(iteration), 'r--', \
    iteration, [all_agents[0].all_y[i][0] for i in range(len(iteration))], 'b',
    iteration, [all_agents[1].all_y[i][0] for i in range(len(iteration))], 'g')

plt.figure(2)
plt.plot(iteration, [np.linalg.norm(all_agents[0].all_y[i] - central_y) for i in range(len(iteration))], 'b',
    iteration, [np.linalg.norm(all_agents[1].all_y[i] - central_y) for i in range(len(iteration))], 'g',
    iteration, [np.linalg.norm(all_agents[2].all_y[i] - central_y) for i in range(len(iteration))], 'r')

plt.show()
