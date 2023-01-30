import numpy as np
import matplotlib.pyplot as plt

class breastTurbine():
    # constructor
    def __init__(self, radius, num_blades, x_centre, y_centre):
        self.radius = radius
        self.num_blades = num_blades
        # self.bucket_mass = 8
        self.g = 9.81
        self.x_centre = x_centre
        self.y_centre = y_centre

    # plot centre and radius of turbine
    def plotTurbine(self):

        # plot radius of turbine
        theta = np.linspace(0, 2 * np.pi, 100)
        x = self.radius * np.cos(theta) + self.x_centre
        y = self.radius * np.sin(theta) + self.y_centre

        return x, y

    # methods - for calculating rotational velocity
    def velocities(self, head, nappe_height,v_nappe):
        
        self.v_vert = (2 * self.g * abs(head + (nappe_height/2) + self.y_centre)) ** 0.5
        self.v_tan = (v_nappe**2 + self.v_vert**2) ** 0.5
        return self.v_vert, self.v_tan

    # methods - for calculating power
    def power(self, flow_rate, rho):
        self.power_KE = 0.5 * flow_rate * rho * self.v_tan**2

        torque = self.bucket_mass * self.g * self.radius
        self.power_PE = torque * self.v_tan 

        self.power = self.power_KE + self.power_PE
        return self.power  

   
class River():
    # constructor
    def __init__(self, width, depth, velocity, head):
        self.width = width
        self.depth = depth
        self.velocity = velocity
        self.head = head
        self.volFlowRate = width * depth * velocity

        self.kPower = self.volFlowRate**2 / 2
        self.pPower = self.volFlowRate * head * 9.81
        self.totalPower = self.kPower + self.pPower

        self.nappeC = 1.69
        self.g = 9.81
        self.rho = 1
        self.nappe_height = (self.volFlowRate / (self.nappeC * self.g**1/2 * self.width)) ** (2/3)
        self.v_nappe = self.volFlowRate/(self.width * self.nappe_height)

    # methods - for plotting the river flow
    def plotRiver(self):
        # plot points using suvats for river at bed and nappe parametrically for time
        calcT = np.sqrt(2 * self.head / self.g)
        # define time
        t = np.linspace(0, calcT, 1000)

        # define x and y coordinates
        x_bed = self.velocity * t
        y_bed = np.zeros(len(t)) - 0.5 * self.g * t**2
        x_nappe = self.v_nappe * t
        y_nappe = self.nappe_height * np.ones(len(t)) - 0.5 * self.g * t**2

        # return the equations of the river bed and nappe flows
        return x_bed, y_bed, x_nappe, y_nappe

def plotEverything(river, turbine):
    # plot the flow of the river at the height of river bed and nappe
    x_bed, y_bed, x_nappe, y_nappe = river.plotRiver()
    # plt.plot(x_bed, y_bed, 'b-')
    # plt.plot(x_nappe, y_nappe, 'b-')

    # line that is parallel to the river bed
    # plt.plot([-5,0], [0, 0], 'k')
    # line that is parallel to the nappe height
    # plt.plot([-5,0], [river.nappe_height, river.nappe_height], 'k')
    # line that is parallel to the bottom of the waterfall (head)
    # plt.plot([-5,max(x_nappe)], [-river.head, -river.head], 'k')

    # plot the turbine
    x_turbine, y_turbine = turbine.plotTurbine()
    # plt.plot(x_turbine, y_turbine, 'g-')
    # plot centre of turbine
    # plt.plot(turbine.x_centre, turbine.y_centre, 'ro')

    # calculate points of intersection between turbine radius and nappe flow
    x_intersect = []
    y_intersect = []
    for i in range(len(x_nappe)):
        if (x_nappe[i] - turbine.x_centre)**2 + (y_nappe[i] - turbine.y_centre)**2 <= turbine.radius**2:
            x_intersect.append(x_nappe[i])
            y_intersect.append(y_nappe[i])

    # plot the first, last and middle intersection points
    try:
        # plt.plot(x_intersect[0], y_intersect[0], 'ro')
        # plt.plot(x_intersect[-1], y_intersect[-1], 'ro')
        # plt.plot(x_intersect[int(len(x_intersect)/2)], y_intersect[int(len(x_intersect)/2)], 'ro')


        # calculate and plot the radius straight line from the centre of the turbine to the middle intersection point
        m = (y_intersect[int(len(x_intersect)/2)] - turbine.y_centre) / (x_intersect[int(len(x_intersect)/2)] - turbine.x_centre)
        c = turbine.y_centre - m * turbine.x_centre
        x_radius = np.linspace(turbine.x_centre, x_intersect[int(len(x_intersect)/2)], 1000)
        y_radius = m * x_radius + c
        # plt.plot(x_radius, y_radius, 'r-')


        # plt.xlabel('x (m)')
        # plt.ylabel('y (m)')
        # plt.show()

    except:
        pass




    return x_bed, y_bed, x_nappe, y_nappe, x_turbine, y_turbine, x_intersect, y_intersect
        

'''
# Turbine

x_centre, y_centre = 100, -50
fall_dist = 20



# Calculations for KE

v_vert = (2 * g * (fall_dist + nappe_height/2)) ** 0.5
v_tan = (v_nappe**2 + v_vert**2) ** 0.5

power_KE = 0.5 * flow_rate * rho * v_tan**2

# Static PE calculations

torque = mass_bucket * g * radius
power_PE = torque * v_tan

# Instantaneous power

power = power_KE + power_PE

'''