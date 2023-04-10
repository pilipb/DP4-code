# import modules
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.optimize as opt
import pandas as pd

class breastTurbine():
    '''
    This class will contain all the calculations for the breastshot turbine

    Initialise the class with the dimensions of the turbine and a river object

    The class contains methods to calculate:
    - torque at each theta
    - the impulse force at each theta
    - the power variation due to the position of the turbine


    Parameters:
    ----------------
        radius - float: radius of the turbine
        num_blades - int: number of blades on the turbine
        width - float: width of the turbine
        x_centre - float: x coordinate of the centre of the turbine
        y_centre - float: y coordinate of the centre of the turbine
        river - object: river object containing the river parameters

    Methods:
    ----------------
        find_intersects - calculates the coordinates of the intersects between the
                            river and the radius of the turbine
        find_theta_range - calculates the range of useful theta
        find_filling_rate - calculates the filling rate of the turbine at each theta
        find_vol - calculates the volume of water in the turbine bucket at each theta
        find_centre_mass - calculates the centre of mass of the water at each theta (moment arm)
        find_pot_power - calculates the potential power of the turbine at each theta
        find_imp_power - calculates the impulse power of the turbine at each theta
        find_tot_power - calculates the total power of the turbine at each theta

    Returns:
    ----------------
        pot_power - array: the potential power of the turbine at each theta
        imp_power - array: the impulse power of the turbine at each theta
        tot_power - array: the total power of the turbine at each theta
        theta_range - array: the range of useful theta
        vol - array: the volume of water in the turbine bucket at each theta

    '''

    def __init__(self, river, radius = 0.504, width = 1.008, num_blades = 6, x_centre = 0, y_centre = 0, RPM=15): 

        self.radius = radius
        self.width = width
        self.num_blades = num_blades
        self.river = river
        self.x_centre = x_centre 
        self.y_centre = y_centre 
        self.RPM = RPM

        self.blade_sep = 2*np.pi/self.num_blades
        

        self.theta = np.linspace(0, 2*np.pi, 100)
        self.x = self.radius * np.cos(self.theta) + self.x_centre
        self.y = self.radius * np.sin(self.theta) + self.y_centre

        self.g = 9.81
        self.max_vol = 0.032 # m^3

        omega = 2 * np.pi * RPM / 60

        # calculate dtheta/dt
        dtheta = self.theta[1] - self.theta[0]
        dt = (60/RPM) / len(self.theta)
        self.dthetadt = dtheta / dt


    def find_intersects(self):
        # find the intersection of the turbine and the river
        # find the x and y coordinates of the intersection and the corresponding angles
        x_intersect = []
        y_intersect = []

        # intersection occurs when both the x and y differences between the turbine and river are approximately 0
        for i, xval in enumerate(self.river.x_nappe):
            for j, xxval in enumerate(self.x):
                if abs(xval - xxval) < 0.1 and abs(self.y[j] - self.river.y_nappe[i]) < 0.1:
                    x_intersect.append(self.x[j])
                    y_intersect.append(self.y[j])

        self.x_intersect = x_intersect
        self.y_intersect = y_intersect
        return 0
    
    def find_theta_range(self):
        # calculate theta_entry and theta_exit (alpha 1,2)
 
        
        # check that theta_entry is less than pi/2
        try:
            if self.x_intersect[0] > self.x_centre: # if the river intersection over shoots the turbine
                theta_entry = 0
            if self.y_intersect[0] < self.y_centre: # if the turbine centre is above the river intersection
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
        
        # calculate the theta range
        self.theta_entry = theta_entry
        self.theta_exit = theta_exit
        self.theta_range = theta_exit - theta_entry
        return 0

    
    def find_filling_rate(self):
        '''
        calculate the filling rate of the bucket at each theta and emptying rate
        '''
        filling_rate = np.zeros(len(self.theta))
        RPM = self.RPM

        # calculate the angular velocity of the turbine in radians per second
        self.omega = 2 * np.pi * RPM / 60

        for i, theta in enumerate(self.theta):
            if theta >= self.theta_entry and theta <= self.blade_sep + np.pi/2:
            
                # calculate the falling velocity of the water and blade
                blade_v = self.omega * self.radius * np.sin(theta)

                fall_v = np.sqrt(2 * self.g * (-self.y_centre + self.river.head - self.radius * np.cos(theta)))

                # calculate the filling rate in m^3/s at each theta (the flow is split between current and next blade)
                fill = self.width * self.radius * (np.sin(theta) ) * (fall_v - blade_v) #- np.sin(theta - self.blade_sep)

                # remove nan values
                if np.isnan(fill):
                    fill = 0
                elif fill < 0:
                    fill = 0
                filling_rate[i] = fill

            else:

                filling_rate[i]=0
                continue

        
        # multiply by dtheta/dt to get the filling rate in m^3/s and remove the shared value
        rate = (filling_rate * self.dthetadt)  

        self.filling_rate = rate
        
        return 0

    def find_vol(self):
        '''
        the volume of water in the bucket at each theta is the integral of the filling rate from theta_entry to theta
        
        the filling rate is m^3/s but volume is in terms of theta so the integral is multiplied by dt/dtheta
        '''

        vol = np.cumsum(self.filling_rate)
        max_vol_ach = max(vol)
        empty_angle = np.pi/2

        # limit the volume to the maximum volume of the turbine
        for i, val in enumerate(vol):
            if val > self.max_vol:
                val = self.max_vol
                max_vol_ach = val

            # make it so the bucket begins to empty when the turbine is at 90 degrees - need to find exact angle
            
            if self.theta[i] > empty_angle:
                val =  max_vol_ach*(1 - (self.theta[i] - empty_angle))
                if val < 0:
                    val = 0

            vol[i] = val
            
        self.vol = vol
        return 0

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
            if theta >= self.theta_entry and theta <= self.theta_exit:
                centre_mass[i] = (a*(theta**4) + b*(theta**3) + c*(theta**2) + d*theta + e)
            else:
                centre_mass[i] = 0

        self.centre_mass = centre_mass
        return 0
    
    def find_pot_power(self):
        '''
        calculate the potential power at each theta
        '''
        # potential power is the product of the volume of water, the centre of mass, the angular velocity and the density of water
        pot_power = np.zeros(len(self.theta))
        for i, theta in enumerate(self.theta):
            pot_power[i] = (self.g * self.vol[i] * self.centre_mass[i] * self.river.rho * self.omega)

        self.pot_power = pot_power
        return 0

    def find_imp_power(self):
        '''
        calculate the impulse power at each theta
        '''
        imp_power = np.zeros(len(self.theta))

        # impulse power is the product of the radius, the density of water, the angular velocity and the difference between the filling rate and the volume flow rate
        for i, theta in enumerate(self.theta):
            if theta < self.theta_entry or theta > self.blade_sep + np.pi/2:
                imp_power[i] = 0
                continue

            # calculate the falling velocity of the water - the fall distance is the head - (y_centre + radius * cos(theta))
            fall_river_flow = np.sqrt(2 * self.g * (self.river.head - (self.y_centre  + self.radius * np.cos(theta)))) * self.width * self.radius * np.sin(theta - self.theta_entry) 
            
            # the impulse power is the product of the radius, the density of water, the angular velocity and the difference between the filling rate and the volume flow rate
            imp = self.omega * self.river.rho * self.radius * (fall_river_flow - self.filling_rate[i])

            if imp < 0:
                imp = 0

            imp_power[i] = imp

        self.imp_power = imp_power
        return 0
    
    def find_tot_power(self):
        '''
        calculate the total power at each theta
        '''
        tot_power = np.zeros(len(self.theta))

        # total power is the sum of the potential and impulse power
        for i, theta in enumerate(self.theta):
            tot_power[i] =   self.imp_power[i] + self.pot_power[i]

        self.tot_power = tot_power
        return 0
    
    def find_avg_power(self):
        '''
        calculate the average power output of the turbine for the number of blades over one revoulution

        '''
        # calculate the power output over one revolution for all the blades as a function of theta

        # calculate the separation angle between the blades
        blade_sep_idx = 100 / self.num_blades

        # compounding the power output of each blade with offset blade_sep_idx
        power = np.zeros(len(self.theta))
        for i in range(self.num_blades):
            power += np.roll(self.tot_power, int(i*blade_sep_idx))

        # average the power over one revolution
        avg_power = np.sum(power) / len(power)

        self.avg_power = avg_power * self.num_blades  #- 0.2854295943166135 * 1000
        self.full_power = power

        return 0
    
    def analysis(self, x, y, RPM):
        '''
        run the analysis for the turbine
        '''
        # initialise the turbine
        self.x_centre = x
        self.y_centre = y
        self.RPM = RPM

        # run the analysis
        self.find_intersects()
        if self.find_theta_range():
            print('error: turbine not in river')
            return 0
        if self.find_filling_rate():
            return 0
        self.find_vol()
        self.find_centre_mass()
        self.find_pot_power()
        self.find_imp_power()
        self.find_tot_power()
        self.find_avg_power()

        return self.avg_power

        
    def optimise(self, guess):
        '''
        Optimise the turbine position to maximise the average power output
        '''

        # first define the function to be optimised
        def fun(Y):
            # unpack the variables
            x, y, RPM = Y
            # define the power
            power = self.analysis(x , y  , RPM)
            
            return -power
        
        # define the initial guess
        x0 = guess

        # run the optimisation
        res = opt.minimize(fun, x0, bounds=((0, 100), (-self.river.head, 100), (0, 40)), method='nelder-mead')

        # print the results
        if not res.success:
            raise ValueError(res.message)
        newx, newy, RPM = res.x

        # average power at the new position
        power = self.analysis(newx, newy, RPM)

        print('The optimised average power output of the turbine is: %.2f W' % power)

        # return the optimal power
        return power, newx, newy, RPM
    
    def plot_turbine(self):
        '''
        Plot the turbine
        '''
        # plot the turbine
        plt.figure()
        plt.plot(self.x_centre, self.y_centre, color='r', marker='o')
        plt.plot(self.x, self.y, color='r')
        plt.plot(self.river.x_nappe, self.river.y_nappe, color='b')
        plt.plot(self.river.x_bed, self.river.y_bed, color='b')
        plt.xlim(0,2)
        plt.ylim(-1,1)
        plt.show()


