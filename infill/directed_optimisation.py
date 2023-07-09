import numpy as np
from numpy.random.mtrand import beta
import scipy.optimize as optimize
import solve


# Mass calculation for a given part, relative den array and absolute density
def masscalc(part, den, density):

    import numpy as np

    if isinstance(den, list):
        den = np.asarray(den)
    else:
        den = np.ones(len(part.vol))*den

    cell_mass = []

    for i, vol in enumerate(part.vol):

        cell_mass.append(vol * den[i]*density)

    mass = sum(cell_mass)

    return(mass)


# CoM calculation for a given part, relative den array and absolute density
def comcalc(part, den):

    import numpy as np

    if isinstance(den, list):
        den = np.asarray(den)
    else:
        den = np.ones(len(part.vol))*den

    x = []
    y = []
    z = []
    cell_mass = []

    for i, vol in enumerate(part.vol):

        cell_mass.append(vol * den[i])

        x.append(cell_mass[-1]*part.cpts[i][0])
        y.append(cell_mass[-1]*part.cpts[i][1])
        z.append(cell_mass[-1]*part.cpts[i][2])

    comx = sum(x)/sum(cell_mass)
    comy = sum(y)/sum(cell_mass)
    comz = sum(z)/sum(cell_mass)

    com = [comx, comy, comz]

    return(com)


def initialguess(mass_props, denset, shell, body, density):

    # Set solid shell
    den_shell = np.ones(len(shell.vol))

    # Set initial minimum structure body density
    den_body = np.ones(len(body.vol)) * denset[0]

    # Find CoM of shell
    com_shell = comcalc(shell, den_shell)
    # print(f"CoM Shell = {com_shell}")

    # Find mass of shell
    mass_shell = masscalc(shell, den_shell, density)
    # print(f"Mass shell = {mass_shell}")

    # Find initial CoM of body
    com_body = comcalc(body, den_body)

    # print(f"CoM Body = {com_body}")

    # Find initial mass of body
    mass_body_i = masscalc(body, den_body, density)
    # print(f"Mass Body Initial = {mass_body_i}")

    # Find total initial mass
    mass_initial = mass_shell+mass_body_i

    # Find required body mass
    mass_diff = mass_props.mass - mass_shell - mass_body_i
    # print(f"Mass diff = {mass_diff}")

    # Find increase in mass from one cell of higher density
    mcell = (denset[-1] - denset[0]) * (sum(body.vol)/len(body.vol)) * density
    # print(f"Mass increase of cell = {mcell}")

    # Find number of cells that need to have higher density
    num_cells = round(mass_diff/mcell)
    print(f"Num cells = {num_cells}")

    # Find initial CoM of whole
    com_initial = []
    for i in range(3):

        comtemp = ((com_shell[i]*mass_shell)+(com_body[i]*mass_body_i))/(mass_body_i+mass_shell)
        
        com_initial.append(comtemp)
    # print(f"CoM Initial = {com_initial}")
    
    # Get required CoM
    com_req = [mass_props.comx, mass_props.comy, mass_props.comz]
    # print(f"CoM Required = {com_req}")
    
    # Find average cell position in each axis to achieve CoM

    com_den = []

    for i in range(3):

        comhigh = (mass_initial/mass_diff) * (com_req[i] - com_initial[i]) + com_req[i]
        com_den.append((comhigh*mass_diff + com_body[i]*mass_body_i)/(mass_diff+mass_body_i))
    
    # print(f"CoM Den = {com_den}")

    # Find average probability
    req_prob = num_cells/len(den_body)

    return req_prob, com_den


def expden(beta, x):

    prob = np.exp(-x/beta)

    return prob

  
def probfind(beta, cpts, com_den):
    # Initialise list of probabilities
    probs = []

    # Initialise list of distances of cells from com_den    
    rs = []

    # Cycle through cells and find r
    for cpt in cpts:

        diffs = [(cpt[i] - com_den[i]) for i in range(3)]

        diffs = [pow(diff, 2) for diff in diffs]

        r = pow(sum(diffs), 0.5)

        rs.append(r)

    # Find probability of high density cell for all cells
    for r in rs:

        probs.append(expden(beta, r))

    return probs


def dengen(probs, denset):

    # Initialise density array
    den = []

    # Generate array of random numbers
    for prob in probs:
        den.append(np.random.choice(denset, p=[1-prob, prob]))
    
    return den

   
def f_beta(beta, cpts, com_den, req_prob, denset):

    probs = probfind(beta, cpts, com_den)

    den = dengen(probs, denset)

    numcells = 0

    for val in den:
        if val != denset[0]:
            numcells += 1

    numcells_req = round(req_prob * len(den))

    # prob_av = sum(probs)/len(probs)

    # prob_av_diff = abs(prob_av - req_prob)

    # return prob_av_diff

    cost = abs(numcells_req - numcells)

    return cost


