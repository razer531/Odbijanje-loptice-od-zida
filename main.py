import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from math import ceil, sin, cos, radians

#Kreiramo klasu lopta 

class Lopta:
    def __init__(self, x0, y0, v0, theta, radijus):
        self.koord = x0, y0
        self.theta = theta #pocetni kut nagiba
        self.v = v0
        self.radijus = radijus

lopta = Lopta(radijus = 0.5, x0 = 0, y0 = 5, v0 = 2, theta = 0)


def kreiraj_putanju(x0, y0, v0, theta, num_it, delta_t):

    #Funkcija koja nam stvara x i y koordinate za loptu tijekom putanje, inicijaliziranu početnim
    #uvjetima: x0, y0, v0, theta(kut početnog izbačaja u stupnjevima), num_it(broj iteracija), delta_t.

    vx0, vy0 = v0*cos(radians(theta)), v0*sin(radians(theta))
        
    x_lista = [x0]
    for i in range(num_it):
        x_lista.append(x_lista[i] + delta_t*vx0)
    
    vy_lista = [vy0]
    for i in range(num_it):
        vy_lista.append(vy_lista[i] + delta_t*(-9.81))
        
    y_lista = [y0]
    for i in range(num_it):
        y_lista.append(y_lista[i] + delta_t*vy_lista[i])
    
    return x_lista, y_lista
        
    


fig, ax = plt.subplots()
ax.set_xlim(-1, 6)
ax.set_ylim(0, 7)

#Crtamo zid
ax.plot([5,5], [0,7], color = "black")

'''
#Crtamo loptu na početku
def crtaj_loptu(ax, x, y, r):
    circle = Circle((x, y), radius = r, edgecolor='r', facecolor='r')
    ax.add_patch(circle)


krug = Circle((lopta.koord[0], lopta.koord[1]), radius = lopta.radijus, edgecolor='r', facecolor='r')  
ax.add_patch(krug) 
ax.set_aspect('equal', adjustable='box')
'''
#Inicijaliziramo početne parametre, s time da t_sudar treba točno izračunati u ovisnosti o prethodnim 
#parametrima, jer tada želimo zaustaviti kreiranje prvog dijela putanje.
delta_t = 0.02
h = 1
vx0 = 5
vy0 = 3
t_start = 0

#Sada je potrebno odabrati t_end pažljivo u ovisnosti o vx0, vy0, tj. da bu
t_sudar = 2
num_it = ceil((t_sudar-t_start)/delta_t)

x, y = kreiraj_putanju(0, h, 7, 45, num_it, delta_t)
putanja, = ax.plot(x[0], y[0], '-o', color = "red", markersize = 0.5)

def update(num_it):
    
    global putanja

    novi_x = x[:num_it]
    novi_y = y[:num_it]

    putanja.set_data(novi_x, novi_y)
    

animation = FuncAnimation(fig, update, frames=range(num_it), interval=1)

plt.show()
