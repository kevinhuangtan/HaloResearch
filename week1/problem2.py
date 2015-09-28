import ascii_reader
import numpy as np
import pprint as pp

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

def get_trunk(arr):
    last_mainleaf = int(arr[0]['haloid_last_mainleaf_depthfirst'])
    root = int(arr[0]['haloid_depth_first'])
    length = last_mainleaf - root
    trunk = arr[0: (length + 1)]
    return trunk

def column_cut_tree_gen(columns_to_keep, f, dtype = dt):
    """ 
    Generator that yields a list of length ``chunk_size`` containing the ``columns_to_keep`` 
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
    h = ascii_reader.header_len(fname)
    columns_to_keep = [i for i in range(0, len(dt))]

    with open(fname, 'r') as f:
        with open(ouput_fname, 'w') as o:
            for _ in xrange(0, h):
                f.readline()
            num_trees = int(f.readline())
            tree_index = 0
            while(tree_index < 1):
                line = f.readline()  
                tree_id = line[6:].strip('\n')
                arr = np.array(list(column_cut_tree_gen(columns_to_keep, f, dt)), dtype=dt)
                depth_sort =  arr['haloid_depth_first'].argsort() #sort by depthid
                trunk = get_trunk(arr[depth_sort])
                o.write("#" + tree_id + "\n")
                np.savetxt(ouput_fname, trunk)
                tree_index += 1
        return 

def write_trunk_ascii_old(fname, ouput_fname, dt, **kwargs):
    h = ascii_reader.header_len(fname)
    with open(fname, 'r') as f:
        with open(ouput_fname, 'w') as o:
            for _ in xrange(0, h):
                next(f)    
            num_trees = int(next(f))
            tree_id = ""
            first_line = True
            current_tree = []
            i = 0
            for line in f:
                if(line[0]=='#'):
                    if(not first_line):
                        print i
                        arr = np.array(current_tree, dtype = dt) 
                        depth_sort =  arr['haloid_depth_first'].argsort() #sort by depthid
                        trunk = get_trunk(arr[depth_sort])
                        o.write("#" + tree_id + "\n")
                        np.savetxt(ouput_fname, trunk)
                        current_tree = []
                    first_line = False
                    tree_id = line[6:].strip('\n')
                else:
                    current_tree.append(tuple(line.split()))
                    i += 1
            # o.write("#" + tree_id + "\n")
            # arr = np.array(current_tree, dtype = dt)
            # depth_sort =  arr['haloid_depth_first'].argsort()
            # trunk = get_trunk(arr[depth_sort])
            # np.savetxt(ouput_fname, trunk)
        return 
#156225      
write_trunk_ascii('shortened.dat', 'output.dat', dt)