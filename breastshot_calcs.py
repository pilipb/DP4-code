# import modules
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.optimize as opt
import scipy.integrate
import warnings

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

    def __init__(self, river, radius = 0.504, width = 1.008, num_blades = 5, x_centre = 0, y_centre = 0, RPM = 15): 

        self.radius = radius
        self.width = width
        self.num_blades = num_blades
        self.x_centre = x_centre 
        self.y_centre = y_centre 
        self.river = river
        self.RPM = RPM
        self.Cd = 1.28 # flat plate drag coefficient

        

        self.theta = np.linspace(0, 2*np.pi, 100)

        dtheta = self.theta[1] - self.theta[0]
        dt = (60/RPM ) / len(self.theta)
        self.dtdtheta = dt / dtheta

        self.omega = 2 * np.pi * self.RPM / 60


        self.x = self.radius * np.cos(self.theta) + self.x_centre
        self.y = self.radius * np.sin(self.theta) + self.y_centre

        self.g = 9.81
        self.max_vol = 0.032

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
        filling_rate = []


        for i, theta in enumerate(self.theta):
<<<<<<< Updated upstream

            if theta >= self.theta_entry and theta <= self.theta_exit:
=======
            if theta >= self.theta_entry and theta <= self.blade_sep + np.pi/2:

                area = (self.width * self.radius * (1 - np.cos(self.blade_sep)) ) * np.sin(theta - self.blade_sep)
                if area < 0:
                    area = 0
            
>>>>>>> Stashed changes
                # calculate the falling velocity of the water and blade
                blade_v = self.omega * self.radius * np.sin(theta)
                fall_v = np.sqrt(2 * self.g * (self.y_centre + self.river.head + self.radius * np.cos(theta)))

<<<<<<< Updated upstream
                # calculate the filling rate in m^3/s at each theta
                fill = self.width * self.radius * np.sin(theta) * (fall_v - blade_v) 
                
=======
                fall_v = np.sqrt(2 * self.g * (-self.y_centre + self.river.head  + self.river.nappe_height/2 - self.radius * np.cos(theta)))

                # calculate the filling rate in m^3/s at each theta (the flow is split between current and next blade)
                fill = area * (fall_v - blade_v) #- np.sin(theta - self.blade_sep)

>>>>>>> Stashed changes
                # remove nan values
                if np.isnan(fill):
                    fill = 0
                elif fill < 0:
                    fill = 0


                filling_rate.append(fill)
            else:
                filling_rate.append(0)

        self.filling_rate = filling_rate
        
        return 0

    def find_vol(self):
        '''
        the volume of water in the bucket at each theta is the integral of the filling rate from theta_entry to theta
        
        the filling rate is m^3/s but volume is in terms of theta so the integral is multiplied by dt/dtheta
        '''
        # multiply the filling rate by dt/dtheta to get the volume at each theta
        # calculate the volume at each theta
        for i, val in enumerate(self.filling_rate):
            self.filling_rate[i] = val * self.dtdtheta

        vol = np.cumsum(self.filling_rate)
        
        # limit the volume to the maximum volume of the bucket and make it so volume decreases after theta_exit
        for i, val in enumerate(vol):
            if val >= self.max_vol and self.theta[i] < np.pi/2:
                vol[i] = self.max_vol
            elif self.theta[i] >= np.pi/2 and self.theta[i] <= self.theta_exit:
                vol[i] = vol[i-1] * 0.7
            else:
                vol[i] = 0
                


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
        centre_mass = []
        for i, theta in enumerate(self.theta):
            centre_mass.append(a*(theta**4) + b*(theta**3) + c*(theta**2) + d*theta + e)

        self.centre_mass = centre_mass
        return 0
    
    def find_pot_power(self):
        '''
        calculate the potential power at each theta
        '''
        pot_power = []
        for i, theta in enumerate(self.theta):
            pot_power.append(self.g * self.vol[i] * self.centre_mass[i] * self.omega * self.river.rho)

        self.pot_power = pot_power
        return 0

    def find_imp_power(self):
        '''
        calculate the impulse power at each theta
        '''
        imp_power = []
        for i, theta in enumerate(self.theta):

<<<<<<< Updated upstream
            # add a blocking factor (function of theta) to the impulse power - this is the fraction of the water that is blocked by the next blade
            # block factor = 1 at theta entry and 0 at theta exit
            block_factor = 1 - (theta - self.theta_entry) / self.theta_range
=======
            # calculate the falling velocity of the water - the fall distance is the head - (y_centre + radius * cos(theta))
            fall_river_flow = np.sqrt(2 * self.g * (self.river.head + self.river.nappe_height/2 - (self.y_centre  + self.radius * np.cos(theta)))) 

            blade_v = self.omega * self.radius * np.sin(theta)

            area = (self.width * self.radius * (1 - np.cos(self.blade_sep)) ) * np.sin(theta - self.blade_sep)
            if area < 0:
                area = 0
            
            # model the impulse force as an aerodynamic drag force
            imp = 0.5 * self.Cd * self.river.rho * area * (fall_river_flow - blade_v)**2

            imp = imp * self.radius * self.omega 
