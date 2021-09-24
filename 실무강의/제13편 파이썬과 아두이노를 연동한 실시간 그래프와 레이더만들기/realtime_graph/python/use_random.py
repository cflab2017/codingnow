from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import random

fig = plt.figure()
ax = plt.axes(xlim=(0, 50), ylim=(0, 250))

max_points = 50
line, = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float)*np.nan,
                lw=2)
data = 0

def getDataFunc():
    # global data
    # data = data + 1
    # data = data % 200
    # return data
    return random.randrange(1, 200)

def animate(i):
    y = float(getDataFunc())
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    return line,

anim = animation.FuncAnimation(
                                fig, 
                                animate, 
                                init_func=lambda : line, 
                                interval=20)
plt.show()
