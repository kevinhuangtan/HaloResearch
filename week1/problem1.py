import numpy as np
from itertools import islice
import pprint as pp

def create_ascii():
    # print 1-e
    with open('rockstar', 'w') as f:
        for i in xrange(0, 10):
            f.write("#header lines\n")
        for i in xrange(0, int(35)):
            x = np.random.uniform(0,1,1)[0]
            y = np.random.random_integers(-100,100,1)[0]
            z = np.random.random_integers(-100,100,1)[0]
            l = str(x) + ' ' + str(y) + ' ' + str(z)
            l += '\n'
            f.write(l)

create_ascii()

def ascii_reader(chunksize, *args):
    if(not args):
        args = [0,1,2]
    with open('rockstar', 'r') as f:

        for i in xrange(0, 10):
            f.readline() #skip headers

        while True:
            # chunk = list(islice(f, 10))
            chunk = []
            for i in xrange(0, chunksize):
                line = f.readline().split()
                if(line):
                    chunk.append([line[i] for i in args])
                else: #last chunk will cover reminader
                    break 
            if not chunk:
                break
            # print chunk
            pp.pprint(chunk)
            yield chunk

# ascii_reader()
a = ascii_reader(10)
a.next()
a.next()
a.next()
a.next()
# print a.next()
# print a.next()






