class C(object):
    def __init__(self):
        self._x = 0

    def __str__(self):
        return "C -> " + unicode(self._x)

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x += value

    @x.getter
    def x(self):
        self._x += 1
        return self._x

if __name__ == "__main__":
    c = C()

    c._x = 3

    print unicode(c)

    c.x = 2

    print unicode(c)