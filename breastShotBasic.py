import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Definitions of the turbine

g = 9.81
rho = 1.0

# River
v_channel = 2
b_channel = 2
d_channel = 0.5

flow_rate = d_channel * b_channel * v_channel

# Nappe

nappe_coeff = 1.69
nappe_height = (flow_rate / (nappe_coeff * g**1/2 * b_channel)) ** (2/3)
v_nappe = flow_rate/(b_channel * nappe_height)

# Turbine

x_centre, y_centre = 100, -50
fall_dist = 20
radius = 0.585
num_blades = 6
mass_bucket = 8


# Calculations for KE

v_vert = (2 * g * (fall_dist + nappe_height/2)) ** 0.5
v_tan = (v_nappe**2 + v_vert**2) ** 0.5

power_KE = 0.5 * flow_rate * rho * v_tan**2

# Static PE calculations

torque = mass_bucket * g * radius
power_PE = torque * v_tan

# Instantaneous power

power = power_KE + power_PE

# v_tan as a function of theta

theta = np.linspace(0, 2*np.pi, 1000)
v_tan_changing = (v_nappe**2 + (2 * g * (fall_dist + nappe_height/2 * np.cos(theta))) ** 2) ** 0.5

print("Power: ", power)
print("Power KE: ", power_KE)
print("Power PE: ", power_PE)

# plot the trajectory of the water and the centre of the turbine

# x speed is constant and equal to v_nappe
# y speed is not constant and increases with gravity

x = np.linspace(0, 200, 1000)
y = -0.5 * g * (x / v_nappe)**2 

plt.plot(x, y)
plt.plot(x_centre, y_centre, 'ro')

# plot circle for turbine

circle = plt.Circle((x_centre, y_centre), radius, color='r', fill=False)
plt.gcf().gca().add_artist(circle)

# make axes the same scale

plt.xlim(-10,200)
plt.ylim(-200, 10)


plt.show()

# plot the power output as a function of theta

plt.plot(theta, power_KE + torque * v_tan_changing)
plt.show()







