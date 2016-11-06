import unittest

from inclusion_analysis.graph import Graph


class graph_test(unittest.TestCase):

    def test_cycle_detect_explicit_cycle(self):
        target = Graph()

        target.connect("header0", "header1")
        target.connect("header1", "header2")
        target.connect("header2", "header0")
        target.connect("header2", "header3")

        cycles = target.cycle_detect("header0")
        expected = ["header2", "header1", "header0"]

        self.assertEqual(len(cycles), 1)
        self.assertEqual(cycles[0][0], expected)

    def test_reverse(self):
        target = Graph()
        target.connect("header0", "header1")
        target.connect("header1", "header2")
        target.connect("header2", "header0")
        reversed_graph = target.reversed()

        reversed_graph.is_adjacent("header1", "header0")
        reversed_graph.is_adjacent("header2", "header1")
        reversed_graph.is_adjacent("header0", "header2")


if __name__ == '__main__':
    unittest.main()
