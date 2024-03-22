import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from math import ceil, sin, cos, radians, degrees, sqrt, atan


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
        self.theta = theta0 #pocetni kut nagiba
        self.v = v0
        
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

        return x_lista, y_lista

         

#Inicijaliziramo početne parametre


def glavni_program(n):
    
    print()
    loptice = []
    for i in range(n):
        v = int(input(f"Početna brzina {i+1}. loptice: "))
        theta = int(input(f"Početni kut nagiba {i+1}. loptice: "))
        print()
        lopta = Lopta(x0 = 0, y0 = 2, v0 = v, theta0 = theta)
        loptice.append(lopta)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    #Crtamo zid
    ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 5)

    putanje = []
    x = []
    y = []

    for i in range(n):
        x_c, y_c = loptice[i].simulacija()
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

    return loptice


#Inicijaliziramo početne parametre
delta_t = 0.015
x_zid, y_zid = 9, 9
k = 0.710

os.system("clear")

n = int(input("Odaberite broj loptica: "))
loptice = glavni_program(n)


