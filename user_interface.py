'''
In the user interface, the program will take the user's input and display the output.
The user will be asked to input the following:
- the radius of the turbine
- the width of the turbine
- the number of blades on the turbine
- the type of turbine (undershot or breastshot)

(the optimal centre of the turbine will be calculated by the program)

- the river width
- the river depth
- the river velocity

The program will then calculate the optimal power output of the turbine and display it to the user with the optimal
position of the turbine.

Parameters:
radius - float: radius of the turbine
width - float: width of the turbine
num_blades - int: number of blades on the turbine
turbine_type - string: type of turbine (undershot or breastshot)
river_width - float: width of the river
river_depth - float: depth of the river
river_velocity - float: velocity of the river

Return:
power - float: optimal power output of the turbine
centre - array: optimal position of the turbine

'''

# import modules
import numpy as np
import matplotlib.pyplot as plt
import math
from breastshot_calcs import breastTurbine
from undershot_calcs import underTurbine
from river_class import river_obj

# import modules for the GUI
import tkinter as tk

# import window for the GUI
from tkinter import *


# import FigureCanvasTkAgg from matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# import optimisation module
import scipy.optimize as opt



# define a function to optimise the turbine
def optimise_turbine(turbine, river, type):

    if type == "undershot": 

        # first define the function to be optimised
        def fun(y):
            # define the power
            power = turbine.analysis( y , RPM = 15)
            
            return -power

        # run the optimisation
        res = opt.minimize(fun, -0.1, bounds = [(-1, 3)])

        # reinstantiate the turbine
        under_turbine = underTurbine(turbine.radius, turbine.width, turbine.num_blades, res.x, river)

        # calculate the power 
        power = under_turbine.analysis()
        return power, res.x
    
    elif type == "breastshot":

        # first define the function to be optimised
        def fun(Y):
            # unpack the variables
            x, y = Y
            # define the power
            power = turbine.analysis( x, y , RPM = 15)
            
            return -power


        # define the initial guess
        x0 = [1, -0.2]

        # run the optimisation
        res = opt.fmin(fun, x0 )

        # print the results
        newx, newy = res

        # reinstantiate the turbine
        turbine = breastTurbine(turbine.radius, turbine.width, turbine.num_blades, newx, newy, river)

        # calculate the power
        power = turbine.analysis()

        return power, [newx, newy]
    

# define a function to calculate the power output
def calc_func(radius, width, num_blades, turbine_type, river_width, river_depth, river_velocity):
    river = river_obj(river_width, river_depth, river_velocity)
    
    if turbine_type == "undershot":
        turbine = underTurbine(radius, width, num_blades, -0.1, river)
        power, newy = optimise_turbine(turbine, river, turbine_type)

    elif turbine_type == "breastshot":
        turbine = breastTurbine(radius, width, num_blades, 1, -0.2, river)
        power, newy = optimise_turbine(turbine, river, turbine_type)
        
    else:
        print("Please enter a valid turbine type")

    return power, newy, turbine

'''
Create a GUI that will take the users input, calculate the optimal power output and display it to the user and display
the optimal position of the turbine.

'''

