# note: set ourD=0 and visited=[starting_node] when calling the function func_1
def func_1(G, visited, starting_node, maxD, ourD):
    if ourD<=maxD:
        for a in G[starting_node]:
            if a not in visited:
                #print('a ',a)
                #print('visited ',visited)
                w=int(G.get_edge_data(starting_node,a)['weight'])
                #print('ourD+w ',ourD+w)
                if ourD+w<=maxD:
                    ourD=ourD+w
                    visited.append(a)
                    func_1(G, visited, a, maxD, ourD)
    return visited
