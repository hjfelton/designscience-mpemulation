# Script to calculate the value of the objective function

def objfunc(den, shell, body, abs_density, mass_props, fname):

    import mass_solve as calc

    import numpy as np

    import csv

    # Set obj multipliers

    # Set location for obj multipliers
    pathobj = "resources/objfunc_mult/" + fname + ".csv"

    # Open file, import obj multipliers
    with open(pathobj, "r") as f:

        objdata = csv.reader(f)

        objmul = []

        for row in objdata:

            objmul.append(float(row[0]))

    # Form cpts array
    cpts = np.concatenate((body.cpts, shell.cpts))

    # Form vol array
    vol = body.vol

    vol = np.concatenate((vol, shell.vol))

    # Form den array
    den = np.concatenate((den, shell.den))

    # Get mass from mass func (and array of masses)
    mass, mass_arr = calc.massfunc(abs_density, den, vol)

    # Find cost associated with mass
    mass_cost = (mass - mass_props.mass)

    # Find CoM positions
    com = calc.comfunc(mass_arr, cpts)

    # Find CoM costs
    com_cost = []
    com_cost.append(com.x - mass_props.comx)
    com_cost.append(com.y - mass_props.comy)
    com_cost.append(com.z - mass_props.comz)

    # Find MoIs
    moi = calc.inertiafunc(mass_arr, com, cpts)

#     # Used to print results each iteration if needed
#     print(f"Mass = {mass}")
#     print(f"CoMx = {com.x}")
#     print(f"CoMy = {com.y}")
#     print(f"CoMz = {com.z}")
#     print(f"Ixx = {moi.xx}")
#     print(f"Iyy = {moi.yy}")
#     print(f"Izz = {moi.zz}")

    del mass_arr, cpts, den, vol, shell, body

    # Find MoI costs
    moi_cost = []
    moi_cost.append(moi.xx - mass_props.ixx)
    moi_cost.append(moi.yy - mass_props.iyy)
    moi_cost.append(moi.zz - mass_props.izz)

    # Calculate cost
    cost = (abs(mass_cost)*objmul[0] +
            sum(abs(com_cost[i])*objmul[i+1] for i in range(3)) +
            sum(abs(moi_cost[i])*objmul[i+4] for i in range(3)))

    return cost, mass, com, moi
