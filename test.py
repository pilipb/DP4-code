import classBreastshot

# Define turbine parameters
radius = 1 # m
num_blades = 3 
x_centre = 100 # m
y_centre = -50 # m

# Define river parameters
width = 10 # m
depth = 1 # m
velocity = 1 # m/s
head = 10 # m

turbine = classBreastshot.breastTurbine(radius, num_blades, x_centre, y_centre)
river = classBreastshot.River(width, depth, velocity, head)

# Calculate the velocities of the turbine in the breast shot
turbine.velocities(head, river.nappe_height, river.v_nappe)

# Calculate the power of the turbine in the breast shot
instant_power = turbine.power(river.volFlowRate, river.rho)
print(instant_power)

# Plot the power output of the turbine as the y_centre is varied from 0 to -10m
import matplotlib.pyplot as plt
import numpy as np

y_centre = np.linspace(0, -10, 100)
power = np.zeros(len(y_centre))

for i in range(len(y_centre)):
    i = int(i)
    turbine.y_centre = y_centre[i]
    turbine.velocities(head, river.nappe_height, river.v_nappe)
    power[i] = turbine.power(river.volFlowRate, river.rho)

plt.plot(y_centre, power)
plt.xlabel('y_centre (m)')
plt.ylabel('Power (W)')
plt.show()






