import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.cm as cm

interval = 20 # time between frames in ms
show_trail = False #show the trajectory of each particle
trail_width = 1     # width of the trajectory line
save_to_file = True # save the animation file or show it on screen
limit=5 # axis limit
radius=0.05 # planet radius              
dpi = 150 # resolution of the output file


file_out='innerplanets2'


with open('simulation_data_planets.txt', "r") as f:
    data_str = f.read()


frames_data = list()


for frame_data_str in data_str.split("\n"):
    
    frame_data = list()


    for planet_pos_str in frame_data_str.split("\t"):
        
        if planet_pos_str!='':
            frame_data.append(float(planet_pos_str))

    
    frames_data.append(frame_data)




nplanets = int(len(frames_data[0])/2)



fig, ax = plt.subplots()


ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)


planet_radius=np.zeros(nplanets)
for i in range(nplanets):
    planet_radius[i]= radius




planet_points = list()
planet_trails = list()

colors = cm.rainbow(np.linspace(0, 1, 9))
for i in range(nplanets):

    x= frames_data[0][2*i]
    y=frames_data[0][2*i+1]

    #planet_point, = ax.plot(x, y, "o", markersize=10)
    planet_point = Circle((x, y), planet_radius[i], color=colors[i])
    ax.add_artist(planet_point)
    planet_points.append(planet_point)

    
    if show_trail:
        planet_trail, = ax.plot(
                x, y, "-", linewidth=trail_width,
                color=colors[i])
        planet_trails.append(planet_trail)
 

def update(j_frame, frames_data, planet_points, planet_trails, show_trail):
    
    for i in range(nplanets):
        x= frames_data[j_frame][2*i]
        y= frames_data[j_frame][2*i+1]

        planet_points[i].center = (x, y)

        if show_trail:
            xs_old, ys_old = planet_trails[i].get_data()
            xs_new = np.append(xs_old, x)
            ys_new = np.append(ys_old, y)

            planet_trails[i].set_data(xs_new, ys_new)

    return planet_points + planet_trails

def init_anim():
    
    if show_trail:
        for j_planet in range(nplanets):
            planet_trails[j_planet].set_data(list(), list())

    return planet_points + planet_trails


nframes = len(frames_data)


if nframes > 1:
    # Info FuncAnimation: https://matplotlib.org/stable/api/animation_api.html
    animation = FuncAnimation(
            fig, update, init_func=init_anim,
            fargs=(frames_data, planet_points, planet_trails, show_trail),
            frames=len(frames_data), blit=True, interval=interval)

    
    if save_to_file:
        animation.save("{}.gif".format(file_out), dpi=dpi)
    else:
        plt.show()

else:
    
    if save_to_file:
        fig.savefig("{}.pdf".format(file_out))
    else:
        plt.show()


