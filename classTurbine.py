import matplotlib.pyplot as plt
import numpy as np

class Turbine(self, radius, num_blades, x_centre, y_centre):

    # constructor
    def __init__(self, radius, num_blades, x_centre, y_centre):
        self.radius = radius
        self.num_blades = num_blades
        self.x_centre = x_centre
        self.y_centre = y_centre

    # methods
    def radius(self, radius, x_centre, y_centre):
        theta = np.linspace(0, 2*np.pi, 1000)
        x_circle = radius * np.cos(theta) + x_centre
        y_circle = radius * np.sin(theta) + y_centre
        return self.x_circle, self.y_circle

    def plot(self, x_circle, y_circle):
        plt.plot(x_circle, y_circle, 'r')
        plt.show()

    def breastShotPower(self, radius, num_blades, x_centre, y_centre):
        # calculate the power of the turbine
        return 0

    def underShotPower(self, radius, num_blades, x_centre, y_centre):
        # calculate the power of the turbine
        return 0
    


