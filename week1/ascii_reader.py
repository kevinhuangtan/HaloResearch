import numpy as np
import pprint as pp
from astropy.table import Table

def create_ascii():
    with open('rockstar', 'w') as f:
        for i in xrange(0, 10):
            f.write("#header lines\n")
        for i in xrange(0, int(10e6)):
            x = np.random.uniform(0,1,1)[0]
            y = np.random.random_integers(-100,100,1)[0]
            z = np.random.random_integers(-100,100,1)[0]
            l = str(x) + ' ' + str(y) + ' ' + str(z)
            l += '\n'
            f.write(l)

# create_ascii()

def file_len(fname):
    """ Note that this includes header lines."""
    for i, line in enumerate(open(fname)):
        pass
    return i+1

def header_len(fname):
    """ Get number of header lines."""
    h = 0
    for i, line in enumerate(open(fname)):
        if(line[0] == '#'):
            h += 1
        else:
            return h
    return

def cut_func(chunk): #func determined later
    """ 
    Generator that yields a list of booleans determining which rows to keep in "chunk". 
    
    Parameters 
    ----------
    chunk : np array 
    """
    return np.ones((1, len(chunk)), dtype=bool)[0]

def column_cut_chunk_gen(chunk_size, columns_to_keep, f):
    """ 
    Generator that yields a list of length ``chunk_size`` containing the ``columns_to_keep`` 
    stored in the open file object ``f``. 
    
    Parameters 
    ----------
    chunk_size : int 
    
    columns_to_keep : list 
    
    f : open file object
    """
    cur = 0
    while cur < chunk_size:
        line = f.readline()    
        parsed_line = line.strip().split()
        yield tuple(parsed_line[i] for i in columns_to_keep)
        cur += 1 

def fast_ascii_reader(fname, dt, **kwargs):
    """
    Parameters 
    -----------
    fname : string 
    
    dt : numpy dtype
        dtype object storing the names of the columns and their type.
    
    cut_func : function object, optional 
        function used to apply row-wise cuts to the ascii file. Default is no cuts. 
        
    columns_to_keep : list, optional 
        List of columns to keep. Default is all columns.
        If provided, must have the same length as the input ``dt``. 
        
    chunksize : int, optional 
        Size of the chunks to use when reading in the data. 
        Varying chunksize impacts performance, but not the returned result. 
        Default is nrows/10.
        
    Returns 
    -------
    data : astropy table
        table storing data of type ``dt`` for only the requested rows and columns
    """
    with open(fname, 'r') as f:

        if(not 'columns_to_keep' in kwargs):
            columns_to_keep = [i for i in range(0, len(dt))]

        h = header_len(fname)
        num_total_rows = file_len(fname) - h
        if(not 'chunksize' in kwargs):
            chunksize = int(num_total_rows / 10.)
        num_full_chunks = num_total_rows/chunksize
        chunksize_remainder = num_total_rows % chunksize

        for i in xrange(0,h):
            f.readline()
        for ichunk in xrange(num_full_chunks):
            chunk_array = np.array(list(column_cut_chunk_gen(chunksize, columns_to_keep, f)), dtype=dt)
            mask = cut_func(chunk_array)
            try:
                full_array = np.append(full_array, chunk_array[mask])
            except NameError:
                full_array = chunk_array[mask]
        chunk_array = np.array(list(column_cut_chunk_gen(chunksize_remainder, columns_to_keep, f)), dtype=dt)
        mask = cut_func(chunk_array)
        full_array = np.append(full_array, chunk_array[mask])
    return Table(full_array)

# print fast_ascii_reader('rockstar', np.dtype([('age','f8'),('height','int8'),('weight','int8')]))



