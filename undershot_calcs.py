# import modules
import numpy as np
import matplotlib.pyplot as plt
import math

class underTurbine():
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
    barrel_radius - float: radius of the barrel

    Methods:
    find_eff_depth - calculates the effective depth of the turbine
    find_drag_force - calculates the drag force on the turbine
    find_drag_list - calculates the drag force on the turbine for each theta
    find_power - calculates the power at each theta for a given RPM

    Return:
    force - array: drag force at each theta
    power_list - array: power at each theta for a given RPM

    '''
    # constructor
    def __init__(self,  river, RPM = 15, radius = 0.504, barrel_radius=0.169,  width = 1.008, num_blades = 6,  y_centre = 0):
        self.radius = radius
        self.width = width
        self.num_blades = num_blades
        self.y_centre = y_centre
        self.x_centre = 2
        self.barrel_radius = barrel_radius

        self.max_depth = radius - barrel_radius

        self.river = river
        self.g = 9.81
        self.drag_coeff = 2.3 # from consultancy report
        self.blade_width = width # from CAD

        self.blade_sep = 2 * np.pi / num_blades

        self.RPM = RPM
        self.omega = (RPM * 2 * math.pi) / 60 # convert RPM to rad/s

        # for drawing
        self.theta = np.linspace(0, 2 * np.pi, 100)
        self.x = self.radius * np.cos(self.theta) + self.x_centre
        self.y = self.radius * np.sin(self.theta) + self.y_centre

        # dtheta/dt
        dtheta = self.theta[1] - self.theta[0]
        dt = (60/RPM) / len(self.theta)
        self.dthetadt = dtheta / dt


        # depth of turbine below water surface
        self.sub_depth = y_centre - radius
        self.unsub_depth = y_centre

        # find the intersection angles of the turbine and the river
        self.alpha1 = np.arcsin(self.unsub_depth / radius)
        self.alpha2 = math.pi - self.alpha1

    def find_eff_depth(self, theta):

        # theta is the angle of the turbine blade from the vertical

        if theta < self.alpha1 or theta > self.alpha2:
            return 0
        
        # y centre is the height of the centre of the turbine above the water surface
        depth = self.radius * np.sin(theta - np.pi/2) - self.y_centre

        # check if the turbine is submerged
        if depth > self.max_depth: # max depth of turbine
            depth = self.max_depth

        return depth
    
    def flow_velocity(self, theta):
        v = self.river.velocity - self.omega * self.radius * np.sin(theta)
        return v

    def find_drag_force(self, depth, theta):
        v = self.flow_velocity(theta)
        area = self.blade_width * (depth - depth*np.cos(theta)) * np.sin(theta - self.blade_sep)# account for blocking
        return self.river.rho * v**2 * self.drag_coeff * area * self.dthetadt

    def find_drag_list(self):
        force_list = []
        
        for theta in self.theta:

            # check if the turbine is submerged
            if theta < self.alpha1 or theta > self.alpha2:
                force_list.append(0)
                continue
            else:

                depth = self.find_eff_depth(theta)

                if depth > 0:
                    drag = self.find_drag_force(depth, theta)
                    force_list.append(drag)
                else:
                    force_list.append(0)

        self.force_list = np.array(force_list )

    def find_centre_mass(self):
        '''
        the centre of mass of water is approximated from the CAD model by f(theta) = a*theta^4 + b*theta^3 + c*theta^2 + d*theta + e
        '''
        # constants for the quadratic function - found by fitting the CAD model
        a = 0.7732178173079596
        b = -4.808504916068159
        c = 10.468692683694396
        d = -9.42560937714108
        e = 3.19372668997763

        # calculate the centre of mass at each theta
        centre_mass = np.zeros(len(self.theta))

        for i, theta in enumerate(self.theta):

            if theta >= self.alpha1 and theta <= self.alpha2:
                theta = theta - np.pi/2

                centre_mass[i] = (a*(theta**4) + b*(theta**3) + c*(theta**2) + d*theta + e)
            else:
                centre_mass[i] = 0

        self.centre_mass = centre_mass
        return 0

    # calculate instantaneous power for each theta for a given RPM
    def find_power(self):
        power = np.zeros(len(self.theta))
        for i, force in enumerate(self.force_list):
            # find the power at each angle
            p = force * self.omega * self.centre_mass[i] * np.sin(self.theta[i])

            power[i] = p

        self.power_list = power


    def find_average_power(self):
        '''
        Average power is calculated by summing the power over one rotation of the turbine
        and dividing by the time taken to complete one rotation. This will account for the
        number of blades.

        '''

        # calculate the separation angle between the blades
        blade_sep_idx = 100 / self.num_blades

        # compounding the power output of each blade with offset blade_sep_idx
        power = np.zeros(len(self.theta))
        for i in range(self.num_blades):
            power += np.roll(self.power_list, int(i*blade_sep_idx))

        # average the power over one revolution
        avg_power = np.sum(power) / len(power)

        self.avg_power = avg_power / self.num_blades
        self.full_power = power

        return 0
    
    def analysis(self):

        # set the turbine parameters
        self.find_drag_list()
        self.find_centre_mass()
        self.find_power()
        self.find_average_power()

        return self.avg_power




if __name__ == "__main__":

    # test the class
    from river_class import river_obj

    river = river_obj(0.77, 0.5, 2, head=0)

    turbine = underTurbine(river)

    turbine.analysis(0.2, 25)

    # plot the power curve
    plt.figure()
    plt.plot(turbine.theta, turbine.full_power)
    # plot the average power
    plt.plot(turbine.theta, np.ones(len(turbine.theta)) * turbine.avg_power)
    plt.xlabel('theta')
    plt.ylabel('power')
    plt.show()

    # now vary the RPM
    RPM = np.linspace(0, 40, 50)
    power = np.zeros(len(RPM))

    for i, rpm in enumerate(RPM):
        power[i] = turbine.analysis(0.2, rpm)
        
    plt.figure()
    plt.plot(RPM, power)
    plt.xlabel('RPM')
    plt.ylabel('power')
    plt.show()







