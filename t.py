class WrapFunc:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def a(func):
    return WrapFunc(func)

@a
def test(c):
    return c

print(test(1)) 