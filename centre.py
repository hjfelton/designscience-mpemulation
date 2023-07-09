# Script to find centre point of cells

def centre(vert, el):

    # import numpy
    import numpy as np

    # Initialise cpts tuple
    cpts = []

    # Loop through cells
    for i in el:

        # Reset xc, yc, zc to 0
        xc = 0
        yc = 0
        zc = 0

        # Cycle through vertices that define cell j
        for j in i:

            # Get sum of all x, y, z
            xc = xc + vert[j-1, 0]
            yc = yc + vert[j-1, 1]
            zc = zc + vert[j-1, 2]

        # Once cycled through all vertices, find average position
        xc = xc/len(i)
        yc = yc/len(i)
        zc = zc/len(i)

        # Create temp list of cpts
        temp_cpts = (xc, yc, zc)

        # Append cpts to list
        cpts.append(temp_cpts)

    # Delete temp_cpts
    del temp_cpts

    # Convert list to tuple
    cpts = np.asarray(cpts)

    return cpts
