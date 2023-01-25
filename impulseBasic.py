import matplotlib.pyplot as plt
import numpy as np

# Definitions of the turbine

# constants
g = 9.81
rho = 1.0

# River
v_channel = 10
b_channel = 10
d_channel = 10

flow_rate = d_channel * b_channel * v_channel

# Turbine
radius = 80
num_blades = 10
x_centre, y_centre = 100, 50

# velocities

V_initial = v_channel
u_wheel = 0.5 * V_initial # optimal

# Power

power = 2 * rho * flow_rate * (V_initial - u_wheel) * u_wheel

print(power)

# plot flow 

x = np.linspace(0, 200, 1000)
y = np.linspace(0, 0, 1000)

plt.plot(x, y, 'b')
plt.plot(x_centre, y_centre, 'ro')

# plot circle for turbine

theta = np.linspace(0, 2*np.pi, 1000)
x_circle = radius * np.cos(theta) + x_centre
y_circle = radius * np.sin(theta) + y_centre

plt.plot(x_circle, y_circle, 'r')

plt.show()
