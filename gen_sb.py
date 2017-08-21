import random

def f():
    yield
    for i in range(10):
        roll = yield i
        print("f received {}".format(roll))

gen = f()
next(gen)

try:
    while True:
        res = gen.send(random.randint(1, 6))
        print("f calculated {}".format(res))

except StopIteration:
    pass
