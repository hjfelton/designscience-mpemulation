# Script to retrieve the required mass properties

def getmass(fname, cwd):

    # Import csv
    import csv

    # Set filename
    fname = cwd + "/resources/mass/" + fname + ".csv"

    # Open file
    with open(fname, "r") as file:
        # Read csv data
        data = csv.reader(file)
        # Initialise dict
        d = {}
        # Loop through rows
        for row in data:
            # Split data into keys and values
            k, v = row
            # Add values to dicts, convert value to float
            d[k] = float(v)

    # Create new mass dict
    mass = {"mass": d["mass"]}
    # Create new com dict
    com = {"comx": d["comx"], "comy": d["comy"], "comz": d["comz"]}
    # Create new MoI dict NB: only considering moments of inertia, not products
    inertia = {"ixx": d["ixx"], "iyy": d["iyy"], "izz": d["izz"]}

    mass_props = Mass(mass, com, inertia)

    return mass_props


class Mass:
    # Structures object containing mass properties
    def __init__(self, mass, com, inertia):

        self.mass = mass["mass"]
        self.comx = com["comx"]
        self.comy = com["comy"]
        self.comz = com["comz"]
        self.ixx = inertia["ixx"]
        self.iyy = inertia["iyy"]
        self.izz = inertia["izz"]
