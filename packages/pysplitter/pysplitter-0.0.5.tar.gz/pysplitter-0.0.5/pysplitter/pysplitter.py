import os
import numpy as np
from glob import glob


def generate_file_name(name, ext='split', pad=4):
    """
    Yield new file sting.
    
    Parameters
    ----------
    name : str
        Base name of the file.
    ext : str, optional
        Desired extension of the file name. Default is 'split'.
    pad : int, optional
        Desired zero-padding that will be added to the incremental file names.
        Default is 4.
    
    Returns
    -------
    iterable
    """
    i = 0
    while True:
        file_name = f'{name}{i:0{pad}d}.{ext}'
        i += 1
        yield file_name


def split(src, dst):
    
    name = dst.split('/')[-1]
    dst_dir = dst.replace(name, '')
    file_name = generate_file_name(name)

    with open(src, 'rb') as infile:
        while True:
            chunk = infile.read(100000000)
            if chunk == b'':
                break
            dst = os.path.join(dst_dir, next(file_name))
            with open(dst, 'wb') as outfile:
                outfile.write(chunk)
                print(f'Data written to {dst}')
    
        

def unsplit(src_dir, pattern: str, dst):
    src_dir = os.path.abspath(src_dir)
    assert os.path.exists(src_dir), f'Path does not exist: {src_dir}'
    
    assert '*' in pattern, f'Pattern does not contain a wildcard: {pattern}'
    search_path = os.path.join(src_dir, pattern)
    
    file_list = glob(search_path)
    assert len(file_list) > 0, \
        f'No files were found at given path: {search_path}'
    
    with open(dst, 'wb') as dst_file:
        for src in file_list:
            with open(src, 'rb') as src_file:   
                data = src_file.read()
                dst_file.write(data)


if __name__ == '__main__':
    src = './data/train75_test25_rs1234/X_train.npy'
    dst = './data/train75_test25_rs1234/X_train'
    split(src, dst)
    
    recon_src = './data/train75_test25_rs1234/'
    recon_dst = './data/train75_test25_rs1234/X_train_recon.npy'
    unsplit(recon_src, 'X_train*.split', recon_dst)
