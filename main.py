import func_1 as f1
import func_3 as f3
import pandas as pd
import csv
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pylab import *
import itertools

#DATA COLLECTION
# Cleaning data of coordinates and appending all the nodes in a list.
# We consider only the useful rows and we split them to have a csv with the
# the node_id, longitude and latitude on separate columns

all_nodes = []

with open('C:\\Users\\bo\\Desktop\\Laura\\Istruzione\\Data Science\\Algorithmic Methods of Data Mining\\Homeworks\\HW5\\USA-road-d.CAL.co', 'r') as inp,\
        open('C:\\Users\\bo\\Desktop\\Laura\\Istruzione\\Data Science\\Algorithmic Methods of Data Mining\\Homeworks\\HW5\\cle_USA-road-d.CAL.co.csv', 'w') as out:
#with open('/Users/caterina/PycharmProjects/ADM5/USA-road-d.CAL.co', 'r') as inp,\
 #       open('/Users/caterina/PycharmProjects/ADM5/cle_USA-road-d.CAL.co.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[0][0] == "v":
            writer.writerow(row)
            tmp = row[0].split()
            all_nodes.append(int(tmp[1]))

#print("Number of points:", len(all_nodes))

# Now we create the DataFrame corresponding to the
# file USA-road-d.CAL.co and add titles to the columns

usaCoordDf = pd.read_csv('C:\\Users\\bo\\Desktop\\Laura\\Istruzione\\Data Science\\Algorithmic Methods of Data Mining\\Homeworks\\HW5\\cle_USA-road-d.CAL.co.csv', sep=' ', delimiter=None, header=None)
#usaCoordDf = pd.read_csv('/Users/caterina/PycharmProjects/ADM5/cle_USA-road-d.CAL.co.csv', sep=' ', delimiter=None, header=None)
usaCoordDf = usaCoordDf.drop(usaCoordDf.columns[0], axis=1)
usaCoordDf.columns = ["node", "coord1", "coord2"]
usaCoordDf.set_index('node', inplace=True)

usaCoordDf

# We clean the USA-road-d.CAL.gr file and we create the network_distance graph
# (base_graph) where all the edges have weight = 1 and the nodes have their coordinates
# saved in the attribute "pos"

def create_graph_base():

    g_base = nx.Graph()
    with open('C:\\Users\\bo\\Desktop\\Laura\\Istruzione\\Data Science\\Algorithmic Methods of Data Mining\\Homeworks\\HW5\\USA-road-d.CAL.gr', 'r') as inp:
    #with open('/Users/caterina/PycharmProjects/ADM5/USA-road-d.CAL.gr', 'r') as inp:
        for row in csv.reader(inp):
            if row[0][0] == "a":
                tmp = row[0].split()
                c1 = int(usaCoordDf.loc[int(tmp[1]), "coord1"])
                c2 = int(usaCoordDf.loc[int(tmp[1]), "coord2"])
                pos=[c1,c2]
                g_base.add_edge(int(tmp[1]), int(tmp[2]), weight=1)
                g_base.add_node(int(tmp[1]), p=pos)

    return g_base

# We clean the USA-road-d.CAL.gr file and we create the distance graph
# (dist_graph) where all the edges have the weight specified in the file
# and the nodes have their coordinates saved in the attribute "pos"

def create_graph_dist():

    g_dist = nx.Graph()
    with open('C:\\Users\\bo\\Desktop\\Laura\\Istruzione\\Data Science\\Algorithmic Methods of Data Mining\\Homeworks\\HW5\\USA-road-d.CAL.gr', 'r') as inp:
    #with open('/Users/caterina/PycharmProjects/ADM5/USA-road-d.CAL.gr', 'r') as inp:
        for row in csv.reader(inp):
            if row[0][0] == "a":
                tmp = row[0].split()
                c1 = int(usaCoordDf.loc[int(tmp[1]), "coord1"])
                c2 = int(usaCoordDf.loc[int(tmp[1]), "coord2"])
                pos=[c1,c2]
                g_dist.add_edge(int(tmp[1]), int(tmp[2]), weight=int(tmp[3]))
                g_dist.add_node(int(tmp[1]), p=pos)

    return g_dist

# We clean the USA-road-t.CAL.gr file and we create the time distance graph
# (time_graph) where all the edges have the weight specified in the file
# and the nodes have their coordinates saved in the attribute "pos"

def create_graph_time():

    g_time = nx.Graph()
    with open('C:\\Users\\bo\\Desktop\\Laura\\Istruzione\\Data Science\\Algorithmic Methods of Data Mining\\Homeworks\\HW5\\USA-road-t.CAL.gr', 'r') as inp:#,\
    #with open('/Users/caterina/PycharmProjects/ADM5/USA-road-t.CAL.gr', 'r') as inp:
        for row in csv.reader(inp):
            if row[0][0] == "a":
                tmp = row[0].split()
                c1 = int(usaCoordDf.loc[int(tmp[1]), "coord1"])
                c2 = int(usaCoordDf.loc[int(tmp[1]), "coord2"])
                pos=[c1,c2]
                g_time.add_edge(int(tmp[1]), int(tmp[2]), weight=int(tmp[3]))
                g_time.add_node(int(tmp[1]), p=pos)

    return g_time

