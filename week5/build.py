import subvolume_directory
import tree_directory 
import param_binary
import numpy as np
import h5py
import advanced_data

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
    ('axisA_z_500c', 'f'), 
    ('t_by_u', 'f4'), 
    ('mass_pe_behroozi', 'f4'), 
    ('mass_pe_diemer', 'f4')
    ])


# subvolume_directory.create_subvolume_directory('tree_ascii_data/tree_0_0_0.dat', 
# 	'subvolume_directory.hdf5','0_0_0')


# tree_directory.create_tree_directory('tree_ascii_data/tree_0_0_0.dat', 
# 	'trees/0_0_0/tree_directory.hdf5', dt)


# param_binary.create_paramater_binary('tree_ascii_data/tree_0_0_0.dat', 
# 	'trees/0_0_0/tree_directory.hdf5',
# 	'trees/0_0_0/coprog_depthfirst.int64/coprog_depthfirst.data',
# 	'haloid_next_coprog_depthfirst', dt)

# param_binary.create_paramater_binary('tree_ascii_data/tree_0_0_0.dat', 
# 	'trees/0_0_0/tree_directory.hdf5',
# 	'trees/0_0_0/depthfirst.int64/depthfirst.data',
# 	'haloid_depth_first', dt)


# param_binary.create_paramater_binary('tree_ascii_data/tree_0_0_0.dat', 
# 	'trees/0_0_0/tree_directory.hdf5',
# 	'trees/0_0_0/mass.float32/mass.data',
# 	'mvir', dt)

# param_binary.get_parameter('trees/0_0_0/tree_directory.hdf5', 3060299107)


# param_binary.create_paramater_binary('tree_ascii_data/tree_0_0_0.dat', 
# 	'trees/0_0_0/tree_directory.hdf5',
# 	'trees/0_0_0/scale.float32/scale.data',
# 	'scale', dt)

# param_binary.get_parameter('trees/0_0_0/tree_directory.hdf5', 3060299107)



# advanced_data.clumpy_accretion(3060299107)





