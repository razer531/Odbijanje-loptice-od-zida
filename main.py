import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from math import ceil, sin, cos, radians, degrees, sqrt, atan

k = 0.7

#Kreiramo klasu lopta 

class Lopta:
    global k
    
    def __init__(self, x0, y0, v0, theta, radijus):
        self.x, self.y = x0, y0
        self.theta = theta #pocetni kut nagiba
        self.v = v0
        self.radijus = radijus
        self.x_lista = [self.x] 
        self.y_lista = [self.y]
        self.lupio = False
        
    def kreiraj_putanju(self):

    #Funkcija koja nam stvara x i y koordinate za loptu tijekom putanje, inicijaliziranu početnim
    #uvjetima: x0, y0, v0, theta(kut početnog izbačaja u stupnjevima), num_it(broj iteracija), delta_t.
    #Vrijednosti x i y, kao i vy, računate su Eulerovom metodom. vx posebno ne računamo jer je ono 
    #konstatno za danu putanju.
        

        global delta_t, x_zid

        vx0, vy0 = self.v*cos(radians(self.theta)), self.v*sin(radians(self.theta))
        
        vy_lista = [vy0]
        
        while self.v > 0.5:

            while self.x <= x_zid and self.y >= 0:

                self.x_lista.append(self.x_lista[-1] + delta_t*vx0)
                vy_lista.append(vy_lista[-1] + delta_t*(-9.81))
                self.y_lista.append(self.y_lista[-1] + delta_t*vy_lista[-1])
                
                self.x, self.y = self.x_lista[-1], self.y_lista[-1]
                
            
                
            vx0 = -k*vx0
            vy0 = -k*vy_lista[-1]
            for i in range(1000):
                self.x_lista.append(self.x_lista[-1] + delta_t*vx0)
                vy_lista.append(vy_lista[-1] + delta_t*(-9.81))
                self.y_lista.append(self.y_lista[-1] + delta_t*vy_lista[-1])
                
                self.x, self.y = self.x_lista[-1], self.y_lista[-1]

            break


           

        return self.x_lista, self.y_lista


         
        



lopta = Lopta(radijus = 0.5, x0 = 0, y0 = 2, v0 = 10, theta = 45)


fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

#Crtamo zid
x_zid = 9
y_zid = 9
ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 5)

'''
#Crtamo loptu na početku
def crtaj_loptu(ax, x, y, r):
    circle = Circle((x, y), radius = r, edgecolor='r', facecolor='r')
    ax.add_patch(circle)


krug = Circle((lopta.koord[0], lopta.koord[1]), radius = lopta.radijus, edgecolor='r', facecolor='r')  
ax.add_patch(krug) 
ax.set_aspect('equal', adjustable='box')
'''

#Inicijaliziramo početne parametre
delta_t = 0.015

t_start = 0
t_end = 2
num_it = ceil((t_end-t_start)/delta_t)

x,y = lopta.kreiraj_putanju()

putanja, = ax.plot(x[0], y[0], '-o', color = "red", markersize = 0.5)

def update(frame):
    global putanja
    
    novi_x = x[:frame]
    novi_y = y[:frame]
    putanja.set_data(novi_x, novi_y)

    

animation = FuncAnimation(fig, update, frames=range(num_it), interval=1)

plt.show()
