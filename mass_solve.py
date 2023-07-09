# Function to find mass
def massfunc(abs_density, den, vol):

    import numpy as np

    # Find array of mass for iteration
    mass_arr = np.multiply(den, vol)*abs_density

    # Sum cell masses to find total mass
    mass = sum(mass_arr)

    return mass, mass_arr


# Function to find CoM
def comfunc(mass_arr, cpts):

    import numpy as np

    # Initialise com array
    com_arr = []

    # Loop over each axis
    for i in range(3):
        com_arr.append(sum(np.multiply(mass_arr, cpts[:, i]))/sum(mass_arr))

    # Convert list to array
    com_arr = np.asarray(com_arr)

    # Send arr to get CoM structure
    com = CoMStruct(com_arr)

    # Return array
    return com


# Function to find inertia
def inertiafunc(mass_list, com, cpts):

    import numpy as np

    # Initialise MoI list
    moi_list = []

    # Find ixx, iyy, izz
    moi_list.append(sum([mass_list[i]*((cpts[i][1]-com.y) ** 2 +
                    (cpts[i][2] - com.z) ** 2) for i in range(len(cpts))]))
    moi_list.append(sum([mass_list[i]*((cpts[i][0]-com.x) ** 2 +
                    (cpts[i][2] - com.z) ** 2) for i in range(len(cpts))]))
    moi_list.append(sum([mass_list[i]*((cpts[i][0]-com.x) ** 2 +
                    (cpts[i][1] - com.y) ** 2) for i in range(len(cpts))]))

    # Convert to array
    moi_arr = np.asarray(moi_list)

    # Structure MoI data
    moi = MoIStruct(moi_arr)

    return moi


# Class to structure CoM data
class CoMStruct:
    def __init__(self, com_arr):

        self.x = com_arr[0]
        self.y = com_arr[1]
        self.z = com_arr[2]


# Class to structure MoI data
class MoIStruct:
    def __init__(self, moi_arr):

        self.xx = moi_arr[0]
        self.yy = moi_arr[1]
        self.zz = moi_arr[2]
