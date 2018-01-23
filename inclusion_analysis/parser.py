import os
import inspect


def _default_action(cur_char, cur_token, token_stack):
    return _parse_initial_state_0(cur_char, cur_token, token_stack)


def _parse_initial_state_0(cur_char, cur_token, token_stack):
    """ a function that analyze character in initial state of finite automaton """
    if cur_char in ' \t':
        return _parse_initial_state_0
    del cur_token[:]
    cur_token.append(cur_char)
    if cur_char.isalpha() or cur_char.isdigit() or cur_char in '_-':
        return _parse_word_1
    if cur_char == '#':
        return _parse_hash_2
    if cur_char in '<>':
        return _parse_shevrons_4
    if cur_char == '"':
        return _parse_double_quotion_5
    if cur_char == '/':
        return _parse_slash_6
    if cur_char == '*':
        return _parse_star_7

    raise ValueError("wrong char in state " + inspect.currentframe().f_code.co_name + ": " + cur_char)


def _parse_word_1(cur_char, cur_token, token_stack):
    """ a function that analyze character in state 1 of finite automaton

    that state means the finite automaton handles word
    """
    if cur_char.isalpha() or cur_char.isdigit() or cur_char in '_-.':
        cur_token.append(cur_char)
        return _parse_word_1
    token_stack.append(''.join(cur_token))
    del cur_token[:]

    if cur_char in ' \t':
        return _parse_initial_state_0
    if cur_char in '<>':
        cur_token.append(cur_char)
        return _parse_shevrons_4
    if cur_char == '"':
        cur_token.append(cur_char)
        return _parse_double_quotion_5
    if cur_char == '/':
        cur_token.append(cur_char)
        return _parse_slash_6
    raise ValueError("wrong char in state " +
                     inspect.currentframe().f_code.co_name + ": " + cur_char)


def _parse_hash_2(cur_char, cur_token, token_stack):
    """ a function that analyze character in state 2 of finite automaton

    that state means the finite automaton has just handled hash character
    """
    token_stack.append('#')
    del cur_token[:]
    if cur_char.isalpha() or cur_char in '_-':
        cur_token.append(cur_char)
        return _parse_word_1
    if cur_char in ' \t':
        return _parse_initial_state_0
    raise ValueError("wrong char in state " +
                     inspect.currentframe().f_code.co_name + ": " + cur_char)


def _parse_shevrons_4(cur_char, cur_token, token_stack):
    """ a function that analyze character in state 4 of finite automaton

    that state means the finite automaton has just handled shevron '<' or '>'
    """
    token_stack.append(''.join(cur_token))
    del cur_token[:]
    return None


def _parse_double_quotion_5(cur_char, cur_token, token_stack):
    """ a function that analyze character in state 5 of finite automaton

    that state means the finite automaton has just handled double quotion
    """
    token_stack.append(''.join(cur_token))
    del cur_token[:]
    return None


def _parse_slash_6(cur_char, cur_token, token_stack):
    """ a function that analyze character in state 6 of finite automaton

    that state means the finite automaton has handled /
    """
    if cur_char in '*/':
        cur_token.append(cur_char)
        token_stack.append(''.join(cur_token))
        del cur_token[:]
        return _parse_comment_8
    token_stack.append('/')
    return None


def _parse_star_7(cur_char, cur_token, token_stack):
    """ a function that analyze character in state 7 of finite automaton

    that state means the finite automaton has handled *
    """
    if cur_char == '/':
        cur_token.append(cur_char)
        token_stack.append(''.join(cur_token))
        del cur_token[:]
        return _parse_comment_8
    return None


def _parse_comment_8(cur_char, cur_token, token_stack):
    """ a function that analyze character in state 8 of finite automaton

    that state means the finite automaton is handling comment
    """
    return None


def _get_lexems(line):
    """
    splits a line info lexems

    :param line: input line
    :type line: str
    :return: a list of lexems
    """
    current_state_function = _default_action
    cur_token = []
    token_stack = []
    line = line.strip('\n')
    for i, ch in enumerate(line):
        try:
            current_state_function = current_state_function(ch, cur_token, token_stack)
            if current_state_function is None:
                current_state_function = _default_action(ch, cur_token, token_stack)
        except ValueError as ex:
            raise ValueError("exception in '" + line + "' char #" + str(i) +
                             ", value '" + line[:i] +
                             ">>>" + ch + "<<<" + line[i+1:] + "': " + ex.message)
    token_stack.append(''.join(cur_token))
    return token_stack


def obtain_header(line_lexems):
    """
    get an included file name from provided lexems

    :param line_lexems: a list of lexems
    :return: file name is include construction exists, None otherwise
    """
    control_stack = []
    include_words = []
    for lex in line_lexems:
        if lex == '//':
            break
        if lex == '/*':
            control_stack.append(lex)
        if lex == '*/':
            if control_stack[-1] == '/*':
                del control_stack[-1]
            else:
                return None
        if len(control_stack) > 0 and control_stack[-1] == '/*':
            continue
        include_words.append(lex)

    i = 1
    while i < len(include_words)-1:
        if include_words[i] == '/':
            include_words[i-1] = include_words[i-1] + include_words[i] + include_words[i+1]
            del include_words[i:i+2]
        i += 1

    if len(include_words) >= 5 and \
            include_words[-5:-2] == ['#', 'include', '<'] and \
            include_words[-1] == '>':
        return include_words[-2]
    if len(include_words) >= 5 and \
            include_words[-5:-2] == ['#', 'include', '"'] and \
            include_words[-1] == '"':
        return include_words[-2]


def find_full_header_name(filename, include_directories):
    """ finds the full path to the file

    :param filename: file name
    :param include_directories: directories to loor the file up
    :rtype filename: str
    :rtype include_directories: str
    :return: full path of file
    :rtype: str
    """
    for path in include_directories:
        full_path = os.path.join(path, filename)
        if os.path.exists(full_path):
            return full_path
    else:
        raise ValueError("no header file was detected: " + filename + ", with include dirs: " + ', '.join(include_directories))


def find_included_headers(filename, include_directories):
    """
    parse a file and return included header names

    :param filename: a file to parse
    :param include_directories: list of directories to look files up
    :rtype filename: str
    :rtype include_directory: str
    :return: a list of included files
    :rtype: list <str>
    """
    full_filename = find_full_header_name(filename, include_directories)
    result = []
    with open(full_filename, 'r') as f:
        for line in f:
            try:
                lexems = _get_lexems(line)
                header_name = obtain_header(lexems)
                if header_name is not None:
                    result.append(header_name)
            except ValueError:
                pass
    return result


def find_project_headers(project_root, header_ext=['h', 'hpp']):
    """
    lookup for headers in subdirectory

    :param project_root: root directory
    :param header_ext: header extension
    :return: a list of found headers as paths from 'project_root' argument
    ..warning.. not used
    """
    project_headers = []
    for root, dirs, files in os.walk(project_root, followlinks=False):
        local_headers = filter(lambda x: len(x.split('.')) == 2 and \
                               x.split('.')[1] in header_ext, files)
        project_headers.extend(map(lambda x: root + x, local_headers))
    return project_headers
