import copy

class Dijkstra(object):
    def __init__(self, start: str, end: str, dist: str) -> None:
        self.path = list()
        self.city_eval= dict()
        self.dist_eval= dict()
        self.visited = list()

        self.__null(dist)
        self.__dijkstra(start, end, dist)

    # private method:
    #   input: distance
    #   return 
    # Note: For all vertices the edge evaluation(dist_eval) = +infinity, and the state(city_eval) = undefined      
    def __null(self, dist: str) -> None:
        dist_eval = self.dist_eval
        city_eval = self.city_eval

        for i in dist.keys():
            dist_eval[i] = float('Inf')
            city_eval[i] = None
    
    # private method:
    #   input: distance evaluation, visited
    #   return minimal distantion in keys
    # Note: Select the open vertex whose edge length is the smallest.
    def __take_node(self, dist_eval: dict, visited: list) -> str:
        # deep copy vs shallow copy 
        dist_eval_t = copy.deepcopy(dist_eval)

        for node in visited:
            del dist_eval_t[node]

        return min(dist_eval_t, key = lambda k: dist_eval_t[k])
    
    # private method:
    #   input: start_node, end_node, all records 
    #   return shortest path
    # Note: Add nodes from memory to the resulting shortest path, until the end node equals its true value and thus the starting node
    def __shortest_path(self, start_node: str, end_node: str, records: dict) -> list:
        shortest_path = [end_node]

        while True:
            shortest_path.append(records.get(end_node))
            end_node = records.get(end_node)

            if end_node == start_node:
                break
        
        """
        for i in range(len(shortest_path),0,-1):
            if i == 1:
                pass
            else:
                print(shortest_path[i-1] + " -> " + shortest_path[i-2])
        """

        # Function in reverse order
        return shortest_path[::-1]
    
    # private method:
    #   input: start_node, end_node, distances
    #   return 
    # Note: for the first calculation, set edge(dist_eval) = 0, and state(city_eval) = starting city. 
    # if the start node is equal to the end node the calculation is terminated.
    def __dijkstra(self, start: str, end: str, dist: dict) -> None:
        dist_eval = self.dist_eval
        city_eval = self.city_eval
        visited = self.visited

        dist_eval[start] = 0
        city_eval[start] = start

        """
        if start == end:
            print('You stand in one place!')
        """

        while True:   
            node = self.__take_node(dist_eval, visited)

            # for all the followers of w from the top in
            for i in dist[node].keys():
                if i in visited:
                    continue
                
                # if the edge of the successor is larger than the edge of its predecessor between the wrinkles (w,v) store the edge
                if dist_eval[i] > dist_eval[node] + dist[node].get(i):
                    dist_eval[i] = dist_eval[node] + dist[node].get(i)
                    city_eval[i] = node
            
            # determination of visited nodes
            visited.append(node)

            if end in visited:
                break
        
        self.path = self.__shortest_path(start, end, city_eval)

        # print('It takes about {} min'.format(dist_eval.get(end)))