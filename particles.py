import random

class Particle_System:
    def __init__(self):
        pass
    def Scatter_Effect(self, x, y, random_range):
        return[[x, y], [random.randrange(-random_range[0],random_range[0]),
        random.randrange(-random_range[1],random_range[1])], random.randint(4, 6)]

    def Fountain_Effect(self,x,y,dimension):
        return [[x, y], [random.randrange(-dimension[0], dimension[0]), -dimension[1]], random.randint(4, 6)]
    
    def Rocket_Boost_Effect(self,x,y):
        return [[x, y], [random.randint(0, 20) / 10 - 1, 2], random.randint(4, 6)]


