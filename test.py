

class new_class:
    '''
    An awesome class that prints something!!!

    Inputs:     
        a (int): a - 1 is the last last amout of prints
        b (int): b is the first amount of prints

    Made for Introduction to Programming and Numerical Analysis 2023
    Lasse Ramovic Laustrup
    '''
    def __init__(self, a = 8, b = 2):
        self.a = a # setting a to equal the input, default is 8
        self.b = b # setting b to equal the input, default is 2
    def print_something(self, sentence):
        '''
        This is here the action is!!!
        
        Inputs:
            sentence (str): The string that is printed
        Returns:
            None
        Output:
            Prints sentence in a range
        '''
        for i in range(self.b, self.a):
            print(sentence * i)
   