#Visualization Functions
def genericVisualization(nodes, start):
    g_vis=g_base.subgraph(nodes)
    plt.figure(figsize=(20,20))
    pos=nx.get_node_attributes(g_vis,'p')
    plt.scatter(usaCoordDf['coord1'], usaCoordDf['coord2'], color='gray')
    draw_networkx(g_vis, pos, with_labels=False, node_size=30, node_color='b', edge_color='r')
    nx.draw_networkx_nodes(g_vis,pos, nodelist=start, node_color='g', node_size=100)
    plt.show()

def detailedVisualization(nodes, start, input_dist):
    g_vis=g_base.subgraph(nodes)
    plt.figure(figsize=(20,20))
    pos=nx.get_node_attributes(g_vis,'p')
    # Choosing the right color for the edge type
    dist_color='black'
    if input_dist=='t(x,y)':
        dist_color='red'
    elif input_dist=='d(x,y)':
        dist_color='yellow'
    elif input_dist=='network_distance':
        dist_color='cyan'
    draw_networkx(g_vis, pos, with_labels=False, node_size=10, node_color='b', width=2, edge_color=dist_color)
    nx.draw_networkx_nodes(g_vis,pos, nodelist=start, node_color='g', node_size=100)
    plt.show()

#Functionality 1 - Find the Neighbours!
#This is the genaral function for the first functionality;
# depending on the given input it calls the actual core function
# with the right input

def func1(v,dist,d):
    visited=[v]
    ourD=0
    if dist=='t(x,y)':
        vis=f1.func_1(g_time, visited, v, d, ourD)
    elif dist=='d(x,y)':
        vis=f1.func_1(g_dist, visited, v, d, ourD)
    elif dist=='network_distance':
        vis=f1.func_1(g_base, visited, v, d, ourD)
    else:
        print('distance error')
    return vis

#Functionality 2 - Find the smartest Network!
# This function computes the cost of an ordered route.
# We start from the node in input and visit all the nodes
# in the input set dest_list in order. To compute the total
# cost of this path we call func_3, our implementation of
# Djikstra's algorithm, to find the minimum cost between a
# source node and a destination node. We call func_3 on all
# the ordered pair of our path and concatenate the results
# to get the whole path and sum the costs to get the total cost

def func_path(graph, node, dest_list, min_w=None):

    if min_w == None: min_w = float("Inf")
    ret=[]
    p = 0
    l = f3.func_3(graph, node, dest_list[0])
    if l!=('Not possible'):
        p += l[0]
        if p < min_w:
            for i in l[1]:
                ret.append(i)
        else:
            return "Too expensive"
    else:
        ret=[('Not possible')]
        return ret
    for n in range( len(dest_list)-1):
        l = f3.func_3(graph, dest_list[n], dest_list[n+1])
        if l!=('Not possible'):
            p += l[0]
            if p < min_w:
                for i in l[1][1:]:
                    ret.append(i)
            else:
                return "Too expensive"
        else:
            ret=[('Not possible')]
            return ret

    return (ret, p)

# This function considers all the possible orders
# in which we may visit the nodes given as input.
# For every ordered route we compute the cost thanks to the
# funch_path function and the we choose the route that
# has the lower cost. Also, while computing the cost of a route,
# if we exceed the current minimum cost we skip to the next one.
# If the considered route is not connected we return "Not possible".

def func_2(graph, to_visit):
    perm = list(itertools.permutations(to_visit))
    final = ([], float("Inf"))
    for p in perm:
        tmp = func_path(graph, p[0], p[1:], final[1])
        if tmp != "Too expensive":
            if tmp[0] != ('Not possible') and tmp[1] < final[1]:
                final = tmp
            if tmp[0] == ('Not possible'):
                return ("Not possible")
        #else: print("Too expensive")
    if final == ([], float("Inf")):
        return ("Not possible")
    return final

# This is the genaral function for the second functionality;
# depending on the given input it calls the actual core
# function with the right input

def func2(dist, l):
    if dist=='t(x,y)':
        vis=func_2(g_time, l)
    elif dist=='d(x,y)':
        vis=func_2(g_dist, l)
    elif dist=='network_distance':
        vis=func_2(g_base, l)
    else:
        print('distance error')
    return vis


#Functionality 3 - Shortest Ordered Route
# This is the genaral function for the third functionality;
# depending on the given input it calls the actual core
# function with the right input.
# It works by concatenating the subpaths of the input path
# using the func_path function (which is explained in the above sections)