>>>>>>> Stashed changes

            if theta >= self.theta_entry and theta <= self.theta_exit:
                # calculate the impulse power at each theta
                imp = self.omega * self.river.rho * self.radius *abs(self.filling_rate[i] * self.dtdtheta - (self.omega * self.radius**2 * np.sin(theta) * self.width)) * block_factor
                if imp < 0:
                    imp = 0
                imp_power.append(imp) 

            else:
                imp_power.append(0)

        self.imp_power = imp_power
        return 0
    
    def find_tot_power(self):
        '''
        calculate the total power at each theta
        '''
        tot_power = []
        for i, theta in enumerate(self.theta):
            tot_power.append(self.pot_power[i] + self.imp_power[i])

        self.tot_power = tot_power
        return 0
    
    def find_avg_power(self):
        '''
        calculate the average power output of the turbine for the number of blades over one revoulution

        '''
        # compound the power over one revolution
        full_power = np.zeros(len(self.theta))
        for i in range(self.num_blades):
            idx_offset = int(i * len(self.theta) / self.num_blades)
            full_power += np.roll(self.tot_power, idx_offset)

        self.full_power = full_power

<<<<<<< Updated upstream
        # calculate the average power
        self.avg_power = np.mean(full_power)
=======
        self.avg_power = avg_power /  self.num_blades  #- 0.2854295943166135 * 1000
        self.full_power = power
>>>>>>> Stashed changes

        return 0
    
    def full_calc(self, x, y, RPM, river):
        '''
        run all the calculations and return the average power
        '''

        # define the turbine
        turbine = breastTurbine(river, x_centre=x, y_centre=y, RPM=RPM)

        # find intersection points
        
        if turbine.find_intersects():
            return 0
        if turbine.find_theta_range():
            return 0
        turbine.find_filling_rate()
        turbine.find_vol()
        turbine.find_centre_mass()
        turbine.find_pot_power()
        turbine.find_imp_power()
        turbine.find_tot_power()
        turbine.find_avg_power()


        return turbine.avg_power


    
    # def optimise(self, RPM =0):
    #     '''
    #     Optimise the turbine position to maximise the average power output
    #     '''
    #     warnings.filterwarnings("ignore")
    #     if RPM == 0:
    #         RPM = self.find_RPM()
    #     # first define the function to be optimised
    #     def fun(Y):
    #         # unpack the variables
    #         x, y = Y
    #         # define the power
    #         power = self.analysis(x , y  , RPM = RPM)
            
    #         return -power
        
    #     # define the initial guess
    #     x0 = [1,0]

    #     # run the optimisation
    #     res = opt.fmin(fun, x0 )

    #     # print the results
    #     newx, newy = res

    #     # average power at the new position
    #     power = self.analysis(newx, newy, RPM = RPM)

    #     print('The optimised average power output of the turbine is: %.2f W' % power)

    #     # hide warnings

        

    #     # return the optimal power
    #     return power, newx, newy
    

    # def plot_turbine(self):
    #     '''
    #     Plot the turbine
    #     '''
    #     # plot the turbine
    #     plt.figure()
    #     plt.plot(self.x_centre, self.y_centre, color='r', marker='o')
    #     plt.plot(self.x, self.y, color='r')
    #     plt.plot(self.river.x_nappe, self.river.y_nappe, color='b')
    #     plt.plot(self.river.x_bed, self.river.y_bed, color='b')
    #     plt.xlim(0,2)
    #     plt.ylim(-1,1)
    #     plt.show()

    #     print('The turbine centre is positioned at: (%.2f, %.2f)' %(self.x_centre, self.y_centre))



if __name__ == "__main__":
    from river_class import river_obj

    # define the river
    river = river_obj(width = 0.77, depth = 0.3, velocity = 2, head=1)


    # find the RPM
    RPM = 20
    # define the turbine
    turbine = breastTurbine(river, x_centre=0.8, y_centre=-0.1, RPM=RPM)

    # find intersection points
    turbine.find_intersects()
    turbine.find_theta_range()
    turbine.find_filling_rate()
    turbine.find_vol()
    turbine.find_centre_mass()
    turbine.find_pot_power()
    turbine.find_imp_power()
    turbine.find_tot_power()
    turbine.find_avg_power()

    # make dataframe with results:
    import pandas as pd
    df = pd.DataFrame({'theta': turbine.theta, 'filling rate': turbine.filling_rate,'COM': turbine.centre_mass, 'volume': turbine.vol ,'pot_power': turbine.pot_power, 'imp_power': turbine.imp_power, 'tot_power': turbine.tot_power})
    print(df.head(20))

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


    # plot the average power against RPM
    RPMs = np.linspace(2, 40, 50)
    avg_power = []
    for RPM in RPMs:
        turbine = breastTurbine(river, x_centre=0.8, y_centre=-0.1, RPM=RPM)
        turbine.find_intersects()
        turbine.find_theta_range()
        turbine.find_filling_rate()
        turbine.find_vol()
        turbine.find_centre_mass()
        turbine.find_pot_power()
        turbine.find_imp_power()
        turbine.find_tot_power()
        turbine.find_avg_power()
        avg_power.append(turbine.avg_power)

    plt.figure()
    plt.plot(RPMs, avg_power)
    plt.xlabel('RPM')
    plt.ylabel('Average Power (W)')
    plt.show()




        




                                