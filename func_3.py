import networkx as nx

# this is our version of Dijkstra's algorithm
def func_3(graph, node, dest):
    ret=(0)
    if graph.has_node(node)==False or graph.has_node(dest)==False:
        ret=('Not possible')      #we check if both nodes actually exist
        return ret
    if nx.has_path(graph,node,dest): #if they do and they are connected
        
        previous = [-1]*(len(graph.nodes)+1)  #list of fathers to recreate path at the end
        dis = [float("Inf")]*(len(graph.nodes)+1)  #list of distances to be updated every time
        seen = set()  #set of nodes for which we have the definitive minimum distance
        dis[node] = 0  #starting node is his own father
        previous[node] = node  #starting node has distance 0 from himself
        l=[item for item in dis] . #copy of the distance list 

        while (dest not in seen):  #while I haven't found the shortest path to my destination
            current_node = l.index(min(l))  #take the node at min distance from the start which is not in see yet
            seen.add(current_node)         #add it in seen 
            l[current_node] = float("Inf") . #pretend its distance from start in "Inf" to avoid choosing it again (we only do this in the copy list, not dist)
            #print(current_node,' ',graph.adj[current_node])
            for v in graph.adj[current_node]:    #for every adjacent it has 
                if dis[v] > dis[current_node] + graph[current_node][v]["weight"]:  #if reaching it this way is cheaper than the route I already knwo
                    dis[v] = dis[current_node] + graph[current_node][v]["weight"]  #update the distance cost
                    l[v] = dis[current_node] + graph[current_node][v]["weight"]    #update the distance cost in the copy list
                    previous[v] = current_node                                     #update the father list (how I got here)
        
        # We need this part to get the path to reach dest (we go back from dest to start through the previous list and then reverse the list)
        path=[]
        index=dest
        node=previous[index]
        while index!=node:
            path.append(index)
            index=node
            node=previous[index]
        path.append(node)
        ret=(dis[dest], path[::-1])
    else:                     #if the nodes are not connected it's impossible to find the path
        ret=('Not possible')
    return ret
