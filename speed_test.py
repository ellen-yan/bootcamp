import numpy as np

x = np.random.random(10000)

def python_sum(x):
    x_sum = 0.0
    for y in x:
        x_sum += y
    return x_sum
