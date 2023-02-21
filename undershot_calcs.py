'''
This class will contain all the calculations for the undershot turbine

Initialise the class with the dimensions of the turbine and a river object

The class contains methods to calculate:
- the impulse force at each theta


Parameters:
radius - float: radius of the turbine
num_blades - int: number of blades on the turbine
width - float: width of the turbine
y_centre - float: y coordinate of the centre of the turbine
river - object: river object containing the river parameters

Methods:
find_eff_depth - calculates the effective depth of the turbine
find_drag_force - calculates the drag force on the turbine
find_drag_list - calculates the drag force on the turbine for each theta
find_power - calculates the power at each theta for a given RPM

Return:
force - array: drag force at each theta
power_list - array: power at each theta for a given RPM

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import math

class underTurbine():
    # constructor
    def __init__(self, radius, width, num_blades,  y_centre, river):
        self.radius = radius
        self.width = width
        self.num_blades = num_blades
        self.y_centre = y_centre

        self.river = river
        self.g = 9.81
        self.drag_coeff = 1.5
        self.blade_width = 0.502

        # depth of turbine below water surface
        self.sub_depth = y_centre - radius
        self.unsub_depth = y_centre

        # find the intersection angles of the turbine and the river
        self.alpha1 = np.arcsin(self.unsub_depth / radius)
        self.alpha2 = math.pi - self.alpha1

    def find_eff_depth(self, alpha, y_centre):
        return abs(self.radius*np.sin(alpha)) - y_centre

    def find_drag_force(self, depth):
        return self.river.rho * self.river.velocity**2 * self.drag_coeff * self.blade_width * depth

    def find_drag_list(self):
        force_list = []
        self.theta_list = np.linspace(self.alpha1, self.alpha2, 100)
        for alpha in self.theta_list:
            depth = self.find_eff_depth(alpha, self.y_centre)

            if depth > 0:
                drag = self.find_drag_force(depth)
                force_list.append(drag)
            else:
                force_list.append(0)

        self.force = np.array(force_list)

    # calculate instantaneous power for each theta for a given RPM
    def find_power(self, RPM):

        angular_v = (RPM * 2 * math.pi) / 60 # convert RPM to rad/s

        self.find_drag_list()

        power = self.force * angular_v * self.radius

        self.power_list = power
