
class OptionEntity(object):
    """
    Holds information
    """

    def __init__(self, short_option, long_option=None, default_value=None):
        self.__short_option = short_option
        self.__long_option = long_option
        self.__value = []
        if default_value is not None:
            self.__value.append(default_value)

        self.__is_value_initialized = False
        self.__met_in_cmd = False

    def __eq__(self, key):
        if isinstance(key, str):
            return key == self.__short_option or key == self.__long_option
        elif isinstance(key, int):
            return key == self.__position
        else:
            raise ValueError("argument must be string or int only")

    def put_value(self, value):
        if not self.__is_value_initialized:
            if len(self.__value):
                self.__value.pop()
        self.__value.append(value)
        self.__is_value_initialized = True

    def get_value(self):
        return self.__value

    def is_set(self):
        return self.__met_in_cmd

    def met_in_cmd(self):
        self.__met_in_cmd = True

    def __str__(self):
        return self.__short_option + " " + self.__long_option


class OptionParser(object):

    def __init__(self):
        self.__options = []

    def parse(self, args):
        current_index = -1
        for word in args:
            current_index = self.__handle_single_word(word, current_index)

    def __handle_single_word(self, word, current_option_index):
        if len(word) and word[0] == '-':  # that's new option word!
            try:
                #  current_option_index = self.__options.index(word)
                current_option_index = self.__options.index(word)
                self.__options[current_option_index].met_in_cmd()
            except ValueError:
                raise ValueError("parameter '" + word + "' is not represented amongst options")
        else:  # parameter comes!
            if current_option_index == -1:
                raise ValueError("'" + word + "' an option should go with '-' in the beginning")
            option = self.__options[current_option_index]
            option.put_value(word)
        return current_option_index

    def add_option(self, short_option, long_option=None, default_value=None):
        self.__options.append(OptionEntity(short_option, long_option, default_value))

    def __getitem__(self, item):
        for i in self.__options:
            if i == item:
                return i
        raise IndexError("")

    def __setitem__(self, key, value):
        for i in self.__options:
            if i == key:
                i.value = value
        raise IndexError("")

    def has_key(self, key):
        for k in self.__options:
            if k == key:
                return k.is_set()
        return False
