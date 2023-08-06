# coding:utf-8


class Color(object):
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @classmethod
    def get_colored(klass, color, text):
        return color + text + klass.END

    @classmethod
    def print(klass, color, text):
        print(klass.get_colored(color, text))
