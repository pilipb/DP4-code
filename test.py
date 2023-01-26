import classBreastshot
import matplotlib.pyplot as plt
import numpy as np
import math

# Define turbine parameters
maxVol = 2 # m^3
radius = 0.75 # m
num_blades = 3 
x_centre = 2 # m
y_centre = -1 # m

# Define river parameters
width = 10 # m
depth = 1.5 # m
velocity = 0.5 # m/s
head = 2 # m

turbine = classBreastshot.breastTurbine(radius, num_blades, x_centre, y_centre)
river = classBreastshot.River(width, depth, velocity, head)


'''Plot the turbine and river flow'''
x_bed, y_bed, x_nappe, y_nappe, x_turbine, y_turbine, x_intersect, y_intersect = classBreastshot.plotEverything(river, turbine)


'''Calculating torque'''

# find entry and exit angles
theta_entry = np.arctan(abs(turbine.x_centre - x_intersect[0]) / abs(turbine.y_centre - y_intersect[0]))

# check that theta_exit is less than pi
if x_intersect[-1] > turbine.x_centre:
    theta_exit = math.pi
else:
    theta_exit = math.pi - np.arctan(abs(turbine.x_centre - x_intersect[-1]) / abs(turbine.y_centre - y_intersect[-1]))

# calculate toreuq at each theta
theta1 = np.linspace(theta_entry, math.pi/4, 1000)
theta2 = np.linspace(math.pi/4, theta_exit, 1000)
torque = np.zeros(len(theta1) + len(theta2))
add = len(theta1)

for i, value in enumerate(theta1):
    torque[i] = ((maxVol/((math.pi/4)-theta_entry))* value) * (turbine.radius * np.sin(value))
for i, value in enumerate(theta2):
    torque[add + i] = ((maxVol - ((maxVol/(theta_exit-(math.pi/4))))* (theta_exit-value))) * (turbine.radius * np.sin(value))


# plot torque vs theta
theta = np.concatenate((theta1, theta2))
plt.plot(theta, torque)
plt.xlabel('theta')
plt.ylabel('torque')
plt.show()








