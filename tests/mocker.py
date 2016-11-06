
class Mocker(object):

    def __init__(self, mocked_function, mock):
        self.__mocked_code = mocked_function.func_code
        self.__mocked = mocked_function
        self.__mock = mock

    def __enter__(self):
        self.__mocked.func_code = self.__mock.func_code

    def __exit__(self, type, value, traceback):
        self.__mocked.func_code = self.__mocked_code
