import numpy as np
from astropy.table import Table

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

def get_trunk_mask(tree):
    """ 
    Generator that returns a slice of the tree that contains the trunk. 
    
    Parameters 
    ----------
    tree : np array 
  
    Returns 
    -------
    trunk : numpy array

    """
    last_mainleaf = int(tree[0]['haloid_last_mainleaf_depthfirst'])
    root = int(tree[0]['haloid_depth_first'])
    length = last_mainleaf - root
    trunk = tree[0: (length + 1)]
    return trunk

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
    yield first_row
    tree_length = int(first_row['haloid_last_prog_depthfirst']) - int(first_row['haloid_depth_first']) + 1
    row = 0
    while row < tree_length - 1:
        line = f.readline() 
        parsed_line = line.strip().split()
        yield tuple(parsed_line[i] for i in columns_to_keep)
        row += 1 

def write_trunk_ascii(fname, ouput_fname, dt, **kwargs):
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

    with open(fname, 'r') as f:
        with open(ouput_fname, 'w') as o:
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            while(tree_index < num_trees):
                print tree_index
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                arr = np.array(list(column_cut_tree_gen(columns_to_keep, f, dt)), dtype=dt)
                depth_sort =  arr['haloid_depth_first'].argsort()
                trunk = get_trunk_mask(arr[depth_sort])
                o.write("#" + tree_id + "\n")
                np.savetxt(ouput_fname, trunk)
                tree_index += 1
    return 
    

write_trunk_ascii('tree_0_0_0.dat', 'output.dat', dt)

