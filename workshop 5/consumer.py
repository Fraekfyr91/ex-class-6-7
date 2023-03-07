import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize
class consumer():
    '''Simple class to find and print optimum'''
    def __init__(self,alpha=0.5, p1=1, p2=2, I =10):
        '''Initializer'''
        self.alpha = alpha # preference parameter
        self.p1 = p1 # price of good 1
        self.p2 = p2 # price of good 2
        self.I = I # income
                  
        self.x1 = np.nan # not-a-number
        self.x2 = np.nan # not-a-number
        self.N = 100 # grid size
        self.x2_max = I/p2 # all income on x2
        self.x1_max = I/p1 # all income on x2
        
    def u_func(self,x1,x2):
        return x1**self.alpha*x2**(1-self.alpha) # cobdouglas util 
    
    def value_of_choice(self,x1):
        ''' Finds optimal value of x2
        Args:
            x1 (float): Quantity of good 1.
            alpha (float): Output elasticities of good 1 and 2.
            u (float):  Utility of good 1 and 2.
            I (float/int): Income.
            p1 (float/int): Price of good 1.
            p2 (float/int): Price of good 2.
        Returns:
            Utility (float): Negative utility of good 1 and 2
        '''
        #find x2 
        x2 = (self.I-self.p1*x1)/self.p2  #  all money not spent on x1
        return -self.u_func(x1,x2) # negative because we minimize

    def print_solution(self,x1,x2,u):
        ''' Print function
        Args:
            X1 (float): Quantity of good 1.
            x2 (float): Quantity of good 1.
            u (float):  Utility of good 1 and 2.
            I (float/int): Income.
            p1 (float/int): Price of good 1.
            p2 (float/int): Price of good 2.
        Returns:
            prints the solutions to the consumer problem.
        '''
        print(f'x1 = {x1:.8f}')
        print(f'x2 = {x2:.8f}')
        print(f'u  = {u:.8f}')
        print(f'I-p1*x1-p2*x2 = {self.I-self.p1*x1-self.p2*x2:.8f}') 
    
    
    def solve(self, print_sol = True):
        ''' Solve Consumer problem
        Args:
            print_sol (Bool): Prints solution if True
            I (float/int): Income.
            p1 (float/int): Price of good 1.

        Returns:
            Updates x1 and x2 and Utility
        '''
        #value_of_choice is the function we minimize
        #method is the algorithm used
        #bounds is set to use between no income and all income on good 1
        # - bounds is the space we look for the solution 
        # args is the constant parameteres in the problem

        sol_case = optimize.minimize_scalar(
            self.value_of_choice,
            method='bounded',
            bounds=(0,self.I/self.p1)) 
        
        self.x1 = sol_case.x # update x1 from nan to value
        self.x2 = (self.I-self.p1*self.x1)/self.p2 # update x2 
        self.u = self.u_func(self.x1,self.x2) # optiaml utility

        if print_sol: # print solution if wanted
           
            self.print_solution(self.x1,self.x2,self.u)
        else: pass
        
      
    def plot(self,print_sol =False):
        ''' Plot solution with indifferece curves and budget line
        Args:
            x1 (float): Quantity of good 1.
            alpha (float): Output elasticities of good 1 and 2.
            u (float):  Utility of good 1 and 2.
            I (float/int): Income.
            p1 (float/int): Price of good 1.
            p2 (float/int): Price of good 2.
            out (bool): option to print optimal values
        Returns:
            A plot of the solution and utility and indifference curves
        '''
        self.solve(print_sol) # update values
        # initialize the figure
        self.fig = plt.figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(1,1,1)
        # allocate memory
        x1_vecs = []
        x2_vecs = []
        us = []
        
        for fac in [0.75,1,1.25]:
            
            # fac = 1 -> indifference curve through optimum
            # fac < 1 -> ... below optimum
            # fac > 1 -> ... above optimum
                
            # a. utility in (fac*x1,fac*x2)
            u = self.u_func(fac*self.x1,fac*self.x2)
            
            # b. allocate numpy arrays
            x1_vec = np.empty(self.N)
            x2_vec = np.linspace(1e-8,self.x2_max,self.N)

            # c. loop through x2 and find x1
            for i,x2 in enumerate(x2_vec):

                # local function given value of u and x2
                def objective(x1):
                    return self.u_func(x1,x2)-u
                # update solution
                sol = optimize.root(objective, 0)
                # allocate solution
                x1_vec[i] = sol.x[0]
            
            # d. save
            x1_vecs.append(x1_vec)
            x2_vecs.append(x2_vec)
            us.append(u)
        
        for x1_vec,x2_vec,u in zip(x1_vecs,x2_vecs,us):
            # Plot indifference curves
            self.ax.plot(x1_vec,x2_vec,label=f'$u = {u:.2f}$')
        
        # custumize labels
        self.ax.set_xlabel('$x_1$')
        self.ax.set_ylabel('$x_2$')
        # custumize axis limits
        self.ax.set_xlim([0,self.x1_max])
        self.ax.set_ylim([0,self.x2_max])
        
        self.ax.grid(ls='--',lw=1) # dashed line
        self.ax.legend(loc='upper right') # legend

        self.ax.plot(self.x1,self.x2,'ro') # a dot for optimum
        self.ax.text(self.x1*1.03,self.x2*1.03,f'$u^{{max}} = {self.u:.2f}$') # text in optimum

        x = [0,0,self.I/self.p1] # x-cordinates
        y = [0,self.I/self.p2,0] # y-cordinates
        
        # plot budgetline
        self.ax.plot(x,y,"--", lw=0.5, color="black", alpha=0.3) # alpha controls transparance
        