def optbeta(cpts, com_den, req_prob, denset):

    # Initialise list of distances of cells from com_den    
    rs = []

    # Cycle through cells and find r
    for cpt in cpts:

        diffs = [(cpt[i] - com_den[i]) for i in range(3)]

        diffs = [pow(diff, 2) for diff in diffs]

        r = pow(sum(diffs), 0.5)

        rs.append(r)

    bracket = [1, 1000]

    result = optimize.minimize_scalar(f_beta, method="bounded", args=(cpts, com_den, req_prob, denset), bounds=bracket, options={"xatol":4})

    if result.success is True:
        beta = result.x
    else:
        print(result.message)
        beta = None
        print(result.x)
    
    return beta


def directcom(denset, req_prob, com_den_req, body):

    import math
    import statistics

    etol = 0
    cetol = 0
    maxit = 8
    intcomits = 5
    error = math.inf
    preerror = math.inf

    com_den = []
    [com_den.append(i) for i in com_den_req]

    it = 0

    com = None

    while error > etol and it < maxit:

        print(f"New CoM Iteration started. It: {it}")

        if it > 0:

            for i in range(3):

                com_den[i] +=  com_den_req[i] - com[i]
                # print(com_den_req[i] - com[i])
       
        # print(com_den)
        # if com is not None:
        #     print(com)

        beta = optbeta(body.cpts, com_den, req_prob, denset) 

        probs = probfind(beta, body.cpts, com_den)
        x = []
        y = []
        z = []

        for i in range(intcomits):

            den = dengen(probs, denset)

            com = comcalc(body, den)

            x.append((com[0]))
            y.append((com[1]))
            z.append((com[2]))

        com_err = [x, y, z]
        
        x = statistics.mean(x)
        y = statistics.mean(y)
        z = statistics.mean(z)

        com = [x, y, z]

        error = 0

        for i in range(3):
            
            temperror = 0

            for j in range(len(com_err[i])):
            
                temperror += abs(abs(com_err[i][j]) - abs(com_den_req[i]))

            temperror = temperror/len(com_err[i])

            error += temperror

        if preerror <= error + cetol and preerror >= error - cetol:
            
            error = etol

        it += 1

        preerror = error

    if it >= maxit:
        print("Maximum CoM iterations reached")

    return com_den

# Multiprocessing call
def monteopt(args):

    den = dengen(args[-1], args[-3])

    cost, den = solve.solvemain(den, args)

    return(cost)

# Master function for directed optimisation
def directedopt(partdef, mass_props, abs_density, denset, fname, model):
    
    # Import time to measure performance of code
    import time
    import csv
    import math

    import concurrent.futures

    # This function is intended to find the best CoM and beta point for use in the model
    # It then uses MCO using modified cell-by-cell probabilities to find a best guess at
    # the internal structure.

    import solid_shell
    from foldpath import foldpathmain

    # Find start time
    starttime = time.perf_counter()

    # Split part into shell and body
    (shell, body) = solid_shell.main(partdef)

    req_prob, com_den_req = initialguess(mass_props, denset, shell, body, abs_density)
    
    com_den_final = directcom(denset, req_prob, com_den_req, body)

    beta = optbeta(body.cpts, com_den_final, req_prob, denset)

    probs = probfind(beta, body.cpts, com_den_final)

    # Then use probs to find several iterations of den and get obj. cost.

    print("MCO Starting")

    # Define number of iterations
    N = 100

    # Get folder path for results
    foldpath = foldpathmain(model)

    # Initialise arg list
    arg = []

    # Create arg for parallel processing
    for i in range(N):
        temp_list = [i, body, shell, N, abs_density, denset[-1], denset[0],
                     mass_props, foldpath, denset, fname, probs]
        arg.append(temp_list)

    # results = [monteopt(args) for args in arg]

    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(monteopt, arg)
    
    # Convert generator to tuple
    res_list = tuple(results)

    # Initialise best cost (lower is better)
    best_cost = math.inf

    # Cycle through all results to find best cost
    for i in range(N):
        if abs(res_list[i]) < abs(best_cost):
            # If cost is lower (better) than current best, overwrite best
            # result
            best_cost = res_list[i]
            # Save best iteration
            best_it = i+1

    # Find end time
    endtime = time.perf_counter()

    # Find time code ran for
    runtime = endtime-starttime

    # Create csv containing costs
    fname = foldpath + "/costs.csv"

    # Write result to file
    with open(fname, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(res_list)
        wr.writerow([runtime])

    # Print best result
    print(f"Best Cost: {best_cost}")
    print(f"Best it: {best_it}")

    with open(foldpath + "/it" + str(best_it) + ".csv", "r", newline="") as f:
        print("Iteration file open")
        rr = csv.reader(f, delimiter=",")
        for i, row in enumerate(rr):

            if i != 0:

                best_mp = row
            
    print(best_mp)

    return best_cost
