# LOP Diameter Polytope facet and point generator
#
# Authors: Thomas R. Cameron, Jonad Pulaj, Sebastian Charmot
# Date: 6/27/2020
import os
import sys
import itertools
from copy import deepcopy

#############################
#   Permutations to Binary      
#############################
def perm_to_bin(perm):
    x = []
    for i in range(len(perm)):
        for j in range(len(perm)):
            if(i!=j):
                if(perm[i]<perm[j]):
                    x.append(1)
                else:
                    x.append(0)
    return x
#############################
#   Main      
#############################
def main(argv):
    try:
        # size of problem
        n = int(argv[0])
        # type of problem
        t = argv[1]
        # create points
        if(t=="p"):
            # all possible permutations
            perm = []
            for x in itertools.permutations(list(range(n))):
                perm.append(list(x))
            # all possible 0-1 combos
            z_lst = list(itertools.product([0, 1], repeat=n*(n-1)))
            # build all feasible LOD points
            points = []
            for i in range(len(perm)):
                x = perm_to_bin(perm[i])
                for j in range(len(perm)):
                    y = perm_to_bin(perm[j])
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
            f = open("point_facet_files/lod_points%d.poly"%n,"w+")
            f.write("POINTS\n")
            for p in points:
                f.write("1")
                for k in p:
                    f.write(" %d"%k)
                f.write("\n")
        # create facets
        elif(t=="f"):
            # variable list
            var_type = ["x","y","z"]
            var_list = ["1"]
            for k in range(3):
                for i in range(n):
                    for j in range(n):
                        if(i!=j):
                            var_list.append(var_type[k]+"_{%d,%d}"%(i+1,j+1))
            # open files
            f = open("point_facet_files/lod_facets%d.txt"%n)
            g = open("point_facet_files/lod_facets%d_clean.txt"%n,"w+")
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