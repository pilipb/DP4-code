'''
This module will contain the payback calculation for the turbine. 

Parameters:
----------------
    turbine_cost - float: the cost of the turbine in £
    turbine_
    turbine - object: the turbine object
    river - object: the river object

Methods:
----------------
    household - object: the household object

Returns:
----------------
    payback - float: the payback period of the turbine in years

'''

# imports
import numpy as np

class household():
    def __init__(self, size):

        self.size = size

        # define general sizes - reference household energy usage
        sizes = {
            'small': 1500, # kWh/year
            'medium': 2900,
            'large': 4000
        }

        if self.size not in sizes:
            # allow for numeric input
            try:
                self.size = float(self.size)
            except:
                print('Invalid size')
        else:
            self.size = sizes[self.size]

        # define usage breakdown
        self.daily_usage = self.size / 365
        self.monthly_usage = self.size / 12
        self.yearly_usage = self.size

        # define costs - reference British Gas
        daily_charge = 0.46356  # £/day
        unit_charge = 0.37037 # £/kWh

        # calculate costs
        self.annual_cost = daily_charge * 365 + unit_charge * self.yearly_usage

        # define sell back rate
        self.sell_back_rate = 0.041 # £/kWh


            
