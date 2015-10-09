import h5py
import numpy as np
MVIR = 10


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

def column_cut_tree_gen(columns_to_keep, f, dtype = dt):
    """ 
    Generator that yields a list of the entire tree, containing the ``columns_to_keep`` 
    stored in the open file object ``f``. 
    
    Parameters 
    ----------
    columns_to_keep : list 
    
    f : open file object

    dt : numpy dtype
        dtype object storing the names of the columns and their type.

    """
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
    """
    Function that writes tree trunks to file.

    Parameters 
    -----------
    fname : string 

    output_fname : string 
    
    dt : numpy dtype
        dtype object storing the names of the columns and their type.
        
    columns_to_keep : list, optional 
        List of columns to keep. Default is all columns.
        If provided, must have the same length as the input ``dt``. 

    """
    h = header_len(fname)
    columns_to_keep = [i for i in range(0, len(dt))]

    with h5py.File(ouput_fname,"w") as hf: 
        with open(fname, 'r') as f:
            with open(ouput_fname, 'w') as o:
                for _ in xrange(0, h):
                    f.readline()
                num_trees = int(f.readline())
                tree_index = 0
                while(tree_index < num_trees):
                    line = f.readline()  
                    tree_id = line[6:].strip('\n')
                    len_arr = len(list(column_cut_tree_gen(columns_to_keep, f, dt)))
                    hf[tree_id] = np.array([len_arr])
                    tree_index += 1
    return 

# create_tree_directory('tree_0_0_0.dat', 'output.hdf5', dt)




# mmap_x = np.memmap(tempfile_x, dtype='float64', mode='w+', shape=(1,npts))
# mmap_x[:] = x[:]


# mmap_i = np.memmap(tempfile_i, dtype='int32', mode='w+', shape=(1,npts))
# mmap_i[:] = i[:]

def get_parameter(f):
    line = f.readline()  
    parsed_line = line.strip().split()
    first_row = np.array(tuple(parsed_line), dtype = dt)
    yield parsed_line[MVIR]
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first']) + 1
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        yield line.strip().split()[MVIR]
        row += 1 

def create_paramater_binary(fname, ouput_fname, tree_directory_hdf5):
    h = header_len(fname)
    with open(fname, 'r') as f:
        with open(ouput_fname, 'a+b') as o:
            m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
            with h5py.File(tree_directory_hdf5,"r") as hf: 
                for _ in xrange(0, h):
                    f.readline()
                num_trees = int(f.readline())
                tree_index = 0
                offset_sum = 0
                offset_size = 8 # bit sizefor float 64
                while(tree_index < num_trees):
                    print tree_index
                    line = f.readline()  
                    tree_id = line[6:].strip('\n')
                    arr = np.array(list(get_parameter(f)))
                    mmap_x = np.memmap(m, dtype='float64', mode='w+', offset = offset_sum * offset_size, shape=(1, hf[tree_id][0]))
                    mmap_x[:] = arr[:]
                    tree_index += 1
                    offset_sum += hf[tree_id][0]
    return 
create_paramater_binary('tree_0_0_0.dat','mass', 'output.hdf5')


