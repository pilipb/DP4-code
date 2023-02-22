'''
This class will contain all the calculations for the breastshot turbine

Initialise the class with the dimensions of the turbine and a river object

The class contains methods to calculate:
- torque at each theta
- the impulse force at each theta
- the power variation due to the position of the turbine


Parameters:
radius - float: radius of the turbine
num_blades - int: number of blades on the turbine
width - float: width of the turbine
x_centre - float: x coordinate of the centre of the turbine
y_centre - float: y coordinate of the centre of the turbine
river - object: river object containing the river parameters

Methods:
find_intersects - calculates the coordinates of the intersects between the
                    river and the radius of the turbine
find_theta_range - calculates the range of useful theta
find_torque - calculates the torque at each theta
find_momentum - calculates the impulse force transfered at each theta
power - calculates the power variation due to the position of the turbine

return:
torque - array: torque at each theta
impulse - array: impulse force at each theta
power - array: power variation due to the position of the turbine

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import math

class breastTurbine():
    # constructor
    def __init__(self, radius, width, num_blades, x_centre, y_centre, river, hyperparams = [1,1,1]):
        a,b,c = hyperparams
        self.a = a
        self.b = b
        self.c = c

        self.radius = radius
        self.width = width
        self.num_blades = num_blades
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

        # intersection occurs when both the x and y differences between the turbine and river are approximately 0
        for i, xval in enumerate(self.river.x_nappe):
            for j, xxval in enumerate(self.x):
                if abs(xval - xxval) < 0.1:
                    if abs(self.y[j] - self.river.y_nappe[i]) < 0.1:
                        x_intersect.append(self.x[j])
                        y_intersect.append(self.y[j])

        self.x_intersect = x_intersect
        self.y_intersect = y_intersect
        return 0
    
    def find_theta_range(self):
        # calculate theta_entry and theta_exit
        
        # check that theta_entry is less than pi/2
        try:
            if self.x_intersect[0] > self.x_centre:
                theta_entry = 0
            if self.y_intersect[0] < self.y_centre:
                theta_entry = math.pi/2
            else:
                theta_entry = np.arctan(abs(self.x_centre - self.x_intersect[0]) / abs(self.y_centre - self.y_intersect[0]))
        except IndexError:
            print('No intersection found')
            return 1
        
        # check that theta_exit is less than pi
        try:
            if self.x_intersect[-1] > self.x_centre:
                theta_exit = math.pi
            else:
                theta_exit = math.pi + np.arctan(abs(self.x_centre - self.x_intersect[-1]) / abs(self.y_centre - self.y_intersect[-1]))
        except IndexError:
            print('No intersection found')
            return 1
        # calculate torque at each theta
        self.theta = np.linspace(theta_entry, theta_exit, 100)
        self.theta_entry = theta_entry
        self.theta_exit = theta_exit
        return 0
                                          
    def find_torque(self):
        '''
        From the CAD model, the mass of the water in the bucket, COM and therefore the torque has been calculated
        and is stored in a csv file. This function approximates the torque at each theta with a quadratic function.
        '''
        # calculate torque at each theta
        torque = []

        # calculated constants for the quadratic function - check water_mass.ipynb
        a = -21.434243694584918 * self.a
        b = 51.40072117993826 * self.b
        c = -24.83940255011645 * self.c

        # calculate torque at each theta
        for i, angle in enumerate(self.theta):
            torque_val = a*(angle**2) + b*angle + c
            if torque_val < 0:
                torque_val = 0
            torque.append(torque_val)

        self.torque_list = torque
        self.torque_angle = self.theta
        return 0

    # calculate change in momentum at each theta
    def find_momentum(self):
        '''
        assume that the momentum change occurs in the same range as the torque
        calculate the area of the blade in contact with the water at each theta
        calculate the velocity of the water at each theta
        calculate the change in momentum at each theta

        the incoming start angle will be calculated as the angle at which the river.x_nappe, river.y_nappe
        first intersects with the turbine radius and the exit angle will always be pi

        '''

        # loop through the river coordinates and find the point closest to the turbine centre
        distance = 10
        for i in range(len(self.river.x_nappe)):
            dist = np.linalg.norm(np.array([self.river.x_nappe[i], self.river.y_nappe[i]]) - np.array([self.x_centre, self.y_centre]))
            if dist < distance:
                distance = dist
                incoming_point = [self.river.x_nappe[i], self.river.y_nappe[i]]
            
        # calculate the angle at which the incoming point is located
        incoming_angle = np.arctan((self.x_centre - incoming_point[0]) / ( incoming_point[1] - self.y_centre))

        # calculate the area of the blade in contact with the water at each theta
        blade_area = []

        # theta range is the range of angles between the incoming angle and pi
        theta_range = np.linspace(incoming_angle, np.pi, 100)

        diff = self.theta_entry -  incoming_angle

        for _ , angle in enumerate(theta_range-incoming_angle - diff):
            blade_area.append(self.width * self.radius * np.sin(angle))

        mom_list = []
        # calculate the velocity of the water at each theta
        for i, angle in enumerate(self.theta):

            fall_height = (abs(self.y_centre) -  self.radius * np.cos(angle))
            # calculate velocity of nappe flow at each theta
            flow_velocity = ((self.river.velocity)**2 + (self.g * fall_height * 2))**0.5

            # calculate momentum transfer as the  A * rho * v
            momentum = blade_area[i] * self.river.rho * flow_velocity

            # if momentum is negative, set to 0
            if momentum < 0:
                momentum = 0

            # append to list
            mom_list.append(momentum)

        self.mom_list = mom_list
        self.mom_angle = self.theta

        return 0

    def find_power(self, RPM):
        # the total power at each theta is the sum of the momentum and torque forces
        # multiplied by the rotational speed RPM
        # torque, mom in units [N m ---- kg m^2 / s^2]
        # power outputted in units [W --- kg m^2 / s^3]
        # the rotational speed must therefore be given in [rot / s]
        RPM = float(RPM) * self.c
        rot_speed = (RPM / 60) 
        self.RPM = RPM

        power = []
        # sum together the torque and momentum contributions and multiply by rotation accounting for different angles
        for i, angle in enumerate(self.theta):
            power.append((self.torque_list[i] + self.mom_list[i]) * rot_speed )

        self.output_power_list = power


        return 0
    
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
            for i, angle in enumerate(self.theta):
                # find the index of the power at each angle
                idx =  i + (blade * 100)
                # find the power at each angle
                summed_power[idx] += self.output_power_list[i]

        self.avg_power_list = summed_power 
        self.avg_power_angle = np.linspace(0, 2*np.pi, 100 * self.num_blades)

        # make nan values 0
        summed_power = np.nan_to_num(summed_power)

        # calculate the average power
        self.avg_power = np.sum(summed_power) / (time  * 100)



        return 0
    
    def analysis(self,x_centre,y_centre, RPM , hyperparams=[1,1,1]):
        '''
        Run the analysis for the turbine at the given RPM
        '''
        self.x_centre = x_centre
        self.y_centre = y_centre
        self.hyperparams = hyperparams
        self.find_intersects()
        self.find_theta_range()
        self.find_torque()
        self.find_momentum()
        self.find_power(RPM)
        self.find_average_power()
        return self.avg_power




                                