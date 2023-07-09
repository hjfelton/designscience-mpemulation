# Script for Monte Carlo optimisation

def monteopt(arg):
    # This function is the monte carlo opt itself

    # Import random to generate random numbers
    import random

    # Import numpy
    import numpy as np

    # Import gc to free memory
    import gc

    # Import solve function
    from solve import solvemain

    # Set up variable names
    it = arg[0]
    body = arg[1]
    shell = arg[2]
    N = arg[3]
    abs_density = arg[4]
    rel_max = arg[5]
    rel_min = arg[6]
    mass_props = arg[7]
    foldpath = arg[8]
    denset = arg[9]

    # Set up rnd num. gen
    rnd = (it+1)/N * rel_max

    # Check if rnd in denset. If it is, modify slightly
    if rnd in denset:
        rnd = rnd + 0.001

    # Set up probability array
    prob = np.ones(len(denset)-1)

    temp_arr = []

    # Find sum of abs(1/(rnd-denset))
    for i in denset:
        temp_arr.append(abs(1/(rnd - i)))

    temp_sum = sum(temp_arr)

    # Remove last value of temp_arr to match prob
    temp_arr.pop(-1)

    # Multiply prob array by temp_arr to get probabilities
    prob = prob * temp_arr * 1/temp_sum

    # Append last probability to prob to make sum prob = 1
    prob = np.append(prob, (1-sum(prob)))

    # Generate arr of random numbers
    # den = np.random.uniform(rel_min, rel_max, len(body.celllist))*rnd
    den = np.random.choice(denset, len(body.celllist), p=prob)

    # Call solve function
    cost, den = solvemain(den, arg)

    # Delete vars
    del den, body, shell, arg

    # Clear memory
    gc.collect()

    # Return result
    return cost


def method(partdef, mass_props, abs_density, rel_min, rel_max, denset):

    # Import module for multiprocessing
    import concurrent.futures

    # Import math for setting inf
    import math

    # Import module to create a solid shell
    import solid_shell

    # Import csv to export costs
    import csv

    # Import function to get folder path
    from foldpath import foldpathmain

    # Define number of iterations
    N = 100

    # Split part into shell and body
    (shell, body) = solid_shell.main(partdef)

    # # Find number of variables
    nVar = len(body.elm)

    # Get folder path for results
    # foldpath = foldpathmain()
    foldpath = ""

    # Initialise arg list
    arg = []

    # Create arg for parallel processing
    for i in range(N):
        temp_list = [i, body, shell, N, abs_density, rel_max, rel_min,
                     mass_props, foldpath, denset]
        arg.append(temp_list)

    print("Starting multiprocessing")

    # Use parallel processing to complete optimisation
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(monteopt, arg)

    print("Finished multiprocessing")

    # Convert generator to tuple
    res_list = tuple(results)

    # Initialise best cost (lower is better)
    best_cost = math.inf

    # Cycle through all results to find best cost
    for i in range(N):
        if abs(res_list[i]) < abs(best_cost):
            # If cost is lower (better) than current best, overwrite best
            # result
            best_cost = res_list[i]
            # Save best iteration
            best_it = i+1

    # # Create csv containing costs
    # fname = foldpath + "/costs.csv"

    # # Write result to file
    # with open(fname, "w") as f:
    #     wr = csv.writer(f)
    #     wr.writerow(res_list)

    # Print best result
    print(f"Best Cost: {best_cost}")
    print(f"Best it: {best_it}")

    return best_cost
