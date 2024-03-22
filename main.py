import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from math import sin, cos, radians, degrees, sqrt, atan, floor


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
    global k, delta_t, x_zid
    
    def __init__(self, x0, y0, v0, theta0):

        self.x, self.y = x0, y0
        self.theta = theta0 #kut nagiba
        self.v = v0
        self.greska = 0 #odstupanje loptice od početne visine kad se vrati na x = 0
        
    def kreiraj_putanju(self):

    #Funkcija koja nam mijenja x, y, v, theta za loptu tijekom putanje sve do sudara i vraća koordinate tijekom putanje      
    #uvjetima: x0, y0, v0, theta(kut početnog izbačaja u stupnjevima), delta_t.
    #Vrijednosti x i y, kao i vy, računate su Eulerovom metodom. vx posebno ne računamo jer je ono 
    #konstatno za danu putanju.

        vx0, vy0 = self.v*cos(radians(self.theta)), self.v*sin(radians(self.theta))
        
        vy_lista = [vy0]
        x_lista, y_lista  = [self.x], [self.y]
        
        while True:

            if self.x <= x_zid and self.x >= 0 and self.y >= 0.1:
                
                vy_lista.append(vy_lista[-1] + delta_t*(-9.81))

                x_lista.append(x_lista[-1] + delta_t*vx0)
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
            
            elif self.y < 0.1:
                x_lista.pop()
                y_lista.pop()
                self.x, self.y = x_lista[-1], y_lista[-1]
                vy = -k*vy_lista[-1]
                vx = vx0
                self.v = sqrt(vy**2 + vx**2)
                self.theta = calc_theta(vx, vy)
                break

            else:
                break
                
        return x_lista, y_lista

    def simulacija(self):
        x_lista, y_lista = [], []
        
        while self.x >=0:
            x_c, y_c = self.kreiraj_putanju()
            x_lista.extend(x_c)
            y_lista.extend(y_c)

        self.greska = y_lista[-1] - y_lista[0]
        return x_lista, y_lista 

         

def animacija_vise_loptica(): #n je broj loptica
    
    print()
    n = int(input("Odaberite broj loptica: "))
    
    lopte = []
    for i in range(n):
        v = float(input(f"Početna brzina {i+1}. loptice: "))
        theta = float(input(f"Početni kut nagiba {i+1}. loptice: "))
        print()
        lopta = Lopta(x0 = 0, y0 = 2, v0 = v, theta0 = theta)
        lopte.append(lopta)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 10)

    #Crtamo zid

    ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 5)

    putanje = []
    x = []
    y = []

    for i in range(n):
        x_c, y_c = lopte[i].simulacija()
        x.append(x_c)
        y.append(y_c)

        putanja, = ax.plot(x[i][0], y[i][0], '-o', color = "red", markersize = 5) 
        putanje.append(putanja)

    def update(frame):
        for i in range(n):
            putanje[i].set_data(x[i][frame], y[i][frame])
        
    num_it = max([len(t) for t in x])
    animation = FuncAnimation(fig, update, frames=range(num_it), interval=1)

    plt.show()

    return lopte

def animiraj_loptu(lopta):
    global x_zid, y_zid
    
    x, y = lopta.simulacija()

    fig, ax = plt.subplots()
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    #Crtamo zid
    ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 5)

    #Crtamo pravac y = y0
    ax.plot([0, x_zid], [2, 2], color = "red", linestyle = "dashed")
    putanja, = ax.plot(x[0], y[0], '-o', color = "red", markersize = 5)

    def update(frame):
        novi_x = x[frame]
        novi_y = y[frame]
        putanja.set_data(novi_x, novi_y)

    animation = FuncAnimation(fig, update, frames=range(len(x)), interval=1)
    plt.show()




#Inicijaliziramo početne parametre
delta_t = 0.02
x_zid, y_zid = 15, 19
k = 0.710

os.system("clear")

#simulacija_vise_loptica()


#Optimalna loptica

v = np.arange(10,40,0.1)
theta = 35
d = np.zeros(v.shape)
lopte = []
for i in range(len(v)):
    lop = Lopta(x0 = 0, y0 = 2, v0 = v[i], theta0 = theta)
    lopte.append(lop)
    x, y = lop.simulacija()
    d[i] = lop.greska
argmin = np.argmin(np.absolute(d))
najbolja_lopta = Lopta(x0 = 0, y0 = 2, v0 = v[argmin], theta0 = theta)
animiraj_loptu(najbolja_lopta)
print(najbolja_lopta.y)










'''

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
#Crtamo zid
ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 5)

#Crtamo pravac y = y0
ax.plot([0, x_zid], [2, 2], color = "red", linestyle = "dashed")
putanja, = ax.plot(x[0], y[0], '-o', color = "red", markersize = 5)

def update(frame):
    novi_x = x[frame]
    novi_y = y[frame]
    putanja.set_data(novi_x, novi_y)

animation = FuncAnimation(fig, update, frames=range(len(x)), interval=1)
plt.show()
'''