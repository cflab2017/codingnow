import matplotlib.pyplot as plt
from math import pi
from matplotlib import animation

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

def animate(k):
    global angleOffset
    if angleOffset:
        for i in range(len(angles)):
            angles[i] -= 0.2
            if(angles[i] < 0):
                angleOffset = False
    else:
        for i in range(len(angles)):
            angles[i] += 0.2
            if(angles[i] > 3.2):
                angleOffset = True
    ax.cla()
    return updateRadar(),
######################################################

fig = plt.figure(figsize=(5, 5))
fig.set_facecolor('white')

my_palette = plt.cm.get_cmap("Set2", 1)
color = my_palette(0)
data = [20, 20, 0, 20]
angles = [0.0, 0.2, 0.2, 0.0]

r = [5, 16]
theta = [1.0, 2.8]#60, 160
area = 120
colors = theta

angleOffset = False

ax = plt.subplot(1, 1, 1, polar=True)
line = updateRadar()
anim = animation.FuncAnimation(
                                fig,
                                animate,
                                init_func=lambda: line,
                                interval=100)
plt.show()
