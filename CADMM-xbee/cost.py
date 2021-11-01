class cost:
    
    def __init__(self,keyword,params):
        if keyword == 'Affine':
            self.A = params['A']
            self.b = params['b']
