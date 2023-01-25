import numpy as np
import matplotlib.pyplot as plt

class breastTurbine():
    # constructor
    def __init__(self, radius, num_blades, x_centre, y_centre):
        self.radius = radius
        self.num_blades = num_blades
        self.bucket_mass = 8
        self.g = 9.81
        self.x_centre = x_centre
        self.y_centre = y_centre

    # methods - for calculating rotational velocity
    def velocities(self, head, nappe_height,v_nappe):
        
        self.v_vert = (2 * self.g * (head + nappe_height/2)) ** 0.5
        self.v_tan = (v_nappe**2 + self.v_vert**2) ** 0.5
        return self.v_vert, self.v_tan

    # methods - for calculating power
    def power(self, flow_rate, rho):
        self.power_KE = 0.5 * flow_rate * rho * self.v_tan**2

        torque = self.bucket_mass * self.g * self.radius
        self.power_PE = torque * self.v_tan 

        self.power = self.power_KE + self.power_PE
        return self.power  

   
class River():
    # constructor
    def __init__(self, width, depth, velocity, head):
        self.width = width
        self.depth = depth
        self.velocity = velocity
        self.head = head
        self.volFlowRate = width * depth * velocity

        self.kPower = self.volFlowRate**2 / 2
        self.pPower = self.volFlowRate * head * 9.81
        self.totalPower = self.kPower + self.pPower

        self.nappeC = 1.69
        self.g = 9.81
        self.rho = 1
        self.nappe_height = (self.volFlowRate / (self.nappeC * self.g**1/2 * self.width)) ** (2/3)
        self.v_nappe = self.volFlowRate/(self.width * self.nappe_height)

'''
# Turbine

x_centre, y_centre = 100, -50
fall_dist = 20



# Calculations for KE

v_vert = (2 * g * (fall_dist + nappe_height/2)) ** 0.5
v_tan = (v_nappe**2 + v_vert**2) ** 0.5

power_KE = 0.5 * flow_rate * rho * v_tan**2

# Static PE calculations

torque = mass_bucket * g * radius
power_PE = torque * v_tan

# Instantaneous power

power = power_KE + power_PE

'''