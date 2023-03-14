# imports
import numpy as np
import matplotlib.pyplot as plt

'''
This class will construct a river object that will contain all the information needed
for turbine calculations in both a breastshot and undershot configuration. The class will also allow automation
of which turbine is used as a zero head river will allow the selection of an undershot turbine.

The measurement inputs to this class should be relatively easy to achieve.

Parameters:
----------------
    width - float: the width of the river in m prior to a nappe (if applicable)
    depth - float: the depth of the river in m prior to a nappe (if applicable)
    velocity - float: the free stream velocity of the river prior to a nappe (if applicable)
    head - float: the head of the waterfall, 0 if not existant

Methods:
NONE

Returns:
----------------
    vol_flow_rate - float: the volumetric flow rate of the river
    y_nappe - array: the y coordinates of the 'top' of the river
    x_nappe - array: the corresponding x coordinates
    y_bed - array: the y coordinates of the river bed
    x_bed - array: the corresponding x coordinates

NOTE the returned coordinates are only after the nappe (assuming left to right flow)
the head does not impact the calculations and can be left empty unless defined otherwise.


'''

class river_obj():
    # constructor
    def __init__(self, width, depth, velocity ):
        self.width = width
        self.depth = depth
        self.velocity = velocity


        self.vol_flow_rate = width * depth * velocity # m^3/s

        # define constants
        self.nappe_C = 1.69 
        self.g = 9.81 
        self.rho = 997 # kg/m^3

        # calculate river features
        self.nappe_height = (self.vol_flow_rate / (self.nappe_C * self.g**1/2 * self.width)) ** (2/3)
        self.v_nappe = self.vol_flow_rate/(self.width * self.nappe_height)

        # calculate river at bed and nappe parametrically for time after waterfall
        time = 40

        # define time - arbitrary 1000
        t = np.linspace(0, time, 1000) 
        # define x and y coordinates (after waterfall)
        self.x_bed = self.velocity * t
        self.y_bed = np.zeros(len(t)) - 0.5 * self.g * t**2
        self.x_nappe = self.v_nappe * t
        self.y_nappe = self.nappe_height * np.ones(len(t)) - 0.5 * self.g * t**2
