import parser
import graph
import sys
from option_parser import OptionParser


def graph_completion_recursive_imp(header_inclusion_graph, existed_headers, current_file, parsed_headers):
    """
    forms an inclusion graph of all headers, contained in directory. Its root is a cpp file.
    Recursive. Implementation function. Use 'graph_completion_recursive' to generate a relation digraph
    :param header_inclusion_graph: the graph is being formed
    :param existed_headers: the headers contained in directory
    :param current_file: currently parsed for includes file
    :param parsed_headers: file that have been already parsed
    :return: None
    """
    current_file_headers = parser.find_included_headers(current_file)
    parsed_headers.append(current_file)
    for h in current_file_headers:
        if any(map(lambda x: h in x, existed_headers)):
            header_inclusion_graph.connect(current_file, h)
            if h not in parsed_headers:
                graph_completion_recursive_imp(header_inclusion_graph, existed_headers, h, parsed_headers)


def graph_completion_recursive(existed_headers, root_file):
    """
    forms an inclusion graph of all headers, contained in directory. Its root is a cpp file.
    Recursive. Implementation function. Use 'graph_completion_recursive' to generate a relation digraph
    :param existed_headers: the headers contained in directory
    :param root_file: a root inclusion file. The first file to be parsed for headers.
    :return: a digraph of headers
    """
    header_inclusion_graph = graph.Graph()
    graph_completion_recursive_imp(header_inclusion_graph, existed_headers, root_file, [])
    return header_inclusion_graph


def main():
    """
    program entry point
    :return: None
    """
    sys.argv = sys.argv[1:]
    option_parser = OptionParser()
    option_parser.add_option('-f', '--file', 0)
    option_parser.add_option('-d', '--directory', 1)
    option_parser.parse(sys.argv)
    root_file = option_parser['-f'].value
    directory = option_parser['-d'].value
    directory_headers = parser.find_project_headers(directory)
    header_inclusion_graph = graph_completion_recursive(directory_headers, root_file)

    cycles = header_inclusion_graph.cycle_detect(root_file)
    result = []
    for cycle, path in cycles:
        result.append("path: " + ' -> '.join(path) +
                      "\ncycle: " + ' -> '.join(cycle))
    print('\n'.join(result))

if __name__ == '__main__':
    main()




