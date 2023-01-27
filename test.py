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
# calculate theta_entry and theta_exit
# check that theta_entry is less than pi/2
if x_intersect[0] > turbine.x_centre:
    theta_entry = 0
else:
    theta_entry = np.arctan(abs(turbine.x_centre - x_intersect[0]) / abs(turbine.y_centre - y_intersect[0]))

# check that theta_exit is less than pi
if x_intersect[-1] > turbine.x_centre:
    theta_exit = math.pi
else:
    theta_exit = math.pi - np.arctan(abs(turbine.x_centre - x_intersect[-1]) / abs(turbine.y_centre - y_intersect[-1]))

# calculate toreuq at each theta
theta = np.linspace(theta_entry, theta_exit, 100)
torque = []

# define a function to calculate bucket mass given theta
def bucketMass(theta):
    if theta < math.pi/4:
        mass = maxVol/((math.pi/4)-theta_entry)* theta
        return mass
    else:
        mass = maxVol - ((maxVol/(theta_exit-(math.pi/4))))* (theta_exit-theta)
        return mass


# calculate torque at each theta
for i, angle in enumerate(theta):
    valueTorque = bucketMass(angle) * turbine.radius * np.sin(angle) * river.g
    torque.append(valueTorque)

# plot torque vs theta
plt.plot(theta, torque)

# show x labels in radians
plt.xticks([0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4, 2*math.pi], ['0', '$\pi$/4', '$\pi$/2', '3$\pi$/4', '$\pi$', '5$\pi$/4', '3$\pi$/2', '7$\pi$/4', '2$\pi$'])
plt.ylabel('torque (N.m)')
plt.show()








