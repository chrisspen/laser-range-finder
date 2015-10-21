from PIL import Image
import numpy as np

def compress_list(lst, bins=10):
    """
    Averages a list of numbers into smaller bins.
    """
    new_lst = []
    chunk_size = int(round(len(lst)/float(bins)))
    for bin in xrange(bins):
        samples = lst[bin*chunk_size:bin*chunk_size+chunk_size]
        new_lst.append(sum(samples)/float(len(samples)))
    return new_lst

def only_red(im):
    """
    Strips out everything except red.
    """
    im = im.convert('RGBA')
    data = np.array(im)
    red, green, blue, alpha = data.T
    im2 = Image.fromarray(red.T)
    return im2

def normalize(arr):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = arr.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
    return arr
