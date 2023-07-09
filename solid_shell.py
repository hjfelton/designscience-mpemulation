# Script to split the part into a shell and body

def main(partdef):

    import numpy as np

    # Initialise lists for shell and body
    temp_shell = []
    temp_body = []

    for i in range(len(partdef.elmcat)):
        if partdef.elmcat[i] != "body":
            temp_shell.append(i)
        else:
            temp_body.append(i)

    # Create shell and body objects
    shelldef = shell(partdef, temp_shell)
    bodydef = body(partdef, temp_body)

    return shelldef, bodydef


class shell:
    # Structures shell object
    def __init__(self, partdef, temp):

        # import numpy
        import numpy as np

        # Record cell numbers used
        self.celllist = temp

        # Initialise lists (matching partdef)
        self.elm = []
        self.vert = []
        self.vol = []
        self.elmcat = []
        self.cpts = []

        # Make solid shell
        self.den = np.ones(len(temp)) # * 2.75

        # Append data for cells in shell
        for i in temp:
            self.elm.append(partdef.elm[i])
            self.vert.append(partdef.vert[i])
            self.vol.append(partdef.vol[i])
            self.elmcat.append(partdef.elmcat[i])
            self.cpts.append(partdef.cpts[i])

        # Convert to arrays
        self.elm = np.asarray(self.elm)
        self.vert = np.asarray(self.vert)
        self.vol = np.asarray(self.vol)
        self.elmcat = np.asarray(self.elmcat)
        self.cpts = np.asarray(self.cpts)


class body:
    # Structures body object
    def __init__(self, partdef, temp):

        # import numpy
        import numpy as np
        import csv

        # Record cell numbers used
        self.celllist = temp

        # Initialise lists (matching partdef)
        self.elm = []
        self.vert = []
        self.vol = []
        self.elmcat = []
        self.cpts = []

        # Append data for cells in body
        for i in temp:
            self.elm.append(partdef.elm[i])
            self.vert.append(partdef.vert[i])
            self.vol.append(partdef.vol[i])
            self.elmcat.append(partdef.elmcat[i])
            self.cpts.append(partdef.cpts[i])

        # Convert to arrays
        self.elm = np.asarray(self.elm)
        self.vert = np.asarray(self.vert)
        self.vol = np.asarray(self.vol)
        self.elmcat = np.asarray(self.elmcat)
        self.cpts = np.asarray(self.cpts)
