# imports
import numpy as np

class river():
    # constructor
    def __init__(self, width, depth, velocity):
        self.width = width
        self.depth = depth
        self.velocity = velocity

        self.x = np.linspace(0, width, 100)
        self.y_bed = -depth * np.ones(100)
        self.y_surface = np.zeros(100)
        self.y = np.linspace(-depth, 0, 100)
        self.g = 9.81