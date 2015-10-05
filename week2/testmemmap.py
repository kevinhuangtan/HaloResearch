import numpy as np

import multiprocessing as mp

def expensive_calculation(seed, output):
    np.random.seed(seed)
    npts = 1e6

    x = np.random.uniform(-seed, seed, npts)
    output.put(np.std(x))


output = mp.Queue()
num_iterations = 100

# for i in range(num_iterations):
#     result[i] = expensive_calculation(i)

processes = [mp.Process(target=expensive_calculation, args=(seed, output)) for seed in range(0, num_iterations)]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

print(results)
print type(results[0])

f = open('parallel.dat', 'w')
f.write(str(results))

# print("done")
