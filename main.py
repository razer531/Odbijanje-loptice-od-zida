import numpy as np
import matplotlib.pyplot as plt
import scipy 

#Kreiramo klasu lopta 

class Lopta:
    def __init__(self, x0, y0, v0, theta):
        self.pozicija = x0, y0
        self.theta = theta #pocetni kut nagiba
        self.v = v0
