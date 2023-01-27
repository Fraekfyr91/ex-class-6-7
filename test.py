

class new_class():
    def __init__(self):
        self.a = 8
        self.b = 2
    def doing_shit(self, sentence):

        for i in range(self.b, self.a):
            
            print(sentence * i)
   
new_class().doing_shit('hello')



