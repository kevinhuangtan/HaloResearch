import h5py

def header_len(fname):
    """ Get number of header lines."""
    h = 0
    for i, line in enumerate(open(fname)):
        if(line[0] == '#'):
            h += 1
        else:
            return h
    return


def create_subvolume_directory(subvolume_file, ouput_fname, subvolume):

    h = header_len(subvolume_file)
    with open(subvolume_file) as f:
        for _ in xrange(0, h):
                f.readline()
        num_trees = int(f.readline())
        n = 0
        with h5py.File(ouput_fname,"w") as hf: 
            for line in f:
                if(line[0] == '#'):
                    tree_id = line[6:].strip('\n')
                    hf[tree_id] = [subvolume]
                    n += 1

    return 

def check_hdf5(subvolume_file):
    with h5py.File(subvolume_file,"r+") as hf: 
        print hf.keys()

    return

