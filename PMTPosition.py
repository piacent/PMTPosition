import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt


def GetGEMsDim():
    """
    Returns GEM dimensions in cm (width and height, respectively)
    """
    GEM_width  = 50.0
    GEM_height = 80.0
    return GEM_width, GEM_height

def GenEventPosition(x_offset = 0.0, y_offset = 0.0, size = 10, distribution = 'uniform'):
    """
    Returns N=size randomly generated spot positions with the specified spacial `distribution`, and
    assuming an offset = [x_offset, y_offset]
    """
    GEM_width, GEM_height = GetGEMsDim()
    if distribution == 'uniform':
        x = st.uniform.rvs(loc = x_offset, scale = GEM_width,  size = size)
        y = st.uniform.rvs(loc = y_offset, scale = GEM_height, size = size)
    else:
        raise Exception("PMTPosition.GenEventPosition: unknown '"+distribution+"' distribution.")

    pos = np.vstack((x, y)).T
    
    return pos