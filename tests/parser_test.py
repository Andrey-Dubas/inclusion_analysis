from inclusion_analysis import parser
import unittest
import os
from mocker import Mocker


def os_walk_mock(path, followlinks):
    return [
        ('/dir1/', [], ['garbage', '.settingsFile', 'text_file.txt', 'header.h'])
    ]


class parser_test(unittest.TestCase):

    def test_find_project_headers(self):
        with Mocker(mocked_function=os.walk, mock=os_walk_mock):
            result = parser.find_project_headers('/some_dir')
            self.assertEqual(result, map(lambda x: '/dir1/' + x, ['header.h']))

    def test_get_lexems(self):
        input_lines = [
            "#include <iostream>",
            "#include< stdlib.h >  // bla-bla",
            "// #include <header.hpp>",
            "/*#include <h.h>*/ #include   <real_header.h>"
        ]
        produced_output = map(parser._get_lexems, input_lines)
        expected_output = [
            ['#', 'include', '<', 'iostream', '>'],
            ['#', 'include', '<', 'stdlib.h', '>', '//', 'bla-bla'],
            ['//', '#', 'include', '<', 'header.hpp', '>'],
            ['/*', '#', 'include', '<', 'h.h', '>', '*/', '#', 'include', '<', 'real_header.h', '>']
        ]
        self.assertEqual(produced_output, expected_output)

    def test_obtain_header(self):
        input_lines = [
            ['#', 'include', '<', 'iostream', '>'],
            ['#', 'include', '<', 'stdlib.h', '>', '//', 'bla-bla'],
            ['//', '#', 'include', '<', 'header.hpp', '>'],
            ['/*', '#', 'include', '<', 'h.h', '>', '*/', ],
        ]
        produced_output = map(parser.obtain_header, input_lines)
        expected_output = ['iostream', 'stdlib.h', None, None]
        self.assertEqual(produced_output, expected_output)


if '__main__' == __name__:
    unittest.main()
