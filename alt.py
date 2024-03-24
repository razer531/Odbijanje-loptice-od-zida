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
        self.povijest = {}
       
        self.povijest["x_pov"] = [x0]
        self.povijest["y_pov"] = [y0]
        self.povijest["v_pov"] = [v0]
        self.povijest["theta_pov"] = [theta0]
        

    def update(self):
        vx, vy = self.v*cos(radians(self.theta)), self.v*sin(radians(self.theta))

        if self.x <= x_zid-0.2 and self.x >= 0 and self.y >= 0.3:
            vx = vx
            vy += delta_t * (-9.81)
            self.x += delta_t*vx
            self.y += delta_t*vy
            self.v = sqrt(vy**2 + vx**2)
            self.theta = calc_theta(vx, vy)

            self.povijest["x_pov"].append(self.x)
            self.povijest["y_pov"].append(self.y)
            self.povijest["v_pov"].append(self.v)
            self.povijest["theta_pov"].append(self.theta)
        
        elif self.x > x_zid-0.2:
            vx = -k*vx
            self.x += delta_t*vx
            self.y += delta_t*vy
            self.v = sqrt(vy**2 + vx**2)
            self.theta = calc_theta(vx, vy)

            self.povijest["x_pov"].append(self.x)
            self.povijest["y_pov"].append(self.y)
            self.povijest["v_pov"].append(self.v)
            self.povijest["theta_pov"].append(self.theta)
                
        elif self.y < 0.3:
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
        
        while self.x >= 0 and self.v > 1:
            self.update()
        
        self.greska = self.y - self.povijest["y_pov"][0]

        if animiraj:
            
            x, y = self.povijest["x_pov"], self.povijest["y_pov"]

            fig, ax = plt.subplots()
            ax.set_xlim(-1, 20)
            ax.set_ylim(0, 20)
            
            #Crtamo zidove
            ax.plot([x_zid, x_zid], [0,y_zid], color = "black", linewidth = 3)
            ax.plot([0, 0], [0,y_zid], color = "black", linewidth = 3)

            #Crtamo pravac y = y0
            ax.plot([0, x_zid], [2, 2], color = "red", linestyle = "dashed")
            putanja, = ax.plot(x[0], y[0], '-o', color = "red", markersize = 5)

            def update(frame):
                novi_x = x[frame]
                novi_y = y[frame]
                putanja.set_data(novi_x, novi_y)

            animation = FuncAnimation(fig, update, frames=range(len(x)), interval=1)
            plt.show()

#Optimalna loptica
def optimalna_loptica(theta):
    v = np.arange(10,40,0.1)
    d = np.zeros(v.shape)
    lopte = []
    for i in range(len(v)):
        lop = Lopta(x0 = 0, y0 = 2, v0 = v[i], theta0 = theta)
        lopte.append(lop)
        lop.simulacija()
        d[i] = lop.greska
    argmin = np.argmin(np.absolute(d))
    najbolja_lopta = Lopta(x0 = 0, y0 = 2, v0 = v[argmin], theta0 = theta)
    
    return najbolja_lopta


#Inicijaliziramo početne parametre
delta_t = 0.02
x_zid, y_zid = 15, 19
theta = 45
k = 0.7
os.system("clear")

lopta = Lopta(x0 = 0, y0 = 4, v0 = 13, theta0 = 45)
lopta.simulacija(animiraj = True)












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









