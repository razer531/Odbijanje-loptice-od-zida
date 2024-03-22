import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from math import ceil, sin, cos, radians, degrees, sqrt, atan

k = 0.7
x_zid, y_zid = 9,9

def calc_theta(vx, vy):
    if vy > 0 and vx > 0:
        return degrees(atan(vy/vx))
    if vy > 0 and vx < 0:
        return degrees(atan(vy/vx)) + 180
    if vy < 0 and vx > 0:
        return degrees(atan(vy/vx))
    if vy < 0 and vx < 0:
        return degrees(atan(vy/vx)) + 180

#Kreiramo klasu lopta 

class Lopta:
    global k
    
    def __init__(self, x0, y0, v0, theta, radijus):
        self.x, self.y = x0, y0
        self.theta = theta #pocetni kut nagiba
        self.v = v0
        self.radijus = radijus
        self.lupio = False
        
    def kreiraj_putanju(self):

    #Funkcija koja nam mijenja x, y, v, theta za loptu tijekom putanje sve do sudara i vraća koordinate tijekom putanje      
    #uvjetima: x0, y0, v0, theta(kut početnog izbačaja u stupnjevima), delta_t.
    #Vrijednosti x i y, kao i vy, računate su Eulerovom metodom. vx posebno ne računamo jer je ono 
    #konstatno za danu putanju.
        
        global delta_t 
        global x_zid

        vx0, vy0 = self.v*cos(radians(self.theta)), self.v*sin(radians(self.theta))
        
        vy_lista = [vy0]
        x_lista, y_lista  = [self.x], [self.y]
        
        while True:

            if self.x <= x_zid and self.y >= 0:
                x_lista.append(x_lista[-1] + delta_t*vx0)
                vy_lista.append(vy_lista[-1] + delta_t*(-9.81))
                y_lista.append(y_lista[-1] + delta_t*vy_lista[-1])
                self.x, self.y = x_lista[-1], y_lista[-1]
                continue
            
            elif self.x > x_zid:
                x_lista.pop()
                y_lista.pop()
                self.x, self.y = x_lista[-1], y_lista[-1]
                vy = vy_lista[-1]
                vx = -k*vx0
                self.v = sqrt(vy**2 + vx**2)
                self.theta = calc_theta(vx, vy)
                break
            
            else:
                x_lista.pop()
                y_lista.pop()
                self.x, self.y = x_lista[-1], y_lista[-1]
                vy = -k*vy_lista[-1]
                vx = vx0
                self.v = sqrt(vy**2 + vx**2)
                self.theta = calc_theta(vx, vy)
                break
                
        return x_lista, y_lista

    def simulacija(self):
        x_lista, y_lista = [], []
        
        while self.x >=0:
            x_c, y_c = self.kreiraj_putanju()
            x_lista.extend(x_c)
            y_lista.extend(y_c)

        return x_lista, y_lista

         


'''
#Crtamo loptu na početku
def crtaj_loptu(ax, x, y, r):
    circle = Circle((x, y), radius = r, edgecolor='r', facecolor='r')
    ax.add_patch(circle)


krug = Circle((lopta.koord[0], lopta.koord[1]), radius = lopta.radijus, edgecolor='r', facecolor='r')  
ax.add_patch(krug) 
ax.set_aspect('equal', adjustable='box')
'''

lopta = Lopta(radijus = 0.5, x0 = 0, y0 = 2, v0 = 10, theta = 45)

#Inicijaliziramo početne parametre
delta_t = 0.015

t_start = 0
t_end = 2
num_it = ceil((t_end-t_start)/delta_t)

x,y = lopta.simulacija()
print(lopta.x, lopta.y)
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

#Crtamo zid
x_zid = 9
y_zid = 9
ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 5)

putanja, = ax.plot(x[0], y[0], '-o', color = "red", markersize = 0.5)

def update(frame):
    global putanja
    
    novi_x = x[:frame]
    novi_y = y[:frame]
    putanja.set_data(novi_x, novi_y)

    

animation = FuncAnimation(fig, update, frames=range(100000), interval=1)

plt.show()
