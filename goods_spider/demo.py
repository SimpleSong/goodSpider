class A(object):

    def __init__(self):
        self.i = 0



class B(object):

    def __init__(self):
        self.super = A()
        self.b = 9


