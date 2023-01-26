import classBreastshot
import matplotlib.pyplot as plt

# Define turbine parameters
radius = 1 # m
num_blades = 3 
x_centre = 5 # m
y_centre = -1 # m

# Define river parameters
width = 10 # m
depth = 1.5 # m
velocity = 3 # m/s
head = 10 # m

turbine = classBreastshot.breastTurbine(radius, num_blades, x_centre, y_centre)
river = classBreastshot.River(width, depth, velocity, head)


'''Plot the turbine and river flow'''
# plot the flow of the river at the height of river bed and nappe
x_bed, y_bed, x_nappe, y_nappe = river.plotRiver()
plt.plot(x_bed, y_bed, 'b-')
plt.plot(x_nappe, y_nappe, 'b-')

# line that is parallel to the river bed
plt.plot([-5,0], [0, 0], 'k')
# line that is parallel to the nappe height
plt.plot([-5,0], [river.nappe_height, river.nappe_height], 'k')
# line that is parallel to the bottom of the waterfall (head)
plt.plot([-5,max(x_nappe)], [-river.head, -river.head], 'k')

# plot the turbine
x_turbine, y_turbine = turbine.plotTurbine()
plt.plot(x_turbine, y_turbine, 'b-')
# plot centre of turbine
plt.plot(turbine.x_centre, turbine.y_centre, 'ro')

plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.show()

# calculate how much water enters the turbine
# turbine.volume(river.width, river.depth, river.velocity, river.head)

# Calculate the velocities of the turbine in the breast shot
turbine.velocities(head, river.nappe_height, river.v_nappe)

# Calculate the power of the turbine in the breast shot
instant_power = turbine.power(river.volFlowRate, river.rho)
print(instant_power)

# Plot the power output of the turbine as the y_centre is varied from 0 to -10m
import matplotlib.pyplot as plt
import numpy as np

for y_centre in range(0, -50, -1):
    turbine = classBreastshot.breastTurbine(radius, num_blades, x_centre, y_centre)
    turbine.velocities(head, river.nappe_height, river.v_nappe)
    instant_power = turbine.power(river.volFlowRate, river.rho)
    plt.plot(y_centre, instant_power, 'ro')
    

plt.xlabel('y_centre')
plt.ylabel('Power (W)')
# plt.show()

# now need to account for how much water enters the turbine which is effected by the x_centre











