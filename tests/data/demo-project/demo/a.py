from demo.c.d import E, e

from .b import b


def a():
    b()
    e()
    E().print()
    print("This is file a!")
