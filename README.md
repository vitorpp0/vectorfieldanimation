# VectorFieldAnimation
Simple class that makes it easy to simulate a Vector Field through an matplotlib animation

## Requirements
This class makes use of some Python's modules [Numpy](https://numpy.org/) and [MatPlotLib](https://matplotlib.org/).

## Quick With Predefined Vector Field
This run the predefined vector field. \
""""
    import os
    os.chdir(r"Directory/Path/Where/The/VectorFieldAnimation.py/Is"

    # Importing the VectorFieldAnimation.py
    import VectorFieldAnimation as vfa

    # Instancianting Our VectorFieldAnimation Object
    vfaObject = vfa.vectorFieldAnimation()

    # Running the simulation and animation
    vfaObject.animate()
""""

## Quick Set Up
Now let's set our Vector Field. \
""""
    import os
    os.chdir(r"Directory/Path/Where/The/VectorFieldAnimation.py/Is"

    # Importing the VectorFieldAnimation.py
    import VectorFieldAnimation as vfa

    # Setting Up Our Vector Field
    import numpy as np # Because we always need it

    # Sets Our 3D Space and the vectors tails
    x_axis = np.arange(-2,2,0.5)
    y_axis = np.arange(-2,2,0.5)
    z_axis = np.arange(-2,2,0.5)
    spaceMesh = [x_axis, y_axis, z_axis]

    # Setting the Vector Components Functions in terms of x,y,z and time
    # Remember, x,y and z are Numpy arrays, so use Numpy functions!!
    x_component = "4*time*x"
    y_component = "-2*(time**2)*y"
    z_component = "4*np.multiply(x,z)"
    componentsFunctions = [x_component, y_component, z_component]

    # Instancianting Our VectorFieldAnimation Object
    vfaObject = vfa.vectorFieldAnimation(space=spaceMesh, vectorComponents=componentsFunctions, length=0.3, animationDuration=2)
    # animationDuration must be in seconds and length is the vectors lengths

    # Running the simulation and animation
    vfaObject.animate()
""""

## End
Hope you like it! :grin: