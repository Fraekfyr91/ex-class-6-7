import matplotlib.pyplot as plt # for plotting
import seaborn as sns           # for prettyness in plotting
import numpy as np              # for numericals
sns.set(style="whitegrid")      # whitegrid make the plot ohh so pretty
sns.set_palette("dark")         # we like our palette as we like our homour, for prettynes

class workshop_ex:
    '''
    A class that calculates the Probability Density Function (PDF) and Cumulative Density Fucntion (CDF) and displays it.

    Inputs:     
        mu (float): mean of the density, default = 0
        sigma (float): Standard deviation, defaul = 1

    Made for Introduction to Programming and Numerical Analysis 2023
    Lasse Ramovic Laustrup
    '''
    def __init__(self, mu = 0, sigma = 1, tsigma = 3):
        self.mu = mu # setting a to equal the input, default is 8
        self.sigma = sigma # setting b to equal the input, default is 2
        self.tsigma = tsigma
    def PDF(self, grid_vals = False):
        '''
        Calculates the Probabilty Density Fuction for mean, mu and standard deviation, sigma.
        
        Inputs:
            mu (float): mean of the density, default = 0
            sigma (float): Standard deviation, default = 1
            tsigma (int): number of standard deviation between calculation start/end and mean, default = 3 
            grid_vals (bool): option to return grid values, default = False
        Returns:
            pdf (list): list of probability density function ranging between - tsigma * mean and tsigma * mean 
        
        '''
        # create a lambda function that takes 3, arguments. x is the function value, mu is the distribution mean, sigma is the standard deviation, 
        # returns the probability density function
        pdf = lambda x, sigma, mu: 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- 1 / 2*(( x - mu) / sigma)**2) 



        # if mu = 0 and sigma = 1, pdf is standard normal

        grid = np.linspace(self.mu - self.tsigma * self.sigma, self.mu + self.tsigma * self.sigma, 1000) # create a grid for funciton evaluations and plotting
        vals = [ pdf(i, self.sigma, self.mu) for i in grid ]                 # list comprehension, provides list of pdf values on the grid
        
        if grid_vals:
            return vals, grid
        return vals
        

    def CDF(self, pdf = False):
        '''
        Calculates the Cumulative Density Function for mean, mu and standard deviation, sigma.
        Depends on calculation in PDF function
        
        Inputs:
            mu (float): mean of the density, default = 0
            sigma (float): Standard deviation, default = 1
            tsigma (int): number of standard deviation between calculation start/end and mean, default = 3 
            pdf (bool): option to return probability density function values, default = False

        Returns:
            cdf (list): list of cumulative density function ranging between - tsigma * mean and tsigma * mean 
        '''

        if pdf:
            pdf_vals, grid = self.PDF(grid_vals = True)
        else:
            pdf_vals = self.PDF(self) # call PDF function to calculate PDF
         # cumulative sum of probabilities divided by the sum of probabilities, returns the cumulative distibution function
        # for every value on the grid
        cdf = np.cumsum(pdf_vals) / np.sum(pdf_vals)  
        if pdf:
            return cdf, pdf_vals, grid
        return cdf

    def make_figure(self, savename = None, lines = False):
        '''
        Plots the Cumulative Density Function and Probability density function for mean, mu and standard deviation, sigma.
        Depends on calculation in PDF and CDF functions
        
        Inputs:
            mu (float): mean of the density, default = 0
            sigma (float): Standard deviation, default = 1
            tsigma (int): number of standard deviation between calculation start/end and mean, default = 3 
            Savename (str): if specified the figuere will be saved by the string name, default = None
            lines (bool): option to add lines at y = 0,5 and x = mu, default = False
        Returns:
            None
        Output:
            Figure with Probability Density function and Cumulative Density Function
        '''
        cdf_vals, pdf_vals, grid = self.CDF(pdf=True)  
          
        fig, ax = plt.subplots(figsize=(10,6)) # defining a figue and axis
        ax.plot(grid, pdf_vals, label = 'PDF')     # plotting the proberbility density function, as a line plot
        ax.plot(grid, cdf_vals, label = 'CDF')      # plotting the cumulative density function, as a line plot
        if lines:
            ax.axhline(y = 0.5, color = 'k', linestyle = ':', linewidth=.75) # plot horizontal line at p = 0.5
            ax.axvline(x = self.mu, color = 'k', linestyle = ':', linewidth=.75)  # plot vertical line at x = mu

        ax.text(x = self.mu - self.tsigma * self.sigma, y = 0.85 , s = f' $\mu$ = {self.mu}, $\sigma$ = {self.sigma}')


        # Add title and axis labels
        plt.xlabel('X', fontsize = 14, fontweight = 'bold')     
        plt.ylabel('PDF(x), CDF(x)', fontsize=14, fontweight='bold')
        ax.grid(False, which = 'both', axis = 'x')  # remove some the grid in the plot
        ax.set_axisbelow(True)                      # ticks below axis, maybe they are anyway.

        # Add legend
        ax.legend()

        # Remove box around the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Change fontsize for axis labels and tick marks
        ax.tick_params(axis = 'both', labelsize = 14)
        if savename:
            plt.savefig(f'{savename}.png')
        plt.show()