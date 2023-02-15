'''
This class will contain all the calculations for the breastshot turbine

Initialise the class with the dimensions of the turbine and a river object

The class contains methods to calculate:
- bucket mass at each theta for the bucket model
- torque at each theta
- the impulse force at each theta
- the power variation due to the position of the turbine


Parameters:
radius - float: radius of the turbine
num_blades - int: number of blades on the turbine
max_bucket - float: maximum mass of the bucket
width - float: width of the turbine
x_centre - float: x coordinate of the centre of the turbine
y_centre - float: y coordinate of the centre of the turbine
river - object: river object containing the river parameters

Methods:
find_intersects - calculates the coordinates of the intersects between the
                    river and the radius of the turbine
find_theta_range - calculates the range of useful theta
find_bucket_mass - calculates the mass of the bucket at each theta
find_torque - calculates the torque at each theta
find_momentum - calculates the impulse force transfered at each theta
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
        return 0
    
    def find_theta_range(self):
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
        return 0

    # calculate the mass of the bucket at each theta and the max_bucket volume
    def find_bucket_mass(self):
        # the maximum volume of water that can be stored in the turbine scales with the river width
        if self.river.width > self.width:
            self.max_bucket = self.max_bucket
        else:
            self.max_bucket = 8 * (self.river.width / self.width)

        # calculate the mass of the bucket at each theta
        self.bucket_mass_list = []
        for theta in self.theta:
            # assumes that 
            if theta < math.pi/4:
                mass = (self.max_bucket)/((math.pi/4)-self.theta_entry)* theta
                self.bucket_mass_list.append(mass)
                
            else:
                mass = self.max_bucket - ((self.max_bucket/(self.theta_exit-(math.pi/4))))* (self.theta_exit-theta)
                self.bucket_mass_list.append(mass)
        return 0

                                             
    def find_torque(self):
        # calculate torque at each theta
        torque = []
        # calculate torque at each theta
        for i, angle in enumerate(self.theta):
            torque_val = self.bucket_mass_list[i] * self.radius * np.sin(angle) * self.g
            torque.append(torque_val)

        self.torque_list = torque
        return 0

    # calculate change in momentum at each theta
    def find_momentum(self):
        self.mom_list = []
        river = self.river
        # find the x_nappe value at the point where y_nappe is closest to the turbine centre
        y_diff = min(river.y_nappe, key=lambda x:abs(x-self.y_centre))
        x_interest = river.x_nappe[river.y_nappe == y_diff]

        # calculate distance between nappe flow and turbine centre
        hor_dist = abs(x_interest - self.x_centre)

        for i, angle in enumerate(self.theta):

            fall_height = abs(self.y_centre +  self.radius * np.cos(angle))

            # calculate velocity of nappe flow at each theta
            flow_velocity = ((river.velocity)**2 + (river.g * fall_height * 2))**0.5

            # calculate momentum transfer as a fraction of the contact area
            mom_transfer = abs((1 - (hor_dist/self.radius)) * river.vol_flow_rate * flow_velocity/river.velocity)

            # the rotational momentum transfer is momentum transfer * radius - which will be the average impact radius
            avg_impact_radius = self.radius - (self.radius - hor_dist)/2
            rot_mom_transfer = mom_transfer * avg_impact_radius

            self.mom_list.append(rot_mom_transfer)
        return 0
    
        ''' 
        Here maybe calculate the proportion of the river that misses the turbine,
        and then use that to get a more accurate momentum transfer
        '''

    def find_power(self, RPM):
        # the total power at each theta is the sum of the momentum and torque forces
        # multiplied by the rotational speed RPM
        # torque, mom in units [N m ---- kg m^2 / s^2]
        # power outputted in units [W --- kg m^2 / s^3]
        # the rotational speed must therefore be given in [rad / s]
        rot_speed = (RPM / 60) * 2 * math.pi

        power = []
        # sum together the torque and momentum contributions and multiply by rotation
        for i, mom in enumerate(self.mom_list):
            power.append((mom + self.torque_list[i]) * rot_speed)

        self.output_power_list = power
        self.max_power = max(power)
        self.avg_power = np.mean(power)

        return 0




        

        

                                