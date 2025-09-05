import numpy as np
import matplotlib.pyplot as plt
import imageio
import os
from numba import njit
import matplotlib.cm as cm


name = ['sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

x=np.array([0, 5.8343e10, 1.0771e11, 1.496e11, 2.2739e11, 7.779e11, 1.4331e12, 2.8723e12, 4.5029e12])
y=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
vx=np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
vy=np.array([0, 47.9e3, 35.0e3, 29.8e3, 24.0e3, 13.1e3, 9.69e3, 6.81e3, 5.43e3])
m=np.array([1.9891e30, 3.285e23, 4.867e24, 5.97219e24, 6.39e23, 1.898e27, 5.683e26, 8.681e25, 1.024e26])

print('start')



dt = 0.01
steps = 150000



G=6.67430e-11
c= 1.496e11
M=1.9891e30

#the variables are reescalated
x[:]=x[:]/c
m[:]=m[:]/M
vy[:]=vy[:]*np.sqrt(c/(G*M))




@njit
def forces(x,y, m):
    n=len(x)
    forcex=np.zeros(n)
    forcey=np.zeros(n)
    for i in range(n):
        for j in range(i+1, n):
            d2= (x[i]-x[j])**2 + (y[i]-y[j])**2
            fx= -m[i]*m[j]/(d2**1.5)*(x[i]-x[j])
            fy= -m[i]*m[j]/(d2**1.5)*(y[i]-y[j])
            forcex[i]=forcex[i] + fx
            forcey[i]=forcey[i] + fy
            forcex[j]=forcex[j] - fx
            forcey[j]=forcey[j] - fy
    
    ax=forcex/m
    ay=forcey/m


    return ax, ay

def step(x, y, vx, vy, m, dt=dt):
    

    forcex, forcey= forces(x,y,m)

    vxhalf= vx + 0.5*forcex*dt
    vyhalf= vy + 0.5*forcey*dt

    xnew=x + vxhalf*dt
    ynew=y + vyhalf*dt

    forcex, forcey= forces(xnew, ynew, m)

    vxnew=vxhalf + 0.5*forcex*dt
    vynew=vyhalf + 0.5*forcey*dt

    return xnew, ynew, vxnew, vynew



T=np.zeros(8) #periods
osccount=np.zeros(8)
avT=np.zeros(8) #average period for planets with multiple cycles completed 

j=0

with open("simulation_data_planets.txt", "w") as f:

    #structure: x0  y0  x1  y1  etc...

    for i in range(len(x)):

        if i==len(x)-1:
            f.write(str(x[i]) + '\t' + str(y[i]) + '\n')

        else: 
            f.write(str(x[i]) + '\t' + str(y[i]) + '\t')
    

    for i in range(1, steps+1):

        prevy= y.copy()
        x, y, vx, vy= step(x, y, vx, vy, m, dt)

        if i%5==0:
             for i in range(len(x)):

                if i==len(x)-1:
                    f.write(str(x[i]) + '\t' + str(y[i]) + '\n')

                else: 
                    f.write(str(x[i]) + '\t' + str(y[i]) + '\t')


        T[:]=T[:]+dt

        for k in range(8):
            if prevy[k+1]-prevy[0]<0. and y[k+1]-y[0]>=0.:
                osccount[k]=osccount[k] + 1
                avT[k]=avT[k] + T[k]
                T[k]=0.



avT[:]=avT[:]/osccount[:]
avT[:]=avT[:]*np.sqrt(c**3/(G*M))/(3600*24*365.25)

print('Periods in years: ' )
print(avT)



