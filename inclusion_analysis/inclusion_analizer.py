import parser
import graph
import sys
import os
from option_parser import OptionParser


def graph_completion_recursive_imp(header_inclusion_graph, include_directories, current_file, parsed_headers):
    """
    forms an inclusion graph of all headers, contained in directory. Its root is a cpp file.
    Recursive. Implementation function. Use 'graph_completion_recursive' to generate a relation digraph
    :param header_inclusion_graph: the graph is being formed
    :param include_directories: list of include directories
    :param current_file: currently parsed for includes file
    :param parsed_headers: file that have been already parsed
    :return: None
    """
    current_file_headers = parser.find_included_headers(current_file, include_directories)
    parsed_headers.append(current_file)
    for included_header in current_file_headers:
            full_name = parser.find_full_header_name(included_header, include_directories)
            header_inclusion_graph.connect(current_file, full_name)
            if full_name not in parsed_headers:
                graph_completion_recursive_imp(header_inclusion_graph, include_directories, full_name, parsed_headers)


def graph_completion_recursive(include_directories, root_file):
    """
    forms an inclusion graph of all headers, contained in directory. Its root is a cpp file.
    Recursive. Implementation function. Use 'graph_completion_recursive' to generate a relation digraph
    :param root_file: a root inclusion file. The first file to be parsed for headers.
    :return: a digraph of headers
    """
    include_directories.append(os.getcwd())
    header_inclusion_graph = graph.FileGraph()
    graph_completion_recursive_imp(header_inclusion_graph, include_directories, root_file, [])
    return header_inclusion_graph


def main():
    """
    program entry point
    :return: None
    """
    sys.argv = sys.argv[1:]
    option_parser = OptionParser()
    option_parser.add_option('-f', '--file', 0)
    option_parser.add_option('-i', '--include_path', 1)
    option_parser.add_option('-h', '--help')
    option_parser.parse(sys.argv)
    root_files = option_parser['-f'].get_value()
    include_directories = option_parser['-i'].get_value()
    if option_parser.has_key('-h'):
        print("""-f, --file - set up .cpp file as starting point for analyzer
                   example:
                   python inclusion_analizer.py -f <dir>/<filename>.cpp
                 -i, --include_path:
                   add include path""")
    else:
        if len(root_files) == 0:
            print("no translation unit was specified")
        else:
            root_file = root_files[0]
            header_inclusion_graph = graph_completion_recursive(include_directories, root_file)
            print(header_inclusion_graph)
            cycles = header_inclusion_graph.cycle_detect(root_file)
            result = []

            for cycle in cycles:
                path = []
                result.append("path: " + ' -> '.join(path) +
                            "\ncycle: " + ' -> '.join(cycle))
            print('\n'.join(result))

if __name__ == '__main__':
    main()
