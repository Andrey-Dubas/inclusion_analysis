
class OptionEntity(object):

    def __init__(self, short_option, long_option=None, position=None, default_value=None):
        self.__short = short_option
        self.__long_option = long_option
        self.__position = position
        self.__value = default_value

    def __eq__(self, key):
        if isinstance(key, str):
            return key == self.__short or key == self.__long_option
            return False
        elif isinstance(key, int):
            return key == self.__position
        else:
            raise ValueError("argument must be string or int only")

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    value = property(fset=set_value, fget=get_value)


class OptionParser(object):

    def __init__(self):
        self.__options = []

    def parse(self, args):
        is_key = False
        current_key = None
        for index, obj in enumerate(args):
            if obj in self.__options:
                current_key = obj
            else:
                if current_key is not None:
                    index = self.__options.index(current_key)
                    self.__options[index].value = obj

    def add_option(self, short_option, long_option=None, position=None, default_value=None):
        self.__options.append(OptionEntity(short_option, long_option, position, default_value))

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