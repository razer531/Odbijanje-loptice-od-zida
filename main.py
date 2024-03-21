import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import scipy 

#Kreiramo klasu lopta 

class Lopta:
    def __init__(self, x0, y0, v0, theta, radijus):
        self.koord = x0, y0
        self.theta = theta #pocetni kut nagiba
        self.v = v0
        self.radijus = radijus

lopta = Lopta(radijus = 0.5, x0 = 0, y0 = 5, v0 = 2, theta = 0)

fig, ax = plt.subplots()
ax.set_xlim(-10, 42)
ax.set_ylim(0, 40)

ax.plot([40,40], [0,35], color = "black") #Crtamo zid

krug = Circle((lopta.koord[0], lopta.koord[1]), radius = lopta.radijus, edgecolor='r', facecolor='r')  
ax.add_patch(krug)
ax.set_aspect('equal', adjustable='box')


plt.show()