import os
import numpy as np
import h5py
import matplotlib.pyplot as plt


haloid_depth_first = 2

haloid_last_mainleaf_depthfirst = 3

def trunk_param(haloID, tree, param, dtype):
    tree_direc = "trees/" + tree[0] + "/tree_directory.hdf5"
    with h5py.File(tree_direc, "r") as f:
        length = int(f[str(haloID)][0])
        offset = int(f[str(haloID)][1])

        entire_tree = np.memmap(filename= 'trees/'+ tree[0] + '/' + param + '.' + dtype +'/' + param + '.data', dtype=dtype, mode='r', shape=(1, length), offset=offset)
        entire_tree_depth_sort = np.memmap(filename= 'trees/0_0_0/depthfirst.int64/depthfirst.data', dtype='int64', mode='r', shape=(1, length), offset=offset)
        depth_sort_mask = np.argsort(entire_tree_depth_sort)[0]
        entire_tree = np.array(entire_tree[0])

        last_mainleaf = int(f[str(haloID)][haloid_last_mainleaf_depthfirst])
        root = int(f[str(haloID)][haloid_depth_first])
        trunk_length = last_mainleaf - root

        entire_tree = entire_tree[depth_sort_mask]
        trunk = entire_tree[0: (trunk_length + 1)]
    return trunk

def sort_tree(tree, tree_depth_sort):
    depth_sort_mask = np.argsort(entire_tree_depth_sort)[0]
    entire_tree = np.array(entire_tree[0])
    entire_tree = entire_tree[depth_sort_mask]
    return entire_tree

def clumpy_accretion(haloID):
    with h5py.File('subvolume_directory.hdf5', "r") as svd:
        tree = svd[str(haloID)][...]
    tree_direc = "trees/" + tree[0] + "/tree_directory.hdf5"
    with h5py.File(tree_direc, "r") as td:
        tree_format = td[str(haloID)][...]

    length = tree_format[0]
    offset = tree_format[1]
    
    trunk_mass = trunk_param(haloID, tree, 'mass', 'float32')
    trunk_scale = trunk_param(haloID, tree, 'scale', 'float32')
    trunk_coprog = trunk_param(haloID, tree, 'coprog_depthfirst', 'int64')

    entire_tree = np.memmap(filename= 'trees/'+ tree[0] + '/mass.float32/mass.data', dtype="float32", mode='r', shape=(1, length), offset=offset)
    entire_tree_depth_sort = np.memmap(filename= 'trees/'+ tree[0] + '/depthfirst.int64/depthfirst.data', dtype='int64', mode='r', shape=(1, length), offset=offset)
    depth_sort_mask = np.argsort(entire_tree_depth_sort)[0]
    entire_tree = np.array(entire_tree[0])
    entire_tree = entire_tree[depth_sort_mask]

    entire_tree_coprog = np.memmap(filename= 'trees/'+ tree[0] + '/coprog_depthfirst.int64/coprog_depthfirst.data', dtype="int64", mode='r', shape=(1, length), offset=offset)
    entire_tree_coprog = np.array(entire_tree_coprog[0])
    entire_tree_coprog = entire_tree_coprog[depth_sort_mask]

    clumpyArray = [0] * (len(trunk_mass) - 1)
    root = tree_format[haloid_depth_first]

    for i in range(0, len(trunk_mass) - 1): #last trunk leaf has no progenitors
        clumpy = trunk_mass[i + 1] #MMP
        coprogenitor =  trunk_coprog[i + 1]
        sum = 0
        while(coprogenitor != -1.0): #
            clumpy += entire_tree[coprogenitor - root]
            coprogenitor = entire_tree_coprog[coprogenitor - root]
        clumpyArray[i] = clumpy
    print clumpyArray

    x1 = np.linspace(0, 1, len(clumpyArray))
    x2 = np.linspace(0, 1, len(trunk_mass))

    plt.plot(x1, clumpyArray)
    plt.plot(x2, trunk_mass)

    plt.show()
    return clumpyArray


def smooth_accretion(haloID):
    with h5py.File('subvolume_directory.hdf5', "r") as svd:
        tree = svd[str(haloID)][...]
    trunk_mass = trunk_param(haloID, tree, 'mass', 'float32')

    M_0 = trunk_mass[0]
    smoothArray = []
    clumpy_array = clumpy_accretion(haloID)

    for i in range(0, len(trunk_mass) - 1):
        smooth = trunk_mass[i] - clumpy_array[i]
        smoothArray.append(smooth) 

    # z_array = list(reversed(trunk_table['scale']))
    # z_array = z_array[:(len(z_array) - 1)]
    # plt.plot(z_array, list(reversed(smoothArray)))
    x1 = np.linspace(0, 1, len(smoothArray))

    plt.plot(x1, smoothArray)
    plt.show()
    return smoothArray

smooth_accretion(3060299107)


    