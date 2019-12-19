import networkx as nx

# this is our version of Dijkstra's algorithm
def func_3(graph, node, dest):
    ret=(0)
    if graph.has_node(node)==False or graph.has_node(dest)==False:
        ret=('Not possible')
        return ret
    if nx.has_path(graph,node,dest):
        
        #previous = []
        previous = [-1]*(len(graph.nodes)+1)
        #for i in range(len(graph.nodes)+1):
        #   previous.append(-1)
        dis = [float("Inf")]*(len(graph.nodes)+1)
        seen = set()
        dis[node] = 0
        previous[node] = node
        l=[item for item in dis]
        #print("before")
        while (dest not in seen):
            #print("while")
            #print(dis)
            #l=[item for item in dis]
            #for i in range(len(l)):
            #    if i in seen:
            #        l[i]=float("Inf")
            #print(l)
            current_node = l.index(min(l))
            seen.add(current_node)
            l[current_node] = float("Inf")
            #print(current_node,' ',graph.adj[current_node])
            for v in graph.adj[current_node]:
                if dis[v] > dis[current_node] + graph[current_node][v]["weight"]:
                    #print("update:", v)
                    dis[v] = dis[current_node] + graph[current_node][v]["weight"]
                    l[v] = dis[current_node] + graph[current_node][v]["weight"]
                    previous[v] = current_node 
        #print("out")            
        path=[]
        index=dest
        node=previous[index]
        while index!=node:
            path.append(index)
            index=node
            node=previous[index]
        path.append(node)
        ret=(dis[dest], path[::-1])
    else:
        #print("qui")
        ret=('Not possible')
    return ret