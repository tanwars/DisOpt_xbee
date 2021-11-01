import numpy as np
import matplotlib.pyplot as plt
import pickle

d = 2

Ab0 = pickle.load( open( "node_cost0.p", "rb" ) )
Ab1 = pickle.load( open( "node_cost1.p", "rb" ) )
all_y0 = pickle.load( open( "node0.p", "rb" ) )
all_y1 = pickle.load( open( "node1.p", "rb" ) )

## central optima
total_A = Ab0[0] + Ab1[0]
total_b = Ab0[1] + Ab1[1]


# central_y = -0.5 * (np.linalg.inv(total_A) @ total_b)
central_y = -(np.linalg.inv(total_A) @ total_b)

## plotting

assert len(all_y0) == len(all_y1), 'length mismatch'
iteration = [i for i in range(len(all_y0))]

# plt.plot(iteration, [central_y[0]] * len(iteration), 'r--', \
#     iteration, [all_y0[i][0] for i in range(len(iteration))], 'b',
#     iteration, [all_y1[i][0] for i in range(len(iteration))], 'g',
#     iteration, [central_y[1]] * len(iteration), 'c--', \
#     iteration, [all_y0[i][1] for i in range(len(iteration))], 'm',
#     iteration, [all_y1[i][1] for i in range(len(iteration))], 'y'
#     )

plt.plot(
    iteration, [all_y0[i][0] for i in range(len(iteration))], 'b',
    iteration, [all_y1[i][0] for i in range(len(iteration))], 'g',
    iteration, [all_y0[i][3] for i in range(len(iteration))], 'c',
    iteration, [all_y1[i][3] for i in range(len(iteration))], 'k',
    iteration, [all_y0[i][7] for i in range(len(iteration))], 'm',
    iteration, [all_y1[i][7] for i in range(len(iteration))], 'y'
    )

plt.legend(['node0_0', 'node1_0','node0_3', 'node1_3','node0_7', 'node1_7'])

plt.show()
