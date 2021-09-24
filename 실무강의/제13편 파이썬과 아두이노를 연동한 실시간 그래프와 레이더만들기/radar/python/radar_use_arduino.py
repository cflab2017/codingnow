import matplotlib.pyplot as plt
from math import pi
from matplotlib import animation

import serial
seri = serial.Serial(port='COM10', baudrate=9600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS)
######################################################
def updateRadar():
    ax.set_theta_offset(-(pi / 1))  # 시작점
    ax.set_theta_direction(-1)  # 그려지는 방향 시계방향
    ax.set_thetamax(180)
    ax.set_rlabel_position(1)  # y축 각도 설정(degree 단위)
    ax.fill(angles, data, color=color, alpha=0.4)  # 도형 안쪽에 색을 채워준다.
    ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)
    plt.ylim(0, 20)
    plt.yticks([0, 4, 8, 12, 16, 20],
               ['0', '4', '8', '12', '16', '20'],
               fontsize=10)  # y축 눈금 설정
    line, = ax.plot(angles, data, color=color, linewidth=2,
                    linestyle='solid')  # 레이더 차트 출력
    return line
######################################################

def getDataFunc():
    try:
        if seri.readable():
            res = seri.readline()
            res = res.decode()[:len(res)-1]
            print(res)
            res = res.replace("value : ", "")
            degree = int(res.split(',')[0])
            value = int(res.split(',')[1])
            print(degree, value)
            return degree, value
    except Exception as ex:
        print(ex)
        pass
    return -1,-1
######################################################

def animate(k):
    global angleOffset
    degree, value = getDataFunc()
#영역 그리기
    angles[0] = degree/10 #to float
    angles[1] = angles[0]+(3.2/search_max)
    angles[2] = angles[0]+(3.2/search_max)
    angles[3] = angles[0]
#장애물 그리기
    idex = int(degree/8)
    r[idex] = value/10
    theta[idex] = angles[0]+((3.2/search_max)/2)

    ax.cla()
    return updateRadar(),
######################################################

fig = plt.figure(figsize=(5, 5))
fig.set_facecolor('white')

my_palette = plt.cm.get_cmap("Set2", 1)
color = my_palette(0)
data    = [ 20,  20,   0,  20]
angles  = [0.0, 0.2, 0.2, 0.0]

search_max = 4
r       = [0   for i in range(search_max)]
theta   = [0.0 for i in range(search_max)]
area = 120
colors = theta

angleOffset = False

ax = plt.subplot(1, 1, 1, polar=True)
line = updateRadar()
anim = animation.FuncAnimation(
                                fig, 
                                animate, 
                                init_func=lambda:line, 
                                interval=100)
plt.show()
