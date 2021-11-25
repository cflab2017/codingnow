from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import serial

Y_limit_max = 2.0
Y_limit_min = 1.0

###########################################
seri = serial.Serial(port='COM5', baudrate=9600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS)

fig = plt.figure()
ax = plt.axes(xlim=(0, 50), ylim=(Y_limit_min, Y_limit_max))

max_points = 50
line, = ax.plot(np.arange(max_points),
                np.ones(max_points, dtype=np.float)*np.nan,
                lw=2)

def getDataFunc():
    try:
        if seri.readable():
            ret = seri.readline()
            ret = ret.decode()[:len(ret)-2]   
            print(ret)
            if ret.find("ppm") > -1:
                ret = ret.replace('ppm', '')
                ret = ret.replace(' ', '')
                print(ret.split(":"))
                res = ret.split(":")[1]
                return float(res)
    except Exception as ex:
        print(ex)
        pass
    return -1

def animate(i):
    y = float(getDataFunc())
    if(y > -1):
        old_y = line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        line.set_ydata(new_y)
    return line,

anim = animation.FuncAnimation(
                            fig, 
                            animate, 
                            init_func=lambda: line, 
                            interval=20)
plt.show()
