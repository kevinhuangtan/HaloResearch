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
def tree_gen(f, tree_data, dt):
    line = f.readline()  
    parsed_line = line.strip().split()
    first_row = np.array(tuple(parsed_line), dtype = dt)
    yield None
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first']) + 1
    tree_data[0] = first_row['haloid_depth_first']
    tree_data[1] = first_row['haloid_last_mainleaf_depthfirst']
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        yield None
        row += 1 

def create_tree_directory(subvolume_file, tree_directory_fname, dt):
    h = header_len(subvolume_file)
    with h5py.File(tree_directory_fname,"w-") as hf: 
        with open(subvolume_file, 'r') as f:
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            offset_sum = 0
            tree_data = [0,0]
            while(tree_index < num_trees):
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                len_arr = len(list(tree_gen(f, tree_data, dt)))
                hf[tree_id] = np.array([len_arr, offset_sum, tree_data[0], tree_data[1]])
                tree_index += 1
                offset_sum += len_arr
                print tree_index
    return 