# create a class for the GUI
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # set the title of the GUI
        self.title("Turbine Optimisation")

        # set the size of the GUI
        self.geometry("800x600")

        # set the background colour of the GUI
        self.configure(bg = "white")

        # create a frame to hold the widgets
        self.frame = tk.Frame(self, bg = "white")
        self.frame.pack()

        # create a label for the title
        self.title_label = tk.Label(self.frame, text = "Turbine Optimisation", bg = "white", font = ("Arial", 20))
        self.title_label.grid(row = 0, column = 0, columnspan = 2, pady = 10)

        # create a label for the radius
        self.radius_label = tk.Label(self.frame, text = "Radius of turbine (m):", bg = "white", font = ("Arial", 12))
        self.radius_label.grid(row = 1, column = 0, pady = 10)

        # create an entry box for the radius
        self.radius_entry = tk.Entry(self.frame, width = 10)
        self.radius_entry.grid(row = 1, column = 1, pady = 10)

        # create a label for the width
        self.width_label = tk.Label(self.frame, text = "Width of turbine (m):", bg = "white", font = ("Arial", 12))
        self.width_label.grid(row = 2, column = 0, pady = 10)

        # create an entry box for the width
        self.width_entry = tk.Entry(self.frame, width = 10)
        self.width_entry.grid(row = 2, column = 1, pady = 10)

        # create a label for the number of blades
        self.num_blades_label = tk.Label(self.frame, text = "Number of blades:", bg = "white", font = ("Arial", 12))
        self.num_blades_label.grid(row = 3, column = 0, pady = 10)

        # create an entry box for the number of blades
        self.num_blades_entry = tk.Entry(self.frame, width = 10)
        self.num_blades_entry.grid(row = 3, column = 1, pady = 10)

        # create a label for the turbine
        self.turbine_label = tk.Label(self.frame, text = "Type of turbine:", bg = "white", font = ("Arial", 12))
        self.turbine_label.grid(row = 4, column = 0, pady = 10)

        # create a drop down menu for the turbine type
        self.turbine_type = tk.StringVar()
        self.turbine_type.set("undershot")
        self.turbine_menu = tk.OptionMenu(self.frame, self.turbine_type, "undershot", "breastshot")
        self.turbine_menu.grid(row = 4, column = 1, pady = 10)

        # create a label for the river width
        self.river_width_label = tk.Label(self.frame, text = "Width of river (m):", bg = "white", font = ("Arial", 12))
        self.river_width_label.grid(row = 5, column = 0, pady = 10)

        # create an entry box for the river width
        self.river_width_entry = tk.Entry(self.frame, width = 10)
        self.river_width_entry.grid(row = 5, column = 1, pady = 10)

        # create a label for the river depth
        self.river_depth_label = tk.Label(self.frame, text = "Depth of river (m):", bg = "white", font = ("Arial", 12))
        self.river_depth_label.grid(row = 6, column = 0, pady = 10)

        # create an entry box for the river depth
        self.river_depth_entry = tk.Entry(self.frame, width = 10)
        self.river_depth_entry.grid(row = 6, column = 1, pady = 10)

        # create a label for the river velocity
        self.river_velocity_label = tk.Label(self.frame, text = "Velocity of river (m/s):", bg = "white", font = ("Arial", 12))
        self.river_velocity_label.grid(row = 7, column = 0, pady = 10)

        # create an entry box for the river velocity
        self.river_velocity_entry = tk.Entry(self.frame, width = 10)
        self.river_velocity_entry.grid(row = 7, column = 1, pady = 10)

        # create a button to calculate the power output
        self.calc_button = tk.Button(self.frame, text = "Calculate Power Output", command = self.calc_power)
        self.calc_button.grid(row = 8, column = 0, columnspan = 2, pady = 10)

        # create a label for the power output
        self.power_label = tk.Label(self.frame, text = "Power Output:", bg = "white", font = ("Arial", 12))
        self.power_label.grid(row = 9, column = 0, pady = 10)

        # create a label to display the power output
        self.power_display = tk.Label(self.frame, text = "", bg = "white", font = ("Arial", 12))
        self.power_display.grid(row = 9, column = 1, pady = 10)

        # create a label for the optimal position
        self.position_label = tk.Label(self.frame, text = "Optimal Position:", bg = "white", font = ("Arial", 12))
        self.position_label.grid(row = 11, column = 0, pady = 10)

        # create a label to display the optimal position
        self.position_display = tk.Label(self.frame, text = "", bg = "white", font = ("Arial", 12))
        self.position_display.grid(row = 11, column = 1, pady = 10)

    def calc_power(self):

        # get the values from the entry boxes
        radius = float(self.radius_entry.get())
        width = float(self.width_entry.get())
        num_blades = int(self.num_blades_entry.get())
        turbine_type = self.turbine_type.get()
        river_width = float(self.river_width_entry.get())
        river_depth = float(self.river_depth_entry.get())
        river_velocity = float(self.river_velocity_entry.get())

        # create a river object
        river = river_obj(river_width, river_depth, river_velocity)

        if turbine_type == "undershot":

            
            # create a turbine object
            turbine = underTurbine(radius, width, num_blades, 0, river)

            # calculate the optimal position of the turbine
            power , y_opt = optimise_turbine(turbine, river, turbine_type)

        elif turbine_type == "breastshot":
                
            # create a turbine object
            turbine = breastTurbine(radius, width, num_blades, 0, 0, river)

            # calculate the optimal position of the turbine
            power , y_opt = optimise_turbine(turbine, river, turbine_type)


    
        # display the power output
        self.power_display.config(text = str(power) + " W")

        # display the optimal position
        self.position_display.config(text = str(y_opt) + " m")

  
if __name__ == "__main__":
    root = GUI()
    root.title("Turbine Optimisation")
    root.geometry("500x500")
    root.resizable(False, False)
    root.configure(bg = "white")
    root.mainloop()






   