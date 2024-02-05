import csv
from queue import PriorityQueue
edgeFile = 'edges.csv'

def ucs(start, end):
    # Begin your code (Part 3)
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
            
    #ucs
    queue = PriorityQueue() #use priority queue to priority smallest distance 
    visited = []
    parent = {}
    distance = {}
    queue.put((0, start)) #(distance from start to node, node)
    distance[start] = 0 
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
                if next_node[0] not in visited or curr[0]+next_node[1] < distance[next_node[0]]:
                    queue.put((curr[0]+next_node[1], next_node[0])) 
                    #calculator start to next_node distance
                    distance[next_node[0]] = distance[curr[1]] + next_node[1]
                    parent[next_node[0]] = curr[1] #parent of next_node
                    if next_node[0] not in visited:
                        visited.append(next_node[0])
                
    #result
    path = [] #start to end
    dist = curr[0] #distance from start to end
    num_visited = len(visited)
    if path_found: #store path
        path.append(end) #end - start
        while parent[end] is not None: 
            path.append(parent[end])
            end = parent[end]
        path.reverse() #reverse path to get start to end
    return path, dist, num_visited
    # load edgeFile to get adjacency list (start_node: end_node, distance, speed limit)
    # use usc to find path, start to end smallest distance, number visited
    # queue will be priority smallest distance from start to node
    # get path from parent list 
    #raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902,1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
