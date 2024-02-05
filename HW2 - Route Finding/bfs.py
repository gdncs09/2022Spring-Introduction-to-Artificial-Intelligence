import csv
from queue import Queue
edgeFile = 'edges.csv'

def bfs(start, end):
    # Begin your code (Part 1) 
    #load edgeFile to adjacency list
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
    #bfs
    queue = Queue()
    visited = []
    parent = {}
    queue.put((0, start)) #(distance from start to node, node)
    visited.append(start)
    parent[start] = None
    path_found = False
    while not queue.empty():
        curr = queue.get() #curr[0]:distance curr[1]:current node
        if curr[1] == end: #current node is end
            path_found = True
            break
        if curr[1] in adj_list: #current node exist
            for next_node in adj_list[curr[1]]: #next_node[0]:node #next_node[1]:distance
                if next_node[0] not in visited: 
                    queue.put((curr[0]+next_node[1], next_node[0])) 
                    #put distance from start to next_node, next_node to queue
                    parent[next_node[0]] = curr[1] #parent of next_node
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
    # use bfs to find path, start to end distance, number visited
    # get path from parent list
    #raise NotImplementedError("To be implemented")
    # End your code (Part 1)

if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
