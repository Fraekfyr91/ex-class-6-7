import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize
class optimum():
    '''Simple class to find and print optimum'''
    def __init__(self, guess = 0, plot_start = -10, plot_end = 10):
        '''Initializer'''
        self.x_guess = guess
        self.plot_end = plot_end
        self.plot_start = plot_start
        self.x1_vec = np.linspace(self.plot_start,self.plot_end, 100)

    def f(self, x):
        """
        Defines an equation.
        
        Args:
        x (float): x value
        
        Returns:
        func (float): Function value sinus x + 0.05 x^2 
        """
        
        func = np.sin(x)+0.05*x**2 
        
        return func
            
    def solve(self, method = 'BFGS', disp = True):
        '''
        Finds the minimum value of the function f()
        
        Args:
            disp (Bool): True or False, Prints solver outcomes
            method (str): optimizer algorithm
        
        Returns:
            Function minimum values for x and f(x).
        '''
        
         # optimizer needs a starting point for the two values     
        obj = lambda x: self.f(x) #objective function to optimize - in this case minimize
 
        res = optimize.minimize(obj, self.x_guess,method=method) #Nelder-mead is standard and simple method
        if disp:
            print("-----------")
            print(res.message)
            print("-----------")
        
        #c.unpacking results
        x1_best_scipy = res.x[0]
        f_best_scipy = res.fun
        if disp:
            # d. print
            print(f'Using numerical solver the optimal values are:')
            print(f'Function = {f_best_scipy:.4f};  x1 = {x1_best_scipy:.4f}')    
       
        return  x1_best_scipy,f_best_scipy
    
    
    def twod_plot(self, method = 'BFGS', disp = False):
        """
        Plots graph

        Args:
            Method (str): Algorithm to scipy solver
            disp (bool): Display solve output
        Returns:
            
        """
        x_1, f_x1 = self.solve(method, disp)
        fig = plt.figure(figsize=(10,5)) # define new figure object
        ax = fig.add_subplot(111) # add subplot
        obj = [self.f(x) for x in self.x1_vec]

        ax.plot(self.x1_vec,obj) # plot 2-dimensional function
        ax.plot(x_1, f_x1, 'ro')
        ax.text(x_1 - 2, f_x1 + 0.5, f'Minimum is ({x_1:.3f}, {f_x1:.3f})')
        #add lines
        for y in range(-1, 6):    
            plt.plot(range(self.plot_start,self.plot_end + 1), [y] * len(range(self.plot_start, self.plot_end + 1)), "--", lw=0.5, color="black", alpha=0.3)

        ax.xaxis.label.set_fontsize(14) #set label fontsize to 14
        ax.yaxis.label.set_fontsize(14)
        ax.set(xlabel="$x$", ylabel = "$f(x)$",xlim = ([self.plot_start,self.plot_end])) #set xlabel,ylabel and xlimit
        for item in ax.get_yticklabels()+ax.get_xticklabels(): # set ticklabels to fontsize 14
            item.set_fontsize(14)

        #remove borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
