# Script to read .dat file from ansys into Python

def readdat(fname, cwd):

    # Import regex
    import re
    import csv

    # Print statement to show successful call
    # print("Reading dat file into Python.")

    # Set filename
    fname = cwd + "/resources/mesh/" + fname + ".mechdat.dat"

    # Open file
    with open(fname, "r") as file:
        data = file.readlines()

    # Delete entries associated with file header
    del data[0:25]

    if "1" not in data[0]:
        del data[0:6]

    # start list
    temp_v = []

    # Loop over data in data for vertices
    for index, i in enumerate(data):

        # Search for E in string i
        j = re.search(r"E", i)

        # If no E found, break loop
        if j is None:

            # Delete read data from data list, as well as header for next data
            # set
            del data[0:index+7]

            # Break for loop
            break

        # Else append i to temp vertex
        else:
            temp_v.append(i)

    # Initialise el_temp - temp list for element data
    temp_el = []

    # Cycle through cell-vertex numbers
    for index, i in enumerate(data):
        # Check if on odd or even row, as data split over two rows
        if ((index) % 2) == 0:
            temp_str = i
        else:
            temp_el.append(temp_str + i)
            del temp_str

        # Check for - (from -1) signifies end of data
        j = re.search(r"-", i)

        # If - is in data, break loop as reached end of data
        if j is not None:
            break

    # Create empty vertex list, element list
    vert = []
    el = []

    # Open out vertex data and attach to vert list
    for i in range(len(temp_v)):
        vert.append(re.findall(r"\S+", temp_v[i]))

    # Delete temp_v as no longer useful
    del temp_v

    # Open out element data and attach to vert list
    for i in range(len(temp_el)):
        el.append(re.findall(r"\S+", temp_el[i]))

    # Delete temp_el as no longer useful
    del temp_el

    # Delete useless data from el list
    for i in range(len(el)):
        del el[i][0:11]

        # Convert str to int
        for j in range(len(el[i])):
            el[i][j] = int(el[i][j])

        # Convert list to tuple
        el[i] = tuple(el[i])

    # Cycle through vert to convert from scientific to decimal
    for i in range(len(vert)):
        # Delete vertex number (ref using index)
        del vert[i][0]
        # Convert scientific to decimal
        for j in range(len(vert[i])):
            vert[i][j] = float(vert[i][j])
        # Convert list to tuple
        vert[i] = tuple(vert[i])

    # Convert lists to tuples
    vert = tuple(vert)
    el = tuple(el)

    return vert, el
