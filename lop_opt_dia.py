# LOP Optimal Diameter
#
# Authors: Thomas R. Cameron, Jonad Pulaj, Sebastian Charmot
# Date: 6/26/2020
import cplex
import numpy as np
from parallel_rank_vis import AB_to_P2, spider
#####################################
#       LOP Optimal Diameter        
#####################################
def lopOptDia(a):
    """Computes optimal diameter of the LOP given the objective function 'a'.
        It is assumed that the objective function is integer valued.
        Also, it is assumed that the objective function is passed as an nxn matrix."""
    # size
    n = len(a)
    m = np.amin(a)
    # objective function and bounds
    obj = a.reshape(n*n)
    for i in range(n):      # avoid diagonal entries in maximization
        obj[n*i+i] = m - 10
    obj = np.concatenate((obj,obj,-(1/(2*n*n))*np.ones(n*n)))
    lb = np.zeros(3*n*n)
    ub = np.ones(3*n*n)
    # symmetric constraints (x)
    count = 0; sense = ""
    rows = []; cols = []; vals = []; rhs = []
    for i in range(n-1):
        for j in range(i+1,n):
            rows.extend([count,count])
            cols.extend([n*i+j,n*j+i])
            vals.extend([1.0,1.0])
            rhs.append(1.0)
            sense = sense + "E"
            count = count + 1
    # symmetric constraints (y)
    for i in range(n-1):
        for j in range(i+1,n):
            rows.extend([count,count])
            cols.extend([n*i+j+n*n,n*j+i+n*n])
            vals.extend([1.0,1.0])
            rhs.append(1.0)
            sense = sense + "E"
            count = count + 1
    # transitive constraints (x)
    for i in range(n-1):
        for j in range(i+1,n):
            for k in range(i+1,n):
                if(j!=k):
                    rows.extend([count,count,count])
                    cols.extend([n*i+j,n*j+k,n*k+i])
                    vals.extend([1.0,1.0,1.0])
                    rhs.append(2.0)
                    sense = sense + "L"
                    count = count + 1
    # transitive constraints (y)
    for i in range(n-1):
        for j in range(i+1,n):
            for k in range(i+1,n):
                if(j!=k):
                    rows.extend([count,count,count])
                    cols.extend([n*i+j+n*n,n*j+k+n*n,n*k+i+n*n])
                    vals.extend([1.0,1.0,1.0])
                    rhs.append(2.0)
                    sense = sense + "L"
                    count = count + 1
    # diameter constraints (x,y,z)
    for i in range(n):
        for j in range(n):
            if(j!=i):
                rows.extend([count,count,count])
                cols.extend([n*i+j,n*i+j+n*n,n*i+j+2*n*n])
                vals.extend([1.0,1.0,-1.0])
                rhs.append(1.0)
                sense = sense + "L"
                count = count + 1
    # cplex problem variable
    prob = cplex.Cplex()
    # quiet results
    prob.set_results_stream(None)
    # maximiation problem
    prob.objective.set_sense(prob.objective.sense.maximize)
    # problem variables
    prob.variables.add(obj=obj, lb=lb, ub=ub)
    for j in range(prob.variables.get_num()):
        prob.variables.set_types(j,prob.variables.type.integer)
    # linear constraints
    prob.linear_constraints.add(rhs=rhs, senses=sense)
    prob.linear_constraints.set_coefficients(zip(rows, cols, vals))
    # alg method
    alg = prob.parameters.lpmethod.values
    prob.parameters.lpmethod.set(alg.auto)
    # solve problem
    prob.solve()
    print(prob.solution.status[prob.solution.get_status()])
    # solution variables
    var = prob.solution.get_values()
    x = np.sum(np.array(var[0:n*n]).reshape((n,n)),axis=1).argsort()[::-1]
    y = np.sum(np.array(var[n*n:2*n*n]).reshape((n,n)),axis=1).argsort()[::-1]
    z = np.array(var[2*n*n:3*n*n]).reshape((n,n))
    # optimal diameter
    optDia = n*(n-1) - 2*np.sum(z)
    # return
    return x, y, optDia
#####################################
#       Main       
#####################################
def main():
    # examples
    adj = [np.array([[0.,1,1,1,1,1],[0,0.,1,1,1,1],[0,0,0.,1,1,1],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
            np.array([[0.,1,1,1,1,1],[0,0.,0,1,1,1],[1,0,0.,1,1,1],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
            np.array([[0.,1,1,1,0,0],[0,0.,1,0,0,0],[0,0,0.,0,0,0],[0,0,0,0.,1,1],[0,0,0,0,0.,1],[0,0,0,0,0,0.]]),
            np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,0],[0,0,0.,1,0,0],[0,0,0,0.,1,0],[0,0,0,0,0.,1],[1,0,0,0,0,0.]]),
            np.array([[0.,1,1,1,1,1],[1,0.,1,1,1,1],[1,1,0.,1,1,1],[1,1,1,0.,1,1],[1,1,1,1,0.,1],[1,1,1,1,1,0.]]),
            np.zeros((6,6))
            ]
    # testing
    for num in range(6):
        a = adj[num]
        x,y,optDia = lopOptDia(a)
        print(x,y,optDia/(6*5))
        spider(AB_to_P2(x,y))
if __name__ == '__main__':
    main()