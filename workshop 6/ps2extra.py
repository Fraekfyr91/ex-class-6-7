import numpy as np
from types import SimpleNamespace
class ps2extraclass:

    def __init__(self):
        """ setup model """

        # a. create namespaces
        par = self.par = SimpleNamespace()
        # a. choose parameters
        par.N = 10000
        par.J = 5
        par.seed = 1986
        par.eps = 1e-8
        par.kappa = 0.2
        par.maxiter = 5000

        # b. choose Sigma
        # create a lower triangular matrix with ones on the diagonal
        par.Sigma_lower = np.tril(np.ones((par.J, par.J)))
        # generate random off-diagonal elements
        par.Sigma_lower[np.tril_indices(par.J, k=-1)] = np.random.uniform(low=-1, high=1, size=int(par.J*(par.J-1)/2))

        par.Sigma_upper = par.Sigma_lower.T
        par.Sigma = par.Sigma_upper@par.Sigma_lower

        # c. draw random numbers
        np.random.seed(par.seed)
        par.alphas = np.exp(np.random.multivariate_normal(np.zeros(par.J), par.Sigma, par.N))

        # d. normalize alphas to values between 0 and 1
        par.alpha_sum = par.alphas.sum(axis=1)
        par.alphas = par.alphas / par.alpha_sum[:,None]

        par.betas = np.linspace(1,1.3,par.J)

        # e. choose es, each good is distrubted according to expontential distribution
        par.es = np.empty((par.N,par.J))    
        for i in range(par.J):
            par.es[:,i] = np.random.exponential(par.betas[i], size=par.N)

        # generate random positive values for the first J-1 elements
        par.ps = np.random.rand(par.J-1) +1
        # set the last element to 1
        par.ps = np.append(par.ps, 1)

    # c. demand function
    def demand_good_i_func(self):
        par = self.par
        I = np.zeros(par.N)
        for j in range(par.J):
            I += par.ps[j] * par.es[:,j]
        return par.alphas[:,par.i]*I/par.ps[par.i]

    # d. excess demand function
    def excess_demand_good_i_func(self):
        par = self.par
        # a. demand
        demand = np.sum(self.demand_good_i_func())
        
        # b. supply
        supply = np.sum(par.es[:,par.i])
        
        # c. excess demand
        excess_demand = demand - supply

        return excess_demand

    # e. find equilibrium function
    def find_equilibrium(self):
        par = self.par
        t = 0
        while True:
            # a. step 1: excess demand
            ZS = np.empty(par.J-1)
            for i in range(par.J-1):
                par.i = i
                ZS[i] = self.excess_demand_good_i_func()
            
            # b: step 2: stop?
            if  np.abs(np.sum(ZS)) < par.eps or t >= par.maxiter:
                print(f'{t:3d}: ps = {par.ps} -> excess demand -> {np.sum(ZS):14.8f}')
                break    
            
            # c. step 3: update ps
            for i in range(par.J-1):
                par.i = i
                par.ps[i] = par.ps[i] + par.kappa*ZS[i]/par.alphas.shape[0]

            # d. step 4: return 
            if t < 5 or t%100 == 0:
                print(f'{t:3d}: ps = {par.ps} -> excess demand -> {np.sum(ZS):14.8f}')
                #print(f'{t:3d}: p2 = {ps[1]:12.8f} -> excess demand -> {Z1:14.8f}')
            elif t == 5:
                print('   ...')
            t += 1    
