import numpy as np

class agent:

    def __init__(self, init_y, cost, c):
        
        self.y = init_y
        self.p = np.zeros(init_y.size)
        self.cost = cost
        self.c = c
        self.all_y = [init_y] # store y
        self.all_p = [self.p] # store p
    
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors.copy()
        self.degree = len(self.neighbors)

    def minimizer(self, p_k):
        # depends on cost

        A = self.cost.A
        b = self.cost.b

        yjsum = np.sum(np.array([n.y for n in self.neighbors]), axis = 0)
        Jinv = np.linalg.inv(2 * A + 2 * self.c * self.degree * 
                                                        np.eye(self.y.size))


        rhs = self.c * (self.degree * self.y + yjsum) - self.p - b
        
        y_k = Jinv @ rhs

        return y_k

    def step(self):

        yjsum = np.sum(np.array([n.y for n in self.neighbors]), axis = 0)

        self.p += 2 * self.c * (self.degree * self.y - yjsum)

        # print(self.p)

        self.next_y = self.minimizer(self.p)

        # # recorder
        self.all_p.append(self.p)
        self.all_y.append(self.next_y)
        
    def update_state(self):
        self.y = np.copy(self.next_y)
    