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
        self.drag_coeff = 2.3 # from consultancy report
        self.blade_width = width # from CAD

        # depth of turbine below water surface
        self.sub_depth = y_centre - radius
        self.unsub_depth = y_centre

        # find the intersection angles of the turbine and the river
        self.alpha1 = np.arcsin(self.unsub_depth / radius)
        self.alpha2 = math.pi - self.alpha1

    def find_eff_depth(self, alpha, y_centre):

        depth = abs(self.radius*np.sin(alpha)) - y_centre

        if depth < 0:
            depth = 0
        elif depth > 0.335: # max depth of turbine
            depth = 0.335
        elif depth > self.river.depth: # max depth of river
            depth = self.river.depth

        return depth

        

    def find_drag_force(self, depth):
        return 0.5 * self.river.rho * self.river.velocity**2 * self.drag_coeff * self.blade_width * depth

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

        self.RPM = RPM

        angular_v = (RPM * 2 * math.pi) / 60 # convert RPM to rad/s

        self.find_drag_list()

        power = self.force * angular_v * self.radius

        self.power_list = power


    def find_average_power(self):
        '''
        Average power is calculated by summing the power over one rotation of the turbine
        and dividing by the time taken to complete one rotation. This will account for the
        number of blades.

        '''

        # calculate the time taken to complete one rotation
        time = (self.RPM / 60)**-1 # seconds per rotation

        # overlay the power curve for a rotation
        summed_power = np.zeros(100 * self.num_blades)
        for blade in range(self.num_blades):
            for i, angle in enumerate(self.theta_list):
                # find the index of the power at each angle
                idx =  i + (blade * 100)
                # find the power at each angle
                summed_power[idx] += self.power_list[i]

        self.avg_power_list = summed_power 
        self.avg_power_angle = np.linspace(0, 2*np.pi, 100 * self.num_blades)

        # make nan values 0
        summed_power = np.nan_to_num(summed_power)

        # calculate the average power
        self.avg_power = np.sum(summed_power) / (time  * 100)

        return 0
    
    def analysis(self,y_pos, RPM):
        self.y_centre = y_pos
        self.find_power(RPM)
        self.find_average_power()

        return 0


