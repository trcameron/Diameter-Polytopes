# TSP Diameter Polytope facet and point generator
#
# Authors: Thomas R. Cameron, Jonad Pulaj, Sebastian Charmot
# Date: 6/27/2020
import os
import sys
import itertools
from copy import deepcopy

#############################
#       Cycles to Binary    
#############################
def cycle_to_bin(cycle):
    """Takes a cycle permutation and returns a binary vector that stores which edges are used in the cycle."""
    # number of vertices in cycle
    n = len(cycle)
    # binary solution
    x = [0 for k in range(n*(n-1)//2)]
    # counter
    k = 0
    for i in range(n-1):
        for j in range(i+1,n):
            # index of i and j
            ind_i = cycle.index(i)
            ind_j = cycle.index(j)
            # check if i and j are adjacent
            if(abs(ind_i-ind_j)==1 or abs(ind_i-ind_j)==(n-1)):
                x[k] = 1
            # update k
            k += 1
    # return
    return x
#############################
#       Main    
#############################
def main(argv):
    """Accepts input n and t, which denote the size and type of the problem, respectively.
        If t=p, then we are generating points; if t=f, then we are generating facets."""
    try:
        # size of problem
        n = int(argv[0])
        # type of problem
        t = argv[1]
        # create points
        if(t=="p"):
            # all distinct cycles
            cycles = []
            for x in itertools.permutations(list(range(1,n))):
                temp = [0] + list(x)
                test = False
                for l in cycles:
                    test = test or (l[1:]==temp[1:][::-1])
                if(not(test)):
                    cycles.append(temp)
            # all possible 0-1 combos
            z_lst = list(itertools.product([0, 1], repeat=n*(n-1)//2))
            # build all feasible TSD points
            points = []
            for i in range(len(cycles)):
                x = cycle_to_bin(cycles[i])
                for j in range(len(cycles)):
                    y = cycle_to_bin(cycles[j])
                    for k in range(len(z_lst)):
                        z = z_lst[k]
                        test = True
                        for l in range(len(z)):
                            test = test and (x[l]+y[l]-z[l]<=1)
                        if(test):
                            row = deepcopy(x)
                            row.extend(y)
                            row.extend(z)
                            points.append(row)
            print("number of points: %d"%len(points))
            # write points to file
            f = open("point_facet_files/tsd_points%d.poly"%n,"w+")
            f.write("POINTS\n")
            for p in points:
                f.write("1")
                for k in p:
                    f.write(" %d"%k)
                f.write("\n")
            # close file
            f.close()
        # create facets
        elif(t=="f"):
            # variable list
            var_type = ["x","y","z"]
            var_list = ["1"]
            for k in range(3):
                for i in range(n-1):
                    for j in range(i+1,n):
                        var_list.append(var_type[k]+"_{%d,%d}"%(i+1,j+1))
            # open files
            f = open("point_facet_files/tsd_facets%d.txt"%n)
            g = open("point_facet_files/tsd_facets%d_clean.txt"%n,"w+")
            # read all lines of f
            lineList = f.readlines()
            row = lineList.pop(0)
            # remove unwanted characters
            row = row[108:len(row)-2].rstrip()
            # extract facets
            row = row.split(",[")
            row[0] = row[0].replace('[','')
            for k in range(len(row)):
                x = row[k][:-1]
                x = x.split(",")
                x = [int(eval(i)) for i in x]
                x_str = ""
                count = 0
                for j in range(len(x)):
                    if(x[j]!=0):
                        if(count>0):
                            x_str += " + " + str(x[j])+"*"+var_list[j]
                        else:
                            x_str += str(x[j])+"*"+var_list[j]
                        count += 1
                x_str += " >= 0\n"
                g.write(x_str)
            # close files
            f.close()
            g.close()
        # warning
        else:
            print("Input Error")
    except Exception as e: print(e)
if __name__ == '__main__':
    main(sys.argv[1:])