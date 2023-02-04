import classBreastshot
import matplotlib.pyplot as plt
import numpy as np
import math

'''MAKE 3D - make volume a function of river width and turbine width'''
# the maximum volume of water that can be stored in the turbine is 8 m^3
# this is the max vol if the river width is within 10% of the turbine width
# the max vol decreases as the river width decreases

# Define turbine parameters
radius = 0.75 # m
num_blades = 6
x_centre = 2 # m
y_centre = -1 # m
turbWidth = 1 # m

# Define river parameters
width = 10 # m
depth = 1.5 # m
velocity = 0.5 # m/s
head = 2 # m

turbine = classBreastshot.breastTurbine(radius, num_blades, x_centre, y_centre)
river = classBreastshot.River(width, depth, velocity, head)

# check if river is wider than turbine
if river.width > turbWidth:
    maxVol = 8
else:
    maxVol = 8 * (river.width / turbWidth)

'''Plot the turbine and river flow'''
x_bed, y_bed, x_nappe, y_nappe, x_turbine, y_turbine, x_intersect, y_intersect = classBreastshot.plotEverything(river, turbine)

''' Plotting torque vs theta for a given turbine and river flow as a function'''

def torquePlot(turbine, river, x_intersect, y_intersect):
# calculate theta_entry and theta_exit
    '''Calculating torque'''
    # calculate theta_entry and theta_exit
    # check that theta_entry is less than pi/2
    try:
        if x_intersect[0] > turbine.x_centre:
            theta_entry = 0
        else:
            theta_entry = np.arctan(abs(turbine.x_centre - x_intersect[0]) / abs(turbine.y_centre - y_intersect[0]))
    except IndexError:
        print('No intersection found')
        return 1
    # check that theta_exit is less than pi
    try:
        if x_intersect[-1] > turbine.x_centre:
            theta_exit = math.pi
        else:
            theta_exit = math.pi - np.arctan(abs(turbine.x_centre - x_intersect[-1]) / abs(turbine.y_centre - y_intersect[-1]))
    except IndexError:
        print('No intersection found')
        return 1
    # calculate torque at each theta
    theta = np.linspace(theta_entry, theta_exit, 100)
    torque = []

    # define a function to calculate bucket mass given theta
    # this needs to be varied with the distance from the turbine centre
    # let the maximum vloume vary with the distance from the turbine centre

    def bucketMass(theta):

        # def maxVol():
        #     try:
        #         return float(2 - np.sqrt(abs(y_intersect[0] - turbine.y_centre)))
        #     except IndexError:
        #         print('No intersection found')
        #         return 1

        if theta < math.pi/4:
            mass = (maxVol)/((math.pi/4)-theta_entry)* theta
            return mass
        else:
            mass = maxVol - ((maxVol/(theta_exit-(math.pi/4))))* (theta_exit-theta)
            return mass

    # calculate torque at each theta
    for i, angle in enumerate(theta):
        valueTorque = bucketMass(angle) * turbine.radius * np.sin(angle) * river.g
        torque.append(valueTorque)



    return theta, torque

plt.figure()
# plot torque vs theta for 3 different x_centre values
x_centre = 2
for i in range(6):
    x_centre = x_centre + 0.1
    turbine = classBreastshot.breastTurbine(radius, num_blades, x_centre, y_centre)
    x_bed, y_bed, x_nappe, y_nappe, x_turbine, y_turbine, x_intersect, y_intersect = classBreastshot.plotEverything(river, turbine)
    try:
        theta, torque = torquePlot(turbine, river, x_intersect, y_intersect)
        plt.plot(theta, torque, label = 'x_centre = ' + str(x_centre))
    except IndexError:
        print('No intersection found')
        break
    

# # plot torque vs theta
# plt.plot(theta, torque)
# show x labels in radians
plt.legend()
plt.xticks([0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4, 2*math.pi], ['0', '$\pi$/4', '$\pi$/2', '3$\pi$/4', '$\pi$', '5$\pi$/4', '3$\pi$/2', '7$\pi$/4', '2$\pi$'])
plt.ylabel('torque (N.m)')
plt.show()


# calculate impulse force at each theta
# impulse is change in momentum, force is change in momentum per unit time

# calculate change in momentum at each theta
''' 
Momentum transfer from river to turbine

the distance between the nappe flow and the turbine centre at each theta is:

dist = abs((x_nappe[y_nappe = turbine.y_centre] - turbine.x_centre))

mom_transfer = (1 - dist/turbine.radius) *  river.massFlow * river.velocity

river.velocity = river.velocity + sqrt(acceleration due to gravity * fall height * 2)

fall height(at theta) = ycentre + turbine.radius * cos(theta)

'''

# calculate change in momentum at each theta
def momentumTransfer(turbine, river, x_nappe, y_nappe, theta):
    # find the x_nappe value at the point where y_nappe is closest to the turbine centre
    y_diff = min(y_nappe, key=lambda x:abs(x-turbine.y_centre))
    x_interest = x_nappe[y_nappe == y_diff]

    # calculate distance between nappe flow and turbine centre
    horDist = abs(x_interest - turbine.x_centre)
    fallHeight = abs(turbine.y_centre +  turbine.radius * np.cos(theta))

    # calculate velocity of nappe flow at each theta
    flowVelocity = ((river.velocity)**2 + (river.g * fallHeight * 2))**0.5

    # calculate momentum transfer as a fraction of the contact area
    momTransfer = abs((1 - (horDist/turbine.radius)) * river.volFlowRate * flowVelocity/river.velocity)

    # the rotational momentum transfer is momentum transfer * radius - which will be the average impact radius
    avgImpactRadius = turbine.radius - (turbine.radius - horDist)/2
    rotMomTransfer = momTransfer * avgImpactRadius

    return momTransfer, rotMomTransfer

# calculate change in momentum at each theta and plot
momTransfer = []
rotMomTransfer = []
for i, angle in enumerate(theta):
    mom, rotMom = momentumTransfer(turbine, river, x_nappe, y_nappe, angle)
    momTransfer.append(mom)
    rotMomTransfer.append(rotMom)

momTransfer = np.array(momTransfer)
plt.figure()
plt.plot(theta, momTransfer)
plt.xticks([0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4, 2*math.pi], ['0', '$\pi$/4', '$\pi$/2', '3$\pi$/4', '$\pi$', '5$\pi$/4', '3$\pi$/2', '7$\pi$/4', '2$\pi$'])
plt.ylabel('momentum transfer (kg.m/s)')
plt.show()



# plot impulse force vs theta and momentum transfer vs theta with two y axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(theta, torque, 'b-', label='PE Torque')
ax2.plot(theta, rotMomTransfer, 'r-', label = 'KE Mom')
total_torque = []
for i, v in enumerate(torque):
    total_torque.append(v + rotMomTransfer[i])
ax1.plot(theta, total_torque,'k-',label='Total Torque')
ax1.set_xlabel('theta (radians)')
ax1.set_ylabel('torque (N.m)', color='b')
ax2.set_ylabel('rotational momentum transfer (kg.m/s . m)', color='r')
fig.legend()
plt.show()











