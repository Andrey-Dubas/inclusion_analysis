class Graph(object):

    def __init__(self):
        self.__vertices = {}

    def connect(self, from_vertex, to_vertex):
        """
        sets a one-direction relation between vertices. from_vertex -> to_vertex
        :param from_vertex:
        :param to_vertex:
        :return: None
        """
        if not self.__vertices.has_key(from_vertex):
            self.add_vertex(from_vertex)

        if not self.__vertices.has_key(to_vertex):
            self.add_vertex(to_vertex)

        self.__vertices[from_vertex].append(to_vertex)

    def is_adjacent(self, from_vertex, to_vertex):
        return to_vertex in self.__vertices[from_vertex]

    def get_connected(self, from_vertex):
        """
        get all vertices that are connected directly to the particular one
        :param from_vertex: particular vertex
        :return: list
        """
        if isinstance(from_vertex, int):
            return self.__vertices[from_vertex]

    def add_vertex(self, index):
        """
        add a informational vertex to the graph with
        :param data: an information contained by vertex
        :return: None
        """
        self.__vertices[index] = []

    def __len__(self):
        return len(self.__vertices)

    def has_vertex(self, index):
        """
        checks if graph contains a vertex with particular information
        :param name: an info we're looking for
        :return: Boolean
        """
        return self.__vertices.has_key(index)


def dfs_impl(graph, cur_vertex, path_marked, marked, cycles):
    """
    plain depth first search implementation function.
    :param vertex: currently processed vertex
    :param adjacent: adjacency dictionary {to_vertex: from_vertex}
    :param marked: visited vertices
    :param cycles: cycles detected
    :return: boolean
    """
    result = False

    for next_vertex in graph.get_connected(cur_vertex):
        if (path_marked[next_vertex]):  # path detected, the first index in list
            cycles.append([next_vertex])
            path_marked[next_vertex] = False
            result = True
        if not marked[next_vertex]:
            path_marked[next_vertex] = True
            marked[next_vertex] = True

            if dfs_impl(graph, next_vertex, path_marked, marked, cycles):
                # the function is within cycle right now!
                cycle = cycles[-1]
                if cycle[0] != next_vertex:
                    # append it!
                    path_marked[next_vertex] = False
                    cycle.append(next_vertex)
                    result = True
                    break

            path_marked[next_vertex] = False

    # for path in cycles:
    #     path.append(cur_vertex)

    return result


def cycle_detect(graph, root_vertex):
    """
    cycle detection function
    :param self:
    :param root_vertex:
    :return: a list of pairs that combine a cycle detected and a path to a vertex cycle starts with
    """
    print("")

    path_marked = [False] * len(graph)
    marked = [False] * len(graph)
    cycles = []

    dfs_impl(graph, root_vertex, path_marked, marked, cycles)

    print("")
    return cycles


class FileGraph(object):

    def __init__(self):
        self.__graph = Graph()
        self.__name_to_index = {}
        self.__index_name = {}

    def get_name_by_index(self, index):
        return self.__index_name[index]

    def get_index_by_name(self, name):
        return self.__name_to_index[name]

    def connect(self, from_vertex, to_vertex):
        """
        sets a one-direction relation between vertices. from_vertex -> to_vertex
        :param from_vertex:
        :param to_vertex:
        :return: None
        """
        if isinstance(from_vertex, str):
            if not self.__name_to_index.has_key(from_vertex):
                self.add_vertex(from_vertex)
            from_vertex_index = self.__name_to_index[from_vertex]
        else:
            raise ValueError("vertices must be names of files")

        if isinstance(to_vertex, str):
            if not self.__name_to_index.has_key(to_vertex):
                self.add_vertex(to_vertex)
            to_vertex_index = self.__name_to_index[to_vertex]
        else:
            raise ValueError("vertices must be names of files")

        self.__graph.connect(from_vertex_index, to_vertex_index)

    def is_adjacent(self, from_vertex, to_vertex):
        from_vertex = self.get_index_by_name(from_vertex)
        to_vertex = self.get_index_by_name(to_vertex)
        return self.__graph.is_adjacent(from_vertex, to_vertex)

    def get_connected(self, from_vertex):
        """
        get all vertices that are connected directly to the particular one
        :param from_vertex: particular vertex
        :return: list
        """
        if isinstance(from_vertex, int):
            return self.__vertices[from_vertex]

    def add_vertex(self, data):
        """
        add a informational vertex to the graph with
        :param data: an information contained by vertex
        :return: None
        """
        self.__name_to_index[data] = len(self)
        self.__index_name[len(self)] = data
        self.__graph.add_vertex(len(self))

    def __len__(self):
        return len(self.__graph)

    def has_vertex(self, name):
        """
        checks if graph contains a vertex with particular information
        :param name: an info we're looking for
        :return: Boolean
        """
        return self.__vertices.has_key(name)

    def cycle_detect(self, root_vertex):
        """
        cycle detection function
        :param self:
        :param root_vertex:
        :return: a list of pairs that combine a cycle detected and a path to a vertex cycle starts with
        """
        root_vertex = self.get_index_by_name(root_vertex)
        cycles = cycle_detect(self.__graph, root_vertex)
        named_cycles = []
        for cycle in cycles:
            named_cycles.append([self.get_name_by_index(index) for index in cycle])

        return named_cycles
