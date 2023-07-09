# Script to find volume of cells

# Import convex hull method
from scipy.spatial import ConvexHull

# Import numpy
import numpy as np

def volfunc(vert, el):

    # Initialise volume list
    vol = []

    # Loop through cells to find volume
    for i in el:

        # Empty points list
        points = []

        # Cycle through points and add to list
        for j in i:
            points.append(vert[j-1, :])

        # Find convex hull
        hull = ConvexHull(points)

        # Add volume to list
        vol.append(hull.volume)

    # Convert to array
    vol = np.asarray(vol)

    return vol
