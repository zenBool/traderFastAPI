import sys


class SayNameSys:
    def tools(self):
        print(f'SYS Print from {sys._getframe().f_code.co_name}')


test = SayNameSys()
print(test.tools())

import traceback


def say_my_name():
    stack = traceback.extract_stack()
    print('Print from line <{}> in method <{}>'.format(stack[-2][1], stack[-2][2]))
    print(stack.__str__())


class Test:
    def func_1(self):
        print(self.__class__.__name__)
        say_my_name()

    def func_2(self):
        say_my_name()

    def func_3(self):
        say_my_name()


test = Test()
test.func_1()
test.func_2()
test.func_3()

# ====================================
# From ChatGPT
import inspect


class MyClass:
    def my_method(self):
        print(inspect.stack()[0][3])


obj = MyClass()
obj.my_method()  # выводит "my_method"
