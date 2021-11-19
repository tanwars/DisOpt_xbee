import numpy as np
import matplotlib.pyplot as plt
import pickle

Ab0 = pickle.load( open( "node_cost0.p", "rb" ) )
Ab1 = pickle.load( open( "node_cost1.p", "rb" ) )
Ab2 = pickle.load( open( "node_cost2.p", "rb" ) )
all_p0 = pickle.load( open( "node0.p", "rb" ) )
all_p1 = pickle.load( open( "node1.p", "rb" ) )
all_p2 = pickle.load( open( "node2.p", "rb" ) )

## central optima
total_A = Ab0[0] + Ab1[0] + Ab2[0]
total_b = Ab0[1] + Ab1[1] + Ab2[1]

# print(total_A)

central_p = -0.5 * (np.linalg.inv(total_A) @ total_b)

## cost computation
cost0 = np.zeros((len(all_p0),))
cost1 = np.zeros((len(all_p1),))
cost2 = np.zeros((len(all_p2),))

for i in range(len(all_p0)):
    cost0[i] = (all_p0[i]).T @ Ab0[0] @ all_p0[i] + (Ab0[1]).T @ all_p0[i]
for i in range(len(all_p1)):
    cost1[i] = all_p1[i].T @ Ab1[0] @ all_p1[i] + Ab1[1].T @ all_p1[i]
for i in range(len(all_p2)):
    cost2[i] = all_p2[i].T @ Ab2[0] @ all_p2[i] + Ab2[1].T @ all_p2[i]

## error computation
err0 = np.linalg.norm(np.array(all_p0) - central_p, axis = 1 )
err1 = np.linalg.norm(np.array(all_p1) - central_p, axis = 1 )
err2 = np.linalg.norm(np.array(all_p2) - central_p, axis = 1 )

## plotting
lens = [len(all_p0), len(all_p1), len(all_p2)]
iteration = [i for i in range(min(lens))]

print(lens)

plt.figure(1)
plt.plot(
    iteration, [err0[i] for i in range(len(iteration))], 'm',
    iteration, [err1[i] for i in range(len(iteration))], 'y',
    iteration, [err2[i] for i in range(len(iteration))], 'r',
    )

plt.legend(['error0', 'error1', 'error2'])
plt.grid()

plt.figure(2)
plt.plot(
    iteration, [cost0[i] for i in range(len(iteration))], 'm',
    iteration, [cost1[i] for i in range(len(iteration))], 'y',
    iteration, [cost2[i] for i in range(len(iteration))], 'r',
    )

plt.legend(['cost0', 'cost1', 'cost2'])
plt.grid()

plt.show()



# Ab0 = pickle.load( open( "node_cost0.p", "rb" ) )
# Ab1 = pickle.load( open( "node_cost1.p", "rb" ) )
# all_p0 = pickle.load( open( "node0.p", "rb" ) )
# all_p1 = pickle.load( open( "node1.p", "rb" ) )

# ## central optima
# total_A = Ab0[0] + Ab1[0]
# total_b = Ab0[1] + Ab1[1]

# # print(total_A)

# central_p = -0.5 * (np.linalg.inv(total_A) @ total_b)

# ## cost computation
# cost0 = np.zeros((len(all_p0),))
# cost1 = np.zeros((len(all_p1),))

# for i in range(len(all_p0)):
#     cost0[i] = (all_p0[i]).T @ Ab0[0] @ all_p0[i] + (Ab0[1]).T @ all_p0[i]
# for i in range(len(all_p1)):
#     cost1[i] = all_p1[i].T @ Ab1[0] @ all_p1[i] + Ab1[1].T @ all_p1[i]

# ## error computation
# err0 = np.linalg.norm(np.array(all_p0) - central_p, axis = 1 )
# err1 = np.linalg.norm(np.array(all_p1) - central_p, axis = 1 )

# ## plotting
# lens = [len(all_p0), len(all_p1)]
# iteration = [i for i in range(min(lens))]

# print(lens)

# plt.figure(1)
# plt.plot(
#     iteration, [err0[i] for i in range(len(iteration))], 'm',
#     iteration, [err1[i] for i in range(len(iteration))], 'y',
#     )

# plt.legend(['error0', 'error1'])
# plt.grid()

# plt.figure(2)
# plt.plot(
#     iteration, [cost0[i] for i in range(len(iteration))], 'm',
#     iteration, [cost1[i] for i in range(len(iteration))], 'y',
#     )

# plt.legend(['cost0', 'cost1'])
# plt.grid()

# plt.show()

