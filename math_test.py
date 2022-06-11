import functools
import time


class My_math:


    def plus(self, data):
        time.sleep(60)
        return sum(data)

    def multiplication(self, data):
        time.sleep(60)
        return functools.reduce(lambda a, b : a * b, data)
