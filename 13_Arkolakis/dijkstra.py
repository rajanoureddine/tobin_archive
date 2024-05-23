import numpy as np

class Graph:
    def __init__(self, vertices, weights = 1):
        self.weights = weights
        self.V = vertices  # No. of vertices
        self.graph = []
        self.dist = []

        # Define path or previous 
        if self.weights > 1:
            self.path = [{"path": None, "weights": []}] * self.V
            self.path_weights = [None] * self.V
        elif self.weights == 1:
            self.prev = [None] * self.V

        # Initialize constraints
        self.constraints = {}
        for i in range(1, self.weights):
            self.constraints[i] = []
 
    # function to add an edge to graph
    def addEdge(self, u, v, w):
        if (not type(w) == list) and self.weights > 1:
            raise ValueError(f"You must provide {self.weights} weights")
        elif type(w) == list and len(w) != self.weights:
            raise ValueError(f"You must provide {self.weights} weights")
        else:
            self.graph.append([u, v, w])
    
    def addConstraint(self, weight_index, max):
        if weight_index > self.weights:
            raise ValueError("There are only {self.weights} weights")
        else:
            self.constraints[weight_index] = max
        for key, value in self.constraints.items():
            print(f"Constraint {key}: {value}")

    
    # Function to get the path to a node
    def getPath(self, node, src, path = None):
        if not path:
            path = [node]
        if node == src:
            return path[::-1] # reverse it 
        else:
            try:
                if type(self.prev[node]) != list:
                    path.append(self.prev[node])
                    return self.getPath(self.prev[node], src, path)
                else:
                    return [self.getPath(self.prev[node][i], src, path + [self.prev[node][i]]) for i in range(len(self.prev[node]))]

            except Exception as e:
                return "No path"

    # utility function used to print the solution
    def printArr(self, src, dest=None):
        print("Vertex Distance from Source, and Path")
        if dest:
            path = self.getPath(dest, src)
            print("{0}\t{1}\t\t{2}".format(dest, self.dist[dest], path))

        if not dest:
            for i in range(self.V):
                if self.dist[i] != float("Inf"):
                    path = self.getPath(i, src)
                    print("{0}\t{1}\t\t{2}".format(i, self.dist[i], path))
    
    # utility function used to print the path
    def printPaths(self, src):
        for i in range(self.V):
            print(f"Path to {i}: {self.getPath(i, src)}")
 
    def Dijkstra(self, src, dest, print = True):
        output = False

        self.dist = [float("Inf")] * self.V
        self.dist[src] = 0

        A = []
        B = list(np.arange(self.V))

        while len(B) > 0:
            # Node in B with minimum distance
            distances_b = [self.dist[i] for i in B]
            u = B[np.argmin(distances_b)]

            # B = B \ {u}
            B.remove(u)

            # A = A + u
            A.append(u)

            for u2, v, w in self.graph:
                if ((u2 == u) and v in B): # Check the neighbours of u only
                    dsuv = self.dist[u] + w
                    if v == dest:
                        output = True
                        self.dist[v] = dsuv
                        self.prev[v] = u
                        if print:
                             self.printArr(src, dest)
                        return output
                    if dsuv < self.dist[v]:
                        self.dist[v] = dsuv
                        self.prev[v] = u
                    elif dsuv == self.dist[v]:
                        if self.prev[v] is None:
                            self.prev[v] = u
                        # elif type(self.prev[v]) != list:
                        #     self.prev[v] = sorted([self.prev[v], u])
                        # else:
                        #     self.prev[v] = sorted(self.prev[v]+ [u])
        if print:
            self.printArr(src, dest)

        return output
    
    def reset(self):
        self.dist = []

        # Define path or previous 
        if self.weights > 1:
            self.path = [None] * self.V
            self.path_weights = [None] * self.V
        
        elif self.weights == 1:
            self.prev = [None] * self.V



if __name__ == '__main__':
    graph_size = 20
    graph = np.zeros([graph_size, graph_size])
    for i in range(graph_size):
        for j in range(graph_size):
            graph[i][j] = np.random.choice([0, 1], p=[0.6, 0.4])
    graph_weights = np.random.randint(1, 8, (graph_size, graph_size))
    g = Graph(graph_size)
    g_e = GraphExtended(graph_size, 1, np.array([np.infty]))
    for i in range(graph_size):
        for j in range(graph_size):
            if graph[i][j] != 0:
                g.addEdge(i, j, graph_weights[i][j])
                g_e.addEdge(i, j, graph_weights[i][j])
    #g.Dijkstra(0)
    #print(g.prev)
    #g.reset()
    g.BellmanFord(0, True)
    g_e.BellmanExtended(0, 5)
    # print(g_e.path[5][0].path)
   #  print(graph)