# Engineering Design Penultimate Year Research and Dissertation Project

### Outline
The aim of this project is to produce production standard code for the modelling, optimisation and prediction of power output for the Pico Stream hydro-power turbine.

### Aims
The development of the model will build on the existing Pico Stream model and incorporate details from the research. The main objectives of this stage of the project will lie in developing a model that is flexible to variable conditions.

The model will allow variable flow condition inputs, including variable head and flow rate/volume.

The model will then be developed to be used in both the breast shot and under shot flow configurations with the same parameters as in (A).

The model will also be developed to allow the positioning of the turbine to be varied in respect to a datum set by the river position in the given configuration.

### Structure of files

The models are developed in their respective class files:

breastshot_calcs.py
undershot_calcs.py

and both make use of the river_class.py

water_mass.ipynb is a workbook used to calculate an approximation of the torque produced by the turbine, the data from this is from the CAD model as assessed by Henry Haslam, UoB, 20/02/23.

test.ipynb is used to test all the functions of the models

testData.ipynb is a test / viewing of the available validation data

validation.ipynb imports the models and test data and compares the results, with an aim to tune the model to fit the real world results better - the outputs of the hyper parameter tuning will be used in any further development.


