from tempfile import mkdtemp
import os.path as path
import numpy as np

npts = 700
x = np.zeros(npts, dtype = np.float64)
i = np.zeros(npts, dtype = np.int32)

tempfile_x = path.join(mkdtemp(), 'newfile_x.dat')
print tempfile_x

mmap_x = np.memmap(tempfile_x, dtype='float64', mode='w+', shape=(1,npts))

for i in range(0, 300):
    x[i] = i

mmap_x = x[:]
print mmap_x

newfp = np.memmap(tempfile_x, dtype='float32', mode='r', shape=(1,100))
print newfp


offset_64 = 8 #64 bits, 8 bytes
offset_32 = 4 #32 bits, 4 bytes

halo1_x = np.memmap(tempfile_x, dtype='float64', mode='r', shape=(1,10))
halo2_x = np.memmap(tempfile_x, dtype='float64', mode='r', offset = offset_64 * 300, shape=(1,50))
halo3_x = np.memmap(tempfile_x, dtype='float64', mode='r', offset = offset_64 * 350, shape=(1,350))


print halo1_x

# halo1_x = elements of x of halo 1 read directly from your memory-mapped array on disk
# halo2_i = elements of i of halo 1 read directly from your memory-mapped array on disk