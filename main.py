from classes import *
import numpy as np
import matplotlib.pyplot as plt
import timeit

fig, axs = plt.subplots()
fig.show()
axs.clear()
axs.axis('equal')


dt = 0.1
n = 60
radials        = np.linspace(0.2, 3.1, n)
eccentricities = np.linspace(0.03, 0.63, n)
rotations      = np.linspace(0, 4.2*3.1416, n)

ellipses = []
stars = []
largest_sma = 0

for i in range(n):
    r, e, rot = radials[i], eccentricities[i], rotations[i]
    ellipse = Ellipse(r, e, rot)

    if ellipse.semi_major > largest_sma:
        largest_sma = ellipse.semi_major
    xy = ellipse.perimeter
    # axs.plot(xy[0], xy[1], color='black')

    for j in range(130):
        star = Star(ellipse)
        stars.append(star)

    ellipses.append(ellipse)

for star in stars:
    star.r_norm = largest_sma


times = []
for i in range(180):
    toc = timeit.default_timer()

    # use arrays to store positions instead of drawing each star individually, speed up by 3.5x
    x = np.empty(len(stars))
    y = np.empty(len(stars))

    for i, star in enumerate(stars):
        star.move(dt)
        xy = star.get_pos()
        x[i], y[i] = xy[0], xy[1]

    ln = axs.scatter(x, y, color='red', s=0.5)
    fig.canvas.draw()
    fig.canvas.flush_events()

    tic = timeit.default_timer()
    
    time = 1000*round(tic-toc, 6)
    times.append(time)
    print(f"frame time: {time}ms")

    ln.remove()

print(f"avg frame time: {round(np.mean(times), 5)}ms")