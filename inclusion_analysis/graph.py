class Graph(object):

    def __init__(self):
        self.__vertice = {}
        self.__index = 0

    def connect(self, from_vertex, to_vertex):
        """
        sets a one-direction relation between vertice. from_vertex -> to_vertex
        :param from_vertex:
        :param to_vertex:
        :return: None
        """
        if not self.__vertice.has_key(from_vertex):
            self.add_vertex(from_vertex)
        if not self.__vertice.has_key(to_vertex):
            self.add_vertex(to_vertex)
        self.__vertice[from_vertex].append(to_vertex)

    def is_adjacent(self, from_vertex, to_vertex):
        return to_vertex in self.__vertice[from_vertex]

    def add_vertex(self, data):
        """
        add a informational vertex to the graph with
        :param data: an information contained by vertex
        :return: None
        """
        self.__vertice[data] = []
        self.__index += 1

    def __len__(self):
        return self.__index

    def has_vertex(self, name):
        """
        checks if graph contains a vertex with particular information
        :param name: an info we're looking for
        :return: Boolean
        """
        return self.__vertice.has_key(name)

    def __topology_sort(self, vertex_index, postorder, marked):
        """
        return an ordered vertice. Implementation function
        Caution: before using it, check for cycles in graph.
        :param vertex_index: vertex to start with
        :param postorder: formed order list
        :param marked: vertice already visited
        :return: None
        """
        if not marked[vertex_index]:
            marked[vertex_index] = True
            for child_index in self.__vertice[vertex_index].connected():
                    self.__topology_sort(child_index, postorder, marked)
            postorder.append(vertex_index)

    def __dfs(self, vertex, adjacent, marked, cycles):
        """
        plain depth first search implementation function.
        :param vertex: currently processed vertex
        :param adjacent: adjacency dictionary {to_vertex: from_vertex}
        :param marked: visited vertice
        :param cycles: cycles detected
        :return: None
        """
        marked[vertex] = True
        for child in self.__vertice[vertex]:
            if not marked[child]:
                marked[child] = True
                adjacent[child] = vertex
                self.__dfs(child, adjacent, marked, cycles)
            else:
                cycle = []
                current_adjacent = vertex
                while child != current_adjacent:
                    cycle.append(current_adjacent)
                    current_adjacent = adjacent[current_adjacent]
                cycle.append(child)
                cycles.append(cycle)

    def cycle_detect(self, root_vertex):
        """
        cycle detection function
        :param self:
        :param root_vertex:
        :return: a list of pairs that combine a cycle detected and a path to a vertex cycle starts with
        """
        marked = {k: False for k in self.__vertice.keys()}
        cycles = []
        adjacent = {k: None for k in self.__vertice.keys()}
        cycles = []
        active_vetice = []

        def prior(vertex, adjacent, *unused):
            if vertex in active_vetice:
                cycle = []
                current_adjacent = adjacent[vertex]
                while vertex != current_adjacent:
                    cycle.append(current_adjacent)
                    current_adjacent = adjacent[current_adjacent]
                cycle.append(vertex)
                cycles.append(cycle)
            else:
                active_vetice.append(vertex)

        def post(vertex, *unused):
            try:
                i = active_vetice.index(vertex)
                del active_vetice[i]
            except ValueError:  # if a cycle detected, one vertex is visited twice
                pass

        self.__dfs_modifiable(root_vertex, adjacent, marked, prior, post)

        passes_to_cycles = []
        cycles_start_vertice = [cycle[-1] for cycle in cycles]

        for start_vertice in cycles_start_vertice:
            path = []
            while start_vertice != root_vertex:
                path.append(start_vertice)
                start_vertice = adjacent[start_vertice]
            path.append(start_vertice)
            path.reverse()
            passes_to_cycles.append(path)

        return zip(cycles, passes_to_cycles)

    def __dfs_modifiable(self, vertex, adjacent, marked, prefix_operation=None, postfix_operation=None):
        """
        Depth first search implementation function. with user-defined pre/post processing function
        :param vertex: currently processed vertex
        :param adjacent: adjacency dictionary {to_vertex: from_vertex}
        :param marked: visited vertice
        :param prefix_operation: a function called before processing a vertex
        :param postfix_operation: a function called after processing a vertex
        :return: None
        """
        if prefix_operation is not None:
            prefix_operation(vertex, adjacent, marked)
        if not marked[vertex]:
            marked[vertex] = True
            for child in self.__vertice[vertex]:
                adjacent[child] = vertex
                self.__dfs_modifiable(child, adjacent, marked, prefix_operation, postfix_operation)
                adjacent[child] = vertex  # to prevent cycling when looking for a path. It sets a path from current vertex to root
        if postfix_operation is not None:
            postfix_operation(vertex, adjacent, marked)

    def topology_sort(self, root_vertex):
        """
        return an ordered vertice
        :param self:
        :param root_vertex: a vertex to start
        :return: ordered vertive
        """
        postorder = []
        marked = [False for _ in range(0, len(self))]
        for i in range(0, len(self)):
            self.__topology_sort(i, postorder, marked)
        postorder.reverse()
        return postorder

    def reversed(self):
        new_graph = Graph()
        for from_vertex, adjacent in self.__vertice.items():
            [new_graph.connect(to_vertex, from_vertex) for to_vertex in adjacent]
        return new_graph

"""
    def strong_connection(self):
        marked = [False for _ in range(0, len(self))]
        self.__reverse()

        reverse_postorder = self.topology_sort()

        marked = [False for _ in range(0, len(self))]
        self.__reverse()
        groups = []
        for i in reverse_postorder:
            postorder = []
            self.__topology_sort(i, postorder, marked)
            groups.append(postorder)
        return groups
"""
