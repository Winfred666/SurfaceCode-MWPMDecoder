import numpy as np

def list_insert(list,pair):
    insert_index=0
    len_list = len(list)
    while(insert_index<len_list and list[insert_index][0] < pair[0]):
        insert_index+=1
    list.insert(insert_index,pair)

def list_remove_index(list,index):
    for i in range(len(list)):
        if list[i][1] == index:
            list.pop(i)
            break

#matching_graph is a adjacent matrix
#syndrome is a 1D vector, 1 means defect, 0 means no defect
#use local_search_m as minimun degree of each defect node.
#the start node is a index, from 0 to sizeX*sizeY-1
def local_dijkstra(matching_graph,syndrome,local_search_m,start,end=None): 
    # Create a priority queue
    dist_from_start = np.full(len(matching_graph), 99999) # the distance from start to each node
    dist_from_start[start] = 0
    # need to record the path
    parents = np.full(len(matching_graph),-1)
    pq = []
    pq.append((0,start))

    found_defects = [] # the defects found by local dijkstra, decide the min degree of the start node
    while pq and len(found_defects) < local_search_m:
        #find minimun distance node
        current = pq.pop(0)[1]

        if syndrome[current] == 1: # find a defect node
            found_defects.append(current)
        
        for i in range(len(matching_graph)):
            if matching_graph[current][i] == 0 or matching_graph[current][i] == 99999: # not the neighbor
                continue
            if dist_from_start[current] + matching_graph[current][i] < dist_from_start[i]: # update the distance
                dist_from_start[i] = dist_from_start[current] + matching_graph[current][i]
                parents[i] = current
                if(dist_from_start[i] == 99999): #never visit
                    list_insert(pq,(dist_from_start[i],i))
                else: # visit, need to decrease value, here should be decrease key.
                    list_remove_index(pq,i)
                    list_insert(pq,(dist_from_start[i],i))
    # get the path from start to end
    if(end!=None):
        path = [end]
        curnode = end
        while(parents[curnode]!=-1):
            curnode = parents[curnode]
            path.append(curnode)
        return path
    return found_defects,dist_from_start

