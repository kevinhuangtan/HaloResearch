import h5py
import numpy as np

dt = np.dtype([
    ('scale', 'f4'), 
    ('haloid', 'i8'), 
    ('scale_desc', 'f4'), 
    ('haloid_desc', 'i8'), 
    ('num_prog', 'i4'), 
    ('pid', 'i8'), 
    ('upid', 'i8'), 
    ('pid_desc', 'i8'), 
    ('phantom', 'i4'), 
    ('mvir_sam', 'f4'), 
    ('mvir', 'f4'), 
    ('rvir', 'f4'), 
    ('rs', 'f4'), 
    ('vrms', 'f4'), 
    ('mmp', 'i4'), 
    ('scale_lastmm', 'f4'), 
    ('vmax', 'f4'), 
    ('x', 'f4'), 
    ('y', 'f4'), 
    ('z', 'f4'), 
    ('vx', 'f4'), 
    ('vy', 'f4'), 
    ('vz', 'f4'), 
    ('jx', 'f4'), 
    ('jy', 'f4'), 
    ('jz', 'f4'), 
    ('spin', 'f4'), 
    ('haloid_breadth_first', 'i8'), 
    ('haloid_depth_first', 'i8'), 
    ('haloid_tree_root', 'i8'), 
    ('haloid_orig', 'i8'), 
    ('snap_num', 'i4'), 
    ('haloid_next_coprog_depthfirst', 'i8'), 
    ('haloid_last_prog_depthfirst', 'i8'), 
    ('haloid_last_mainleaf_depthfirst', 'i8'), 
    ('rs_klypin', 'f4'), 
    ('mvir_all', 'f4'), 
    ('m200b', 'f4'), 
    ('m200c', 'f4'), 
    ('m500c', 'f4'), 
    ('m2500c', 'f4'), 
    ('xoff', 'f4'), 
    ('voff', 'f4'), 
    ('spin_bullock', 'f4'), 
    ('b_to_a', 'f4'), 
    ('c_to_a', 'f4'), 
    ('axisA_x', 'f4'), 
    ('axisA_y', 'f4'), 
    ('axisA_z', 'f4'), 
    ('b_to_a_500c', 'f4'), 
    ('c_to_a_500c', 'f4'), 
    ('axisA_x_500c', 'f4'), 
    ('axisA_y_500c', 'f4'), 
    ('axisA_z_500c', 'f4'), 
    ('t_by_u', 'f4'), 
    ('mass_pe_behroozi', 'f4'), 
    ('mass_pe_diemer', 'f4')
    ])


def header_len(fname):
    """ Get number of header lines."""
    h = 0
    for i, line in enumerate(open(fname)):
        if(line[0] == '#'):
            h += 1
        else:
            return h
    return

def tree_gen(f, dtype = dt):
    line = f.readline()  
    parsed_line = line.strip().split()
    first_row = np.array(tuple(parsed_line), dtype = dt)
    yield None
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first']) + 1
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        yield None
        row += 1 

def create_tree_directory(fname, ouput_fname, dt, **kwargs):
    h = header_len(fname)

    with h5py.File(ouput_fname,"w-") as hf: 
        with open(fname, 'r') as f:
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            offset_sum = 0
            while(tree_index < num_trees):
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                len_arr = len(list(tree_gen(f, dt)))
                hf[tree_id] = np.array([len_arr, offset_sum])
                tree_index += 1
                offset_sum += len_arr
                print tree_index
    return 

# create_tree_directory('tree_0_0_0.dat', 'output.hdf5', dt)

MVIR = 10

def param_gen(f, param):
    line = f.readline()  
    parsed_line = line.strip().split()
    first_row = np.array(tuple(parsed_line), dtype = dt)
    yield parsed_line[MVIR]
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first']) + 1
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        yield line.strip().split()[param]
        row += 1 

def create_paramater_binary(fname, ouput_fname, tree_directory_hdf5, param):
    h = header_len(fname)
    with open(fname, 'r') as f:
        with h5py.File(tree_directory_hdf5,"r") as hf: 
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            offset_sum = 0
            offset_size = 8 # bit sizefor float 64
            # binaryarr =  np.array([])
            binaryarr = []
            while(tree_index < num_trees):
                print 'tree index', tree_index
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                binaryarr += (list(param_gen(f, param)))
                tree_index += 1
            mm = np.memmap(filename='trees/0_0_0/mass.float64/mass.data', dtype='float64', mode='w+', shape=(1, len(binaryarr)))
            mm[:] = np.array(binaryarr)
            print mm
            del mm
    return 

#
# create_paramater_binary('tree_0_0_0.dat','mass', 'output.hdf5', MVIR)

def get_parameter(tree_directory_hdf5, tree_id):
    with h5py.File(tree_directory_hdf5,"r") as hf: 
        offset_size = 8
        offset = offset_size * hf[str(tree_id)][1]
        length = hf[str(tree_id)][0]
        print length
        check = np.memmap(filename='trees/0_0_0/mass.float64/mass.data', dtype="float64", mode='r', shape=(1, length), offset=offset)
        print check
        del check
    return 

get_parameter('output.hdf5', 3060312953)
