class Graph(object):
    """This class describes directed graph

    vertices represented by plain numbers
    directed edges are start with vertex which is index of __vertices
    vertex the edge goes to is a value within list
    so, __vertices is "list < list <int> >"
    vertex is __vertices[*vertex_from*] = list of vertices of adjacent vertices
    """

    def __init__(self):
        self.__vertices = {}

    def connect(self, from_vertex, to_vertex):
        """
        sets a one-direction relation (directed edge) between vertices.
        from_vertex -> to_vertex

        :param from_vertex: index of vertex that edge goes from
        :param to_vertex: index of vertex that edge goes to
        :type from_vertex: int
        :type to_vertex: int
        :return: None
        """
        if not self.__vertices.has_key(from_vertex):
            self.add_vertex(from_vertex)

        if not self.__vertices.has_key(to_vertex):
            self.add_vertex(to_vertex)

        self.__vertices[from_vertex].append(to_vertex)

    def is_adjacent(self, from_vertex, to_vertex):
        """ checks if there is an edge between vertices """
        return to_vertex in self.__vertices[from_vertex]

    def get_connected(self, from_vertex):
        """
        get all vertices that are connected directly to the particular one

        :param from_vertex: particular vertex
        :rtype: list<int>
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


def dfs_impl(graph, cur_vertex, path_marked, marked, cycles, cur_path):
    """
    plain depth first search implementation function.

    :param cur_vertex: currently processed vertex
    :param path_marked: list of booleans that defines whether a vertex is
        a part of path that connects current vertex and vertex dfs algo started
        with
    :param marked: visited vertices
    :param cycles: cycles detected
    :param cur_path: path to particular vertex from starting point
    :rtype cur_vertex: int
    :rtype path_marked: list<int>
    :rtype marked: list<int>
    :rtype cycles: list<list<int> >
    :rtype cur_path: list <int>
    :returns: if cur_vertex is a part of cycle
    :rtype: boolean
    """
    result = False

    cur_path.append(cur_vertex)

    for next_vertex in graph.get_connected(cur_vertex):
        if (path_marked[next_vertex]):  # path detected, the first index in list
            cycles.append(([next_vertex],[]))
            path_marked[next_vertex] = False
            result = True
        if not marked[next_vertex]:

            path_marked[next_vertex] = True
            marked[next_vertex] = True

            if dfs_impl(graph, next_vertex, path_marked, marked, cycles, cur_path):
                # the function is within cycle right now!
                cycle = cycles[-1][0]
                if cycle[0] != next_vertex:
                    # append it!
                    path_marked[next_vertex] = False
                    cycle.append(next_vertex)
                    result = True
                    break
                else:  # cucle[0] == next_vertex
                    cycles[-1][1].extend(cur_path)

            path_marked[next_vertex] = False

    cur_path.pop()

    # for path in cycles:
    #     path.append(cur_vertex)

    return result


def cycle_detect(graph, root_vertex):
    """
    cycle detection function

    :param graph: processed graph
    :param root_vertex: a vertex to start processing with
    :type graph: graph
    :type root_vertex: root_vertex
    :return: a list of pairs that combine a cycle detected and a
        path to a vertex cycle starts with
    :rtype: list<(list, list)>

    """
    path_marked = [False] * len(graph)
    marked = [False] * len(graph)
    cycles = []

    dfs_impl(graph, root_vertex, path_marked, marked, cycles, [])

    return cycles


class FileGraph(object):
    """Class that reprecent file inclusion

    each vertex is a file, each edge describes one header that is included by
    another
    """

    def __init__(self):
        """
        __graph is a graph of indexes, each index represents file
        __name_to_index if a dict which key is filename and its value is index
        __index_name if a dict which key is index and its value is filename
        """
        self.__graph = Graph()
        self.__name_to_index = {}
        self.__index_name = {}

    def get_name_by_index(self, index):
        """ returns filename by its index """
        return self.__index_name[index]

    def get_index_by_name(self, name):
        """ returns file's index by its name """
        return self.__name_to_index[name]

    def connect(self, from_vertex, to_vertex):
        """
        sets a one-direction relation between vertices. from_vertex -> to_vertex

        :param from_vertex: filename that contains inclusion
        :param to_vertex: included filename
        :type from_vertex: str
        :type to_vertex: str
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
        """ returns whether to_vertex is adjacent to from_vertex """
        from_vertex = self.get_index_by_name(from_vertex)
        to_vertex = self.get_index_by_name(to_vertex)
        return self.__graph.is_adjacent(from_vertex, to_vertex)

    def get_connected(self, from_vertex):
        """
        get all vertices that are connected directly to the particular one

        :param from_vertex: particular vertex
        :type from_vertex: str
        :returns: all adjacent vertices
        :rtype: list <int>
        """
        if isinstance(from_vertex, int):
            return self.__vertices[from_vertex]

    def add_vertex(self, data):
        """
        add a informational vertex to the graph with

        :param data: an information contained by vertex
        :type data: str
        :rtype: None
        """
        self.__name_to_index[data] = len(self)
        self.__index_name[len(self)] = data
        self.__graph.add_vertex(len(self))

    def __len__(self):
        return len(self.__graph)

    def has_vertex(self, name):
        """
        checks if graph contains a vertex with particular information

        :param name: an info we are looking for
        :rtype name: str
        :return: if the graph contains particular filename
        :rtype: Boolean
        """
        return self.__vertices.has_key(name)

    def cycle_detect(self, root_vertex):
        """
        detects all cycles of the graph

        :param root_vertex: the vertex it start graph traverse
        :rtype root_vertex: str
        :return: a list of pairs that combine a cycle detected and a path to a vertex cycle starts with
        """
        root_vertex = self.get_index_by_name(root_vertex)
        cycles = cycle_detect(self.__graph, root_vertex)
        named_cycles = []
        for cycle in cycles:
            named_cycles.append(
                ([self.get_name_by_index(index) for index in cycle[0]]
                , [self.get_name_by_index(index) for index in cycle[1]])
            )

        return named_cycles

    def __str__(self):
        result = ''
        for index, filename in self.__index_name.iteritems():
            result += filename + ': '
            for include in self.__graph.get_connected(index):
                result += self.get_name_by_index(include) + ', '
            result += "\n"
        return result
