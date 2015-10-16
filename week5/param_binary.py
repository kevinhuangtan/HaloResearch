import h5py
import numpy as np

def header_len(fname):
    """ Get number of header lines."""
    h = 0
    for i, line in enumerate(open(fname)):
        if(line[0] == '#'):
            h += 1
        else:
            return h
    return

def param_gen(f, param, dt):
    line = f.readline()  
    parsed_line = line.strip().split()
    first_row = np.array(tuple(parsed_line), dtype = dt)
    yield first_row[param]
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first']) + 1
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        parsed_line = line.strip().split()
        yield parsed_line[dt.names.index(param)]
        row += 1 

def create_paramater_binary(subvolume_file, tree_directory, ouput_binary, param, dt):
    h = header_len(subvolume_file)
    with open(subvolume_file, 'r') as f:
        with h5py.File(tree_directory,"r") as hf: 
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            offset_sum = 0
            binaryarr = []
            while(tree_index < num_trees):
                print 'tree index', tree_index
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                binaryarr += (list(param_gen(f, param, dt)))
                tree_index += 1
            mm = np.memmap(filename = ouput_binary, 
                dtype=dt[param], mode='w+', shape=(1, len(binaryarr)))
            mm[:] = np.array(binaryarr)
            del mm
    return 


def get_parameter(tree_directory_hdf5, tree_id):
    with h5py.File(tree_directory_hdf5,"r") as hf: 
        offset_size = 8
        offset = offset_size * hf[str(tree_id)][1]
        length = hf[str(tree_id)][0]
        print length
        check = np.memmap(filename='trees/0_0_0/scale.float32/scale.data', dtype="float32", mode='r', shape=(1, length), offset=offset)
        print check
        del check
    return 

