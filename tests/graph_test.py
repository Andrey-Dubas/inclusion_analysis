import unittest

from inclusion_analysis.graph import FileGraph
from inclusion_analysis.graph import Graph
from inclusion_analysis.graph import cycle_detect

def list_rotate(l):
    item = l.pop()
    l.insert(0, item)

def assertSameList(l1, l2):
    for i in range(0, len(l1)):
        list_rotate(l1)
        if l1 == l2:
            return True
    return False

class GraphTest(unittest.TestCase):

    def test_cycle_detect_explicit_cycle(self):
        target = Graph()

        # 0
        target.connect(0, 1)
        target.connect(0, 7)
        target.connect(0, 4)

        # 1
        target.connect(1, 7)
        target.connect(1, 2)
        target.connect(1, 3)
        # 2
        target.connect(2, 3)
        target.connect(2, 5)
        # 3
        target.connect(4, 7)
        target.connect(4, 5)
        target.connect(4, 6)
        # 5
        target.connect(5, 2)
        target.connect(5, 6)
        # 6
        target.connect(7, 2)
        target.connect(7, 5)

        # here is cycle forms
        target.connect(3, 7)

        cycles = cycle_detect(target, 0)
        expected = [3, 2, 7]

        print(cycles)
        self.assertEqual(len(cycles), 1)
        assertSameList(cycles[0], expected)


class FileGraphTest(unittest.TestCase):

    def test_cycle_detect_explicit_cycle(self):
        target = FileGraph()

        target.connect("header0", "header1")
        target.connect("header1", "header2")
        target.connect("header2", "header0")
        target.connect("header2", "header3")

        cycles = target.cycle_detect("header0")
        expected = ["header2", "header1", "header0"]

        self.assertEqual(len(cycles), 1)
        assertSameList(cycles[0], expected)

"""
    def test_reverse(self):
        target = Graph()
        target.connect("header0", "header1")
        target.connect("header1", "header2")
        target.connect("header2", "header0")
        reversed_graph = target.reversed()

        reversed_graph.is_adjacent("header1", "header0")
        reversed_graph.is_adjacent("header2", "header1")
        reversed_graph.is_adjacent("header0", "header2")

    def test_strong_connection(self):
        target = Graph()

        target.connect(0, 1)
        target.connect(0, 5)

        target.connect(2, 0)
        target.connect(2, 3)

        target.connect(3, 2)
        target.connect(3, 5)

        target.connect(4, 2)
        target.connect(4, 3)

        target.connect(5, 4)



        target.connect(6, 8)
        target.connect(6, 7)
        target.connect(6, 0)
        target.connect(6, 4)

        target.connect(8, 6)



        target.connect(7, 6)
        target.connect(7, 9)



        target.connect(9, 10)
        target.connect(9, 11)

        target.connect(10, 12)

        target.connect(11, 4)
        target.connect(11, 12)

        target.connect(12, 9)

        groups = target.strong_connection()
        expected = [[1], [0, 2, 3, 4, 5], [6, 8], [7], [9, 10, 11, 12]]
        def list_comparator(list1, list2):
            return reduce(lambda v1, v2: v1 or v2, map(lambda v: v in list2, list1))
        for expected_group in expected:
            if any(map(built_group)):

"""



if __name__ == '__main__':
    unittest.main()
