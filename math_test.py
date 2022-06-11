import functools

class My_math:

    def plus(self, data):
        return sum(data)

    def multiplication(self, data):
        return functools.reduce(lambda a, b : a * b, data)
