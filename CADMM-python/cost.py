class cost:
    def __init__(self):
        return

    def set_cost(self,keyword,params):
        if keyword == 'Affine':
            self.A = params['A']
            self.b = params['b']
