import numpy as np

num_iterations = 100

def expensive_calculation(seed):
    np.random.seed(seed)
    npts = 1e6

    x = np.random.uniform(-seed, seed, npts)
    return np.std(x)

result = np.zeros(num_iterations)
for i in range(num_iterations):
    result[i] = expensive_calculation(i)

print result

f = open('notparallel.dat', 'w')
f.write(str(result))