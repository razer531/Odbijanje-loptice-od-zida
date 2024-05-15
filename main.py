import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sin, cos, radians, degrees, sqrt, atan


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
    global k, g, delta_t, x_zid, lambdaa
    
    def __init__(self, x0, y0, v0, theta0):

        self.x, self.y = x0, y0
        self.theta = theta0 #kut nagiba
        self.v = v0
        self.greska = 0 #odstupanje loptice od početne visine kad se vrati na x = 0
        self.povijest = {}
       
        self.povijest["x_pov"] = [x0]
        self.povijest["y_pov"] = [y0]
        self.povijest["v_pov"] = [v0]
        self.povijest["theta_pov"] = [theta0]
        

    def update(self):
        vx, vy = self.v*cos(radians(self.theta)), self.v*sin(radians(self.theta))

        #Pomak u letu
        if self.x <= x_zid-0.2 and self.x >= 0 and self.y >= 0.3:
            
            self.x += delta_t*vx
            self.y += delta_t*vy
            vx += delta_t * (-lambdaa * vx)
            vy += delta_t * (-g - lambdaa*vy)
            self.v = sqrt(vy**2 + vx**2)
            self.theta = calc_theta(vx, vy)

            self.povijest["x_pov"].append(self.x)
            self.povijest["y_pov"].append(self.y)
            self.povijest["v_pov"].append(self.v)
            self.povijest["theta_pov"].append(self.theta)
        
        elif self.x > x_zid-0.2:
            vx = -k*vx

            self.x = x_zid - 0.2 #Bez ovoga se za neke brzine i kuteve desi da lopta preleti zid

            self.x += delta_t*vx
            self.y += delta_t*vy
            self.v = sqrt(vy**2 + vx**2)
            self.theta = calc_theta(vx, vy)

            self.povijest["x_pov"].append(self.x)
            self.povijest["y_pov"].append(self.y)
            self.povijest["v_pov"].append(self.v)
            self.povijest["theta_pov"].append(self.theta)
                
        elif self.y < 0.3:

            self.y = 0.3 #Analogno, da nebi lopta preletila pod

            vy = -k*vy
            self.x += delta_t*vx
            self.y += 2*delta_t*vy
            self.v = sqrt(vy**2 + vx**2)
            self.theta = calc_theta(vx, vy)

            self.povijest["x_pov"].append(self.x)
            self.povijest["y_pov"].append(self.y)
            self.povijest["v_pov"].append(self.v)
            self.povijest["theta_pov"].append(self.theta)
            
    def simulacija(self, animiraj = False):
        
        while self.v > 1 and self.x >= 0:
            self.update()
        
        self.greska = self.y - self.povijest["y_pov"][0]

        if animiraj:
            
            x, y = self.povijest["x_pov"], self.povijest["y_pov"]

            fig, ax = plt.subplots()
            
            
            #Crtamo zid
            ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 3)

            #Crtamo pravac y = y0
            ax.plot([0, x_zid], [y0, y0], color = "red", linestyle = "dashed")
            putanja, = ax.plot(x[0], y[0], '-o', color = "red", markersize = 5)

            ax.set_xlim(0, x_zid+1)
            ax.set_ylim(0, x_zid+1)
            ax.set_aspect("equal")
            ax.tick_params(axis = "y", length = 5)
            ax.tick_params(axis = "y", length = 5)
            ax.set_title(label = r"Početni kut: ${:.0f}^\circ$".format(self.povijest["theta_pov"][0]) + 
                         "\nOptimalna početna brzina: {:.2f}".format(self.povijest["v_pov"][0]), 
                         fontweight="bold")


            def update(frame):
                novi_x = x[frame]
                novi_y = y[frame]
                putanja.set_data(novi_x, novi_y)

            animation = FuncAnimation(fig, update, frames=range(len(x)), interval=1)
            plt.show()



#Optimalna loptica
def optimalna_loptica(theta):
    v = np.arange(2,1000,0.1)
    d = np.zeros(v.shape)
    for i in range(len(v)):
        lop = Lopta(x0 = 0, y0 = y0, v0 = v[i], theta0 = theta)
        lop.simulacija()
        d[i] = lop.greska
    argmin = np.argmin(np.absolute(d))
    najbolja_lopta = Lopta(x0 = 0, y0 = 2, v0 = v[argmin], theta0 = theta)
    return najbolja_lopta

os.system("clear")

#Inicijaliziramo početne parametre
k = 0.7
delta_t = 0.02
lambdaa = 0.0003
g = 9.81

y0 = 2
theta0 = float(input("Odaberite početni kut: "))
x_zid = float(input("Odaberite udaljenost od zida: "))
y_zid = x_zid - 1

lopta = optimalna_loptica(theta0)
lopta.simulacija(animiraj = True)
