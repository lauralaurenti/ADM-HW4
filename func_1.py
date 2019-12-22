# note: set ourD=0 and visited=[starting_node] when calling the function func_1
def func_1(G, visited, starting_node, maxD, ourD):
    if ourD<=maxD:     #we haven't reached the threshold distance
        for a in G[starting_node]:   #look at every a adjacent of the starting node
            if a not in visited:     
                #print('a ',a)
                #print('visited ',visited)
                w=int(G.get_edge_data(starting_node,a)['weight']) #we add the weight of the edge to a to our distance count
                #print('ourD+w ',ourD+w)
                if ourD+w<=maxD:     #if a is reachable with a distance <= threshold
                    ourD=ourD+w
                    visited.append(a) . #we add a to the reachable and visited nodes
                    func_1(G, visited, a, maxD, ourD) #recursively calling the function on a 
    return visited
