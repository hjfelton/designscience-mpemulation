# Master script for mass property emulation investigation


import numpy as np


def master(mod_in):

    # Import time to measure performance of code
    import time

    # Import numpy for computational efficiency using arrays
    import numpy as np

    # Import python scripts for own functions
    from read_dat import readdat
    from centre import centre
    from volume import volfunc
    from categorisation import categorise
    from getmass import getmass
    from infill.infill_main import infill_main

    import csv

    # For figure creation
    # from figure_creation import figcode

    # Import os to get current cwd
    import os

    # Specify all possible models
    model_dict = {
        1: "Cube",
        2: "Sphere",
        3: "Switch",
        4: "Drill",
        5: "Pointer"}

    # Select model in. NB: This is currently set in code, but could ask user
    model_in = mod_in

    # Print which model is being used
    print(f"Model being optimised: {model_dict[model_in]}")

    # Specify methodolgies available
    method_dict = {
        1: "Variable Infill",
        2: "Particulate",
        3: "Discrete Masses"}

    # Choose methodology
    method = 1

    # Print which method is being used
    print(f"Emulation method: {method_dict[method]}")

    # Set up dict of optimisation methods
    opt_dict = {
        1: "Monte Carlo",
        2: "Particle Swarm",
        3: "Genetic Algorithm",
        4: "Directed Optimisation"
    }

    # Select optimisation method using opt_dict for reference. NB: Could be
    # entered as part of run in future.
    opt = 4

    # Print which model is being used
    print(f"Optimisation method: {opt_dict[opt]}")

    # Set up dict of optimisation methods
    ga_dict = {
        1: "Single Point",
        2: "Uniform",
        3: "Double Point"
    }

    # Select optimisation method using opt_dict for reference. NB: Could be
    # entered as part of run in future.
    gaopt = 2

    if opt == 3:
        # Print which crossover method is being used
        print(f"GA crossover method: {ga_dict[gaopt]}")

    # Find start time
    starttime = time.perf_counter()

    # Set filename
    fname = model_dict.get(model_in)

    # Get cwd
    cwd = os.getcwd()

    # Read mechdat.dat file into python using function readdat
    (vert, el) = readdat(fname, cwd)
    print("Data read")
    print(time.perf_counter())
    # Convert vert and el to numpy arrays
    vert = np.asarray(vert)
    el = np.asarray(el)

    # Find centre point of cells
    cpts = centre(vert, el)
    print("cpts found")
    print(time.perf_counter())

    # Find volumes of cells
    vol = volfunc(vert, el)
    print("Volume found")
    print(time.perf_counter())
    print(f"Total volume = {sum(vol)}")

    print(f"Mean volume of cells = {sum(vol)/len(vol)}")
    print(f"There are {len(vol)} cells")

    # Categorise elements to allow for solid shell
    elcat = categorise(vert, el)
    print("Categorisation completed")
    print(time.perf_counter())
    # Retrieve required mass properties
    mass_props = getmass(fname, cwd)
    print("Required mp found")
    print(time.perf_counter())

    # Create data structure
    partdef = PartStruct(vert, el, vol, elcat, cpts)
    del vert, el, vol, elcat, cpts

    # If function to change methodology
    if method == 1:
        result = infill_main(partdef, mass_props, opt, gaopt, fname, model_dict[model_in])
    elif method == 2:
        pass
    elif method == 3:
        pass

    print("Optimisation completed")

    # Find end time
    endtime = time.perf_counter()

    # Find time code ran for
    runtime = endtime-starttime
    print("The code took %.2fs to run." % round(runtime, 2))
    print(f"The result is {result}")

    # Plotting
    # figcode.figgen(partdef, result)


class PartStruct:
    # Create object containing information defining the part
    def __init__(self, vert, el, vol, elcat, cpts):

        import numpy as np

        self.vert = vert
        self.elm = el
        self.vol = vol
        self.elmcat = elcat
        self.cpts = cpts


# Run program
if __name__ == "__main__":

    models = [3, 4, 5]

    for modin in models:
        master(modin)
