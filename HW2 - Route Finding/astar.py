import csv
from queue import PriorityQueue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def astar(start, end):
    # Begin your code (Part 4)
    #load edgeFile to adj_list
    adj_list = {}
    with open(edgeFile) as f:
        csvreader = csv.reader(f)
        next(csvreader) #first row
        for row in csvreader:
            tmp = []
            if int(row[0]) in adj_list: #node exist in adjacency list
                tmp.extend(adj_list[int(row[0])]) #row[0]:start_node
            tmp.append([int(row[1]), float(row[2]), float(row[3])]) 
            #row[1]:end_node #row[2]:distance #row[3]:speed limit
            adj_list[int(row[0])] = tmp #adjacency list
            
    #load heuristicFile
    with open(heuristicFile) as f:
        csvreader = csv.reader(f)
        ids = next(csvreader) #end node id
        for index in range(1, len(ids)): #get end column index
            if (int(ids[index]) == end): #column is end node
                break
        heu = {}
        for row in csvreader:
            heu[int(row[0])] = float(row[index]) #heuristic list
    
    #Astar
    queue = PriorityQueue() #use priority queue to priority smallest distance
    visited = []
    parent = {}
    distance = {} #distance from start to node
    f = {}
    queue.put((0, start)) #(start to node + node to end distance, node)
    distance[start] = 0
    f[start] = 0
    parent[start] = None
    visited.append(start)
    path_found = None
    while not queue.empty():
        curr = queue.get()
        if curr[1] == end:
            path_found = True
            break
        if curr[1] in adj_list:
            for next_node in adj_list[curr[1]]:
                #none_visited or has smaller than f
                if next_node[0] not in visited or heu[next_node[0]]+next_node[1] + distance[curr[1]] < f[next_node[0]]:
                    queue.put((heu[next_node[0]]+next_node[1] + distance[curr[1]], next_node[0]))
                    f[next_node[0]] = heu[next_node[0]]+next_node[1] + distance[curr[1]]
                    # calculator total start to node and node to end distance
                    distance[next_node[0]] = distance[curr[1]] + next_node[1] #distance start to next_node
                    parent[next_node[0]] = curr[1] #next_node of parent
                    if next_node[0] not in visited:
                        visited.append(next_node[0])
    
    #result
    path = []      
    dist = distance[end]
    num_visited = len(visited)      

    if path_found: #store path
        path.append(end) #end - start
        while parent[end] is not None: 
            path.append(parent[end])
            end = parent[end]
        path.reverse() #reverse path to get start to end
    return path, dist, num_visited
    # load edgeFile to get adjacency list (start_node: end_node, distance, speed limit)
    # load heuristicFile to get heuritic list of node to end distance (node: distance)
    # use a* to find path, start to end smallest distance, number visited
    # queue will be priority smallest f
    # f = distance + heuristic
    # get path from parent list
    #raise NotImplementedError("To be implemented")
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
