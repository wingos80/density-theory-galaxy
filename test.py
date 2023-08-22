import matplotlib.pyplot as plt
import numpy as np

def ellipse(radial_distance, eccentricity, rotation=0):
    r_dist, ecc, rot = radial_distance, eccentricity, rotation
    semi_major, semi_minor = np.sqrt(r_dist**2/(1-ecc**2)), r_dist
    t = np.linspace(0, 2*3.1416, 200)
    x = semi_major * np.cos(t)
    y = semi_minor * np.sin(t)
    xy_vector = np.array([x, y])
    rotation_matrix = np.array([[np.cos(rot), -np.sin(rot)], [np.sin(rot), np.cos(rot)]])
    

    x, y = np.matmul(rotation_matrix, xy_vector)

    return x, y, semi_major, semi_minor

fig, axs = plt.subplots()
fig.show()
rot = 0
axs.clear()
axs.axis('equal')

n = 33
radials        = np.linspace(0.5, 3.1, n)
eccentricities = np.linspace(0.03, 0.6, n)
rotations      = np.linspace(0, 2*3.1416, n)

for i in range(n):
    r, e, rot = radials[i], eccentricities[i], rotations[i]
    x, y, sma, _ = ellipse(r, e, rot)
    axs.plot(x, y, color='black')
fig.canvas.draw()
fig.canvas.flush_events()

i = 0
while True:
    x0, y0 = x[i], y[i]
    ln = axs.scatter(x0, y0, color='red')
    fig.canvas.draw()
    fig.canvas.flush_events()
    ln.remove()

    i+=1
    i = i%len(x)
plt.show()