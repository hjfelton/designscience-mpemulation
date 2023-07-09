# Script containing functions to be run when considering variable infill

def infill_main(partdef, mass_props, opt, gaopt, fname, model_in):

    # Import optimisation modules
    from infill.optimisation.montecarlo import monte
    from infill.optimisation.pso import pso_main
    from infill.optimisation.ga import ga_main
    from infill.directed_optimisation import directedopt

    # Allow results to be printed to file
    from foldpath import foldpathmain

    import numpy as np
    import csv

    cell_size = np.mean(partdef.vol)

    cell_size = pow(cell_size, 1/3)

    # nozzle_size = 0.4

    nozzles = [0.4]

    for nozzle_size in nozzles:

        # Set density data for study
        abs_density = 0.00124
        upp_density = abs_density*2.75
        rel_min = nozzle_size/(2*cell_size)

        # Generic rel_max calculated from rel_min
        rel_max = (upp_density/abs_density)*(1-rel_min) + rel_min

        denset = np.linspace(rel_min, rel_max, num=2)

        # Do initial check to make sure mass can be reached
        potmass = abs_density*sum(partdef.vol)*rel_max

        # Check potmass could provide a plausible solution
        if mass_props.mass <= potmass*1.05:
            # If opt == 1 use Monte Carlo opt
            if opt == 1:

                # Call monte carlo method
                result = monte.method(partdef, mass_props, abs_density,
                                    rel_min, rel_max, denset, fname)

            # If opt == 2 use PSO
            elif opt == 2:
                result = pso_main.method(partdef, mass_props, abs_density, rel_min,
                                        rel_max)
            # If opt == 3 use GA
            elif opt == 3:
                result = ga_main.method(partdef, mass_props, abs_density, rel_min,
                                        rel_max, gaopt)
            elif opt ==4:
                print("Calling directed optimisation")
                result = directedopt(partdef, mass_props, abs_density, denset, fname, model_in)
            else:
                print("No valid optimisation method selected.")
        else:
            print("Method cannot not provide a suitable mass and is exiting")
            result = None

    return result
