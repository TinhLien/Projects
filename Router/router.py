class Graph:
    def __init__(self):
        self.edges = {}     # edges will look like {"a": {"b": 7, "c": 9}, "b": {"f": 5}}
        self.nodes = set()  # set of nodes will look like ("a", "b", "c"... etc)

    def add_edge(self, node_one, node_two, weight):
        # creating set of nodes used
        if node_one not in self.nodes:
            self.nodes.add(node_one)
        if node_two not in self.nodes:
            self.nodes.add(node_two)

        # creating nested dictionary of all edges
        if node_one not in self.edges:
            self.edges[node_one] = {node_one: 0, node_two: weight}
        else:
            for node_id, node_info in self.edges.items():
                if node_id == node_one:
                    self.edges[node_id][node_two] = weight

class Router:
    def __init__(self, start, graph):
        self.start = start
        self.graph = graph

    @staticmethod
    def generate_path(parents, start, end):
        try:    # keep going even if there is no path
            path = [end]
            while True:
                key = parents[path[0]]
                path.insert(0, key)
                if key == start:
                    break
            return path
        except KeyError:    # if a connection was cut off by remove_router()
            return ["Path", "Removed"]

    def dijkstra(self, router_name, edges):
        unvisited = {n: float("inf") for n in self.graph.nodes}
        unvisited[self.start] = 0  # set start vertex to 0
        visited = {}  # list of all visited nodes
        parents = {}  # predecessors
        while unvisited:
            min_vertex = min(unvisited, key=unvisited.get)  # get smallest distance
            for neighbour, _ in edges.get(min_vertex, {}).items():
                if neighbour in visited:
                    continue
                new_distance = unvisited[min_vertex] + edges[min_vertex].get(neighbour, float("inf"))
                if new_distance < unvisited[neighbour]:
                    unvisited[neighbour] = new_distance
                    parents[neighbour] = min_vertex
            visited[min_vertex] = unvisited[min_vertex]
            unvisited.pop(min_vertex)
            if min_vertex == router_name:
                break
        
        path = self.generate_path(parents, self.start, router_name)

        return path, visited[router_name]
    
    def get_path(self, router_name):
        # getting the path and cost using dijkstras algorithm
        path, cost = self.dijkstra(router_name, self.graph.edges)
        return print("Start: {}\nEnd: {}\nPath: {}\nCost: {}".format(self.start, router_name, " -> ".join(path), cost))

    def print_routing_table(self):
        print("{:>6}{:>3}{:>5}{:>20}".format("from", "to", "cost", "path"))
        index = 0
        for _, node in enumerate(self.graph.nodes):
            if node != self.start:
                path, cost = self.dijkstra(node, self.graph.edges)
                print("{}{:>5}{:>3}{:>5}{:>20}".format(index, self.start, node, cost," -> ".join(path)))
                index += 1

    def remove_router(self, router_name):
        self.graph.nodes.remove(router_name)
        del self.graph.edges[router_name]
        for node_id, node_info in self.graph.edges.items():
            try:
                for info in node_info:
                    if info == router_name:
                        del self.graph.edges[node_id][info]
            except RuntimeError:
                continue

        print("{:>6}{:>3}{:>5}{:>20}".format("from", "to", "cost", "path"))
        for id, node in enumerate(self.graph.nodes):
            if node != self.start:
                path, cost = self.dijkstra(node, self.graph.edges)
                print("{}{:>5}{:>3}{:>5}{:>20}".format(id, self.start, node, cost," -> ".join(path)))


def main():
    graph = Graph()

    graph.add_edge("a", "b", 7)
    graph.add_edge("a", "c", 9)
    graph.add_edge("a", "f", 14)
    graph.add_edge("b", "c", 10)
    graph.add_edge("b", "d", 15)
    graph.add_edge("c", "d", 11)
    graph.add_edge("c", "f", 2)
    graph.add_edge("c", "a", 9)
    graph.add_edge("d", "e", 6)
    graph.add_edge("e", "f", 9)

    router = Router("a", graph)
    router_two = Router("b", graph)
    print()
    print("-----Routing Table For Router One!-----\n")
    router.print_routing_table()
    print()
    print("-----Routing Table For Router Two!-----\n")
    router_two.print_routing_table()
    print()
    print("-----Removed 'c' From Edges------\n")
    router.remove_router("c")
    print()
    print("-----New Routing Table For Router Two-----\n")
    router_two.print_routing_table()

main()

# https://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python was used to help with Router.dijkstra() and Router.generate_path()