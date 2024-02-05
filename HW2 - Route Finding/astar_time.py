import csv
from queue import PriorityQueue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    
    #load edgeFile to adj_list
    speed = {}
    adj_list = {}
    with open(edgeFile) as f:
        csvreader = csv.reader(f)
        next(csvreader) #first row
        for row in csvreader:
            tmp = []
            if int(row[0]) in adj_list: #node exist in adjacency list
                tmp.extend(adj_list[int(row[0])]) #row[0]:start_node
            tmp.append([int(row[1]), float(row[2])*3.6/float(row[3])]) #km/h 2 m/s
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
    
    #Astar_time        
    queue = PriorityQueue() #use priority queue to priority smallest distance 
    visited = []
    parent = {}
    sec = {}
    f = {}
    queue.put((0.0, start)) #(distance from start to node, node)
    sec[start] = 0.0
    f[start] = 0.0
    visited.append(start)
    parent[start] = None
    path_found = False  
    while not queue.empty():
        curr = queue.get() #curr[0]:distance curr[1]:current node
        
        if curr[1] == end: #current node is end
            path_found = True
            break
        if curr[1] in adj_list:
            for next_node in adj_list[curr[1]]:
                #none_visited or has smaller than distance
                if next_node[0] not in visited or heu[next_node[0]]/27.8+next_node[1]+sec[curr[1]]<f[next_node[0]]: 
                    f[next_node[0]] = heu[next_node[0]]/27.8+next_node[1]+sec[curr[1]]
                    queue.put((f[next_node[0]], next_node[0])) 
                    #calculator start to next_node distance
                    sec[next_node[0]] = sec[curr[1]] + next_node[1] #calc time from start to node
                    parent[next_node[0]] = curr[1] #parent of next_node
                    if next_node[0] not in visited:
                        visited.append(next_node[0])
    path = []      
    time = curr[0]
    num_visited = len(visited)
    if path_found: #store path
        path.append(end) #end - start
        while parent[end] is not None: 
            path.append(parent[end])
            end = parent[end]
        path.reverse() #reverse path to get start to end
    return path, time, num_visited
    #new heuristic list will be straight line div max speed limit (100km/h = 27.8m/s)
    #raise NotImplementedError("To be implemented")
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
