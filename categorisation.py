# Script to categorise cells

def categorise(vert, el):

    from collections import Counter
    import math
    import numpy as np

    # Convert array to tuple
    array_of_tuples = map(tuple, el)
    el = tuple(array_of_tuples)

    # Count how many time each vertex is used in el (for all tuples in el)
    # Corner nodes only
    num_corner = Counter(elem[i] for i in range(8) for elem in el)

    # Count how many time each vertex is used in el (for all tuples in el)
    # edge nodes only
    # Could get rid of this to improve speed
    num_edge = Counter(elem[i] for i in range(9, 20) for elem in el)

    # Initialise nodecat
    nodecat = []

    # Loop through every vertex (node) to categorise
    for i in range(1, len(vert)+1):

        # Check if vertex defines corner
        # Categorise as necessary
        if num_corner[i] == 0:
            pass
        elif num_corner[i] == 1:
            nodecat.append("corner")
        elif num_corner[i] == 2:
            nodecat.append("edge")
        elif num_corner[i] == 3:
            nodecat.append("corner")
        elif num_corner[i] == 4:
            nodecat.append("surface")
        elif num_corner[i] == 5:
            nodecat.append("corner")
        elif num_corner[i] == 6:
            nodecat.append("edge")
        elif num_corner[i] == 7:
            nodecat.append("corner")
        elif num_corner[i] == 8:
            nodecat.append("body")

        # Check if vertex defines centre of edge
        # Categorise as necessary
        if num_edge[i] == 0:
            pass
        elif num_edge[i] == 1:
            nodecat.append("edge")
        elif num_edge[i] == 2:
            nodecat.append("surface")
        elif num_edge[i] == 3:
            nodecat.append("edge")
        elif num_edge[i] == 4:
            nodecat.append("body")

    # Initialise elcat
    elcat = []

    # Define look up table of terms
    look_up = {1: "corner", 2: "edge", 3: "surface", 4: "body"}

    # Element categorisation looped over number of elements
    for i in range(len(el)):
        # Loop over nodes in element. Only need to consider first 8 that
        # define the corner vertices
        # Reset temp_cat to infinity
        temp_cat = math.inf
        for j in range(8):
            if nodecat[el[i][j]] == "corner":
                temp_cat = 1
                break
            elif nodecat[el[i][j]] == "edge" and temp_cat > 2:
                temp_cat = 2
            elif nodecat[el[i][j]] == "surface" and temp_cat > 3:
                temp_cat = 3
            elif nodecat[el[i][j]] == "body" and temp_cat > 4:
                temp_cat = 4

        # Categorise element
        elcat.append(look_up[temp_cat])

    elcat = np.asarray(elcat)

    return elcat
