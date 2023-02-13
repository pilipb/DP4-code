'''
This class will contain all the calculations for the breastshot turbine

Initialise the class with the dimensions of the turbine and a river object

The class contains methods to calculate:
- bucket mass at each theta for the bucket model
- torque at each theta
- the impulse force at each theta
- the power variation due to the position of the turbine

input parameters:

param: radius - float: radius of the turbine
param: num_blades - int: number of blades on the turbine
param: max_bucket - float: maximum mass of the bucket
param: width - float: width of the turbine
param: x_centre - float: x coordinate of the centre of the turbine
param: y_centre - float: y coordinate of the centre of the turbine
param: river - object: river object containing the river parameters

methods:
bucket_mass - calculates the mass of the bucket at each theta
torque - calculates the torque at each theta
impulse - calculates the impulse force at each theta
power - calculates the power variation due to the position of the turbine

return:
- bucket_mass - array: mass of the bucket at each theta
- torque - array: torque at each theta
- impulse - array: impulse force at each theta
- power - array: power variation due to the position of the turbine

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import math

class breastTurbine():
    # constructor
    def __init__(self, radius, width, num_blades, max_bucket, x_centre, y_centre, river):
        self.radius = radius
        self.width = width
        self.num_blades = num_blades
        self.max_bucket = max_bucket
        self.x_centre = x_centre
        self.y_centre = y_centre
        self.river = river

        self.theta = np.linspace(0, 2 * np.pi, 100)
        self.x = self.radius * np.cos(self.theta) + self.x_centre
        self.y = self.radius * np.sin(self.theta) + self.y_centre

        self.g = 9.81

    def find_intersects(self):
        # find the intersection of the turbine and the river
        # find the x and y coordinates of the intersection
        x_intersect = []
        y_intersect = []
        for i in range(len(self.x)):
            if self.y[i] > self.river.y_bed[i]:
                x_intersect.append(self.x[i])
                y_intersect.append(self.y[i])

        self.x_intersect = x_intersect
        self.y_intersect = y_intersect
    
    def theta_range(self):
        # calculate theta_entry and theta_exit
        
        # check that theta_entry is less than pi/2
        try:
            if self.x_intersect[0] > self.x_centre:
                theta_entry = 0
            else:
                theta_entry = np.arctan(abs(self.x_centre - self.x_intersect[0]) / abs(turbine.y_centre - y_intersect[0]))
        except IndexError:
            print('No intersection found')
            return 1
        
        # check that theta_exit is less than pi
        try:
            if self.x_intersect[-1] > self.x_centre:
                theta_exit = math.pi
            else:
                theta_exit = math.pi - np.arctan(abs(self.x_centre - self.x_intersect[-1]) / abs(turbine.y_centre - y_intersect[-1]))
        except IndexError:
            print('No intersection found')
            return 1
        # calculate torque at each theta
        self.theta = np.linspace(theta_entry, theta_exit, 100)
        self.theta_entry = theta_entry
        self.theta_exit = theta_exit

    # calculate the mass of the bucket at each theta
    def bucket_mass(self):
        # the maximum volume of water that can be stored in the turbine scales with the river width
        if self.river.width > self.width:
            self.max_bucket = self.max_bucket
        else:
            self.max_bucket = 8 * (self.river.width / self.width)

        # calculate the mass of the bucket at each theta
        for theta in self.theta:
            # assumes that 
            if theta < math.pi/4:
                mass = (self.max_bucket)/((math.pi/4)-self.theta_entry)* theta
                return mass
            else:
                mass = self.max_bucket - ((self.max_bucket/(self.theta_exit-(math.pi/4))))* (self.theta_exit-theta)
                return mass