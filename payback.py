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
        self.turbine_cost = 4000 # £

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
        self.daily_charge = 0.46356  # £/day
        self.unit_charge = 0.37037 # £/kWh

        # calculate baseline costs
        self.annual_cost = self.daily_charge * 365 + self.unit_charge * self.yearly_usage

        # define sell back rate
        self.sell_back_rate = 0.041 # £/kWh

    def payback(self, turbine):
        # calculate the payback period of the turbine
        # turbine_cost - float: the cost of the turbine in £
        # turbine - object: the turbine object
        # river - object: the river object
        print('Normal annual electricity cost: %.2f £ / year' % self.annual_cost)

        # calculate the energy produced by the turbine in a year kWh/year
        energy_produced = turbine.avg_power * 365 * 24 / 1000
        print('Energy produced: %.2f kWh / year' % energy_produced)

        # calculate the yearly difference in energy usage
        energy_diff = self.yearly_usage - energy_produced
        print('Energy difference: %.2f kWh / year' % energy_diff)

        # if the turbine produces more energy than the household uses
        if energy_diff < 0:
            # calculate the profit from selling back the energy
            profit = abs(energy_diff) * self.sell_back_rate
            savings = self.unit_charge * self.yearly_usage

        else:
            # calculate the savings made
            profit = 0
            savings = self.unit_charge * abs(energy_diff)

        print('Profit: %.2f £ / year' % profit)
        print('Savings: %.2f £ / year' % savings)


        # caculate the yearly benefit to the household
        self.benefit =  (profit + savings)
        print('Benefit: %.2f £ / year' % self.benefit)

        # calculate the payback period in years
        self.payback_time = self.turbine_cost / self.benefit
        print('Payback time: %.2f years for a turbine cost of £%.2f' % (self.payback_time, self.turbine_cost))

        return self.payback_time, self.benefit





            