if __name__ == "__main__":
    from river_class import river_obj

    # define the river
    river = river_obj(width = 0.77, depth = 0.3, velocity = 1.5, head=2)

    # define the turbine
    turbine = breastTurbine(river)

    # find intersection points
    # if not turbine.analysis(0.2, 0, RPM):
    #     print('The turbine is not in the river')
    #     exit()

    # initial guess for position and RPM
    x,y,RPM = [1, -0.1, 10]
    guess = [x, y, RPM]

    # optimise the turbine position
    opt_pow, x, y, RPM = turbine.optimise(guess)

    print('\nOptimised turbine position: (%.2f, %.2f)' %(x, y))
    print('\nOptimised RPM: %.2f' %RPM)

    # re-initialise the turbine
    print('\nRe-running the analysis for the optimised turbine position (x, y, RPM): (%.2f, %.2f, %.2f)' %(x, y, RPM))
    turbine = breastTurbine(river, x_centre=x, y_centre=y, RPM=RPM)
    turbine.analysis(x, y, RPM)

    # plot the turbine
    turbine.plot_turbine()

    # plot the filling rate and volume
    plt.figure()
    plt.plot(turbine.theta, turbine.filling_rate, label='Filling Rate')
    plt.plot(turbine.theta, turbine.vol, label='Volume')
    plt.xlabel('Theta (rad)')
    plt.ylabel('Filling Rate (m^3/s)')
    plt.legend()
    plt.show()

    # plot the power due to all blades and avg power
    plt.figure()
    plt.plot(turbine.theta, turbine.full_power, label='Full Power')
    plt.plot(turbine.theta, np.ones(len(turbine.theta)) * turbine.avg_power, label='Average Power')
    plt.xlabel('Theta (rad)')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.show()


    # plot the results
    plt.figure()
    plt.plot(turbine.theta, turbine.pot_power, label='Potential Power')
    plt.plot(turbine.theta, turbine.imp_power, label='Impulse Power')
    plt.plot(turbine.theta, turbine.tot_power, label='Total Power')
    plt.xlabel('Theta (rad)')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.show()


  


        




                                