def func3(v,d,dist):
    if dist=='t(x,y)':
        vis=func_path(g_time, v, d)[0]
    elif dist=='d(x,y)':
        vis=func_path(g_dist, v, d)[0]
    elif dist=='network_distance':
        vis=func_path(g_base, v, d)[0]
    else:
        print('distance error')
    return vis

#Functionality 4 - Shortest Route
# This is the core function for functionality 4.
# It works by considering all the possbile ways to
# visit the input nodes given a fixed start and end,
# and then choosing the one with lower cost.
# The cost of a path is computed, again, by the func_path
# funcion, which is described in the sections above.
# If the nodes are not connetced this functions returns
# "Not possible".
# While computing the cost of a route, if we exceed the
# current minimum cost we skip to the next one.

def inner_4(graph, start, to_visit):

    nodes = [start]+to_visit
    perm = list(itertools.permutations(nodes))
    perm = [x for x in perm if x[0]==start and x[-1]==to_visit[-1]]
    final = ([], float("Inf"))
    for p in perm:
        tmp = func_path(graph, p[0], p[1:], final[1])
        if tmp != "Too expensive":
            if tmp[0] != ('Not possible') and tmp[1] < final[1]:
                final = tmp
            if tmp[0] == ('Not possible'):
                return ("Not possible")
        #else: print("Too expensive")
    if final == ([], float("Inf")):
        return ("Not possible")
    return final

# This is the genaral function for the fourth functionality;
# depending on the given input it calls the actual core
# function with the right input.

def func4(start, nodes, dist):
    if dist=='t(x,y)':
        vis=inner_4(g_time, start, nodes)
    elif dist=='d(x,y)':
        vis=inner_4(g_dist,start, nodes )
    elif dist=='network_distance':
        vis=inner_4(g_base, start, nodes)
    else:
        print('distance error')
    return vis


def main_func(f):

    d_functions = ["d(x,y)", "t(x,y)", "network_distance"]

    if f == 1:
        print("Plese insert a valide node, a distance function and a distance threshold")
        inp = input()
        inp = inp.split()
        if len(inp) > 3: print("Too many arguments"); return
        inp[0] = int(inp[0])
        inp[2] = int(inp[2])
        #print(inp)
        if inp[1] not in d_functions:
            print("No such distance function"); return

        res = func1(inp[0], inp[1], inp[2])
        print(res)
        genericVisualization(res, [inp[0]])
        detailedVisualization(res, [inp[0]], inp[1])


    elif f == 2:
        print("Plese insert a list of nodes and a distance function")
        inp = input()
        inp = inp.split()
        if len(inp) > 2: print("Too many arguments"); return
        inp[0] = list(inp[0].split(','))
        inp[0] = [int(x) for x in inp[0]]
        #print(inp)
        if inp[1] not in d_functions:
            print("No such distance function"); return

        res = func2(inp[1], inp[0])
        print(res)
        genericVisualization(res[0], inp[0])
        detailedVisualization(res[0], inp[0], inp[1])


    elif f == 3:
        print("Plese insert a valide node, an ordered list of nodes and a distance function")
        inp = input()
        inp = inp.split()
        if len(inp) > 3: print("Too many arguments"); return
        inp[0] = int(inp[0])
        inp[1] = list(inp[1].split(','))
        inp[1] = [int(x) for x in inp[1]]
        #print(inp)
        if inp[2] not in d_functions:
            print("No such distance function"); return

        res = func3(inp[0], inp[1], inp[2])
        print(res)
        genericVisualization(res, [inp[0]])
        detailedVisualization(res, [inp[0]], inp[2])


    elif f == 4:
        print("Plese insert a valide node, a list of nodes and a distance function")
        inp = input()
        inp = inp.split()
        if len(inp) > 3: print("Too many arguments"); return
        inp[0] = int(inp[0])
        inp[1] = list(inp[1].split(','))
        inp[1] = [int(x) for x in inp[1]]
        #print(inp)
        if inp[2] not in d_functions:
            print("No such distance function"); return

        res = func4(inp[0], inp[1], inp[2])
        print(res)
        genericVisualization(res[0], inp[1])
        detailedVisualization(res[0], inp[1], inp[2])

    else:
        print("No such functionality")



print("I'm creating graph for distance d(x,y)")
g_dist = create_graph_dist()
print("I'm creating graph for network distance")
g_base = create_graph_base()
print("I'm creating graph for distance t(x,y)")
g_time = create_graph_time()

print("Enter a number for corresponding function (1,2,3,4), 0 to exit")
nFunc = int(input())
while(nFunc!=0):
    main_func(nFunc)
    print("Enter a number for corresponding function (1,2,3,4), 0 to exit")
    nFunc = int(input())
