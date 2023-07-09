# Script to check den, send to obj and record result

def solvemain(den, arg):

    # Import csv to write data to csv file
    import csv

    # Import obj_func
    from obj_func import objfunc

    # Import numpy
    import numpy as np

    # Set up variable names
    it = arg[0]
    body = arg[1]
    shell = arg[2]
    abs_density = arg[4]
    rel_max = arg[5]
    rel_min = arg[6]
    mass_props = arg[7]
    foldpath = arg[8]
    fname = arg[10]

    # Check is density in range
    den = denCheck(den, rel_min, rel_max)

    # Calculate cost using obj. func
    cost, mass, com, moi = objfunc(den, shell, body, abs_density, mass_props, fname)

    # Create csv containing result
    fname = foldpath + "/it" + str(it+1) + ".csv"

    # Initiate list
    mp_res_list = []

    # Add mass properties to list
    mp_res_list.append(mass)
    mp_res_list.append(com.x)
    mp_res_list.append(com.y)
    mp_res_list.append(com.z)
    mp_res_list.append(moi.xx)
    mp_res_list.append(moi.yy)
    mp_res_list.append(moi.zz)

    write_den = np.concatenate((den, shell.den))

    # Write result to file
    with open(fname, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(write_den)
        wr.writerow(mp_res_list)

    cpts = np.concatenate((body.cpts, shell.cpts))

    # with open("cpts.csv", "w", newline="") as f:
    #     wr = csv.writer(f)
    #     wr.writerows(cpts)

    return cost, den

def solvemainalt(den, body, shell, abs_density, rel_max, rel_min, mass_props, fname):

    # Import csv to write data to csv file
    import csv

    # Import obj_func
    from obj_func import objfunc

    # Import numpy
    import numpy as np

    # Check is density in range
    den = denCheck(den, rel_min, rel_max)

    # Calculate cost using obj. func
    cost, mass, com, moi = objfunc(den, shell, body, abs_density, mass_props, fname)

    # Initiate list
    mp_res_list = []

    # Add mass properties to list
    mp_res_list.append(mass)
    mp_res_list.append(com.x)
    mp_res_list.append(com.y)
    mp_res_list.append(com.z)
    mp_res_list.append(moi.xx)
    mp_res_list.append(moi.yy)
    mp_res_list.append(moi.zz)

    return cost, den


def denCheck(den, rel_min, rel_max):

    # Check is density in range
    for j in range(len(den)):
        if den[j] > rel_max:
            den[j] = rel_max
        elif den[j] < rel_min:
            den[j] = rel_min

    return den
