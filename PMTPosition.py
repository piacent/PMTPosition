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

def GetGEMsZ():
    """
    Returns z distance GEM distance form PMT in cm 
    """
    GEM_z = 60.0 # FIXME: put here the real number!!!
    return GEM_z

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

def GetR(PMT_pos = np.array([0.0, 0.0]), Event_pos = np.array([[0.0, 0.0]])):
    """
    Returns distance between events and the PMT in cm, given the PMT position (PMT_pos) and the position of the events (Event_pos)
    """
    GEM_z = GetGEMsZ()
    R     = np.sqrt(GEM_z**2 + (PMT_pos[0] - Event_pos.T[0])**2 + (PMT_pos[1] - Event_pos.T[1])**2)
    return R

def GetR_All(PMT_pos = np.array([[0.0, 0.0]]), Event_pos = np.array([[0.0, 0.0]])):
    """
    Returns distance between events and all the PMTs in cm, given the PMT positions (PMT_pos) and the position of the events (Event_pos)
    """
    R_all = np.array([])
    for pmt_xy in PMT_pos:
        if len(R_all) == 0:
            R_all = GetR(PMT_pos = pmt_xy, Event_pos = Event_pos)
        else:
            R_all = np.vstack((R_all, GetR(PMT_pos = pmt_xy, Event_pos = Event_pos)))
    return R_all.T
    



if __name__ == "__main__":

    print("\nPositions:")
    pos = GenEventPosition()
    print(pos)

    print("\nR:")
    R   = GetR(PMT_pos = np.array([25.0, 40.0]), Event_pos = pos)
    print(R)

    print("\nR_all:")
    PMT_pos = np.array([[25.0, 20.0], [25.0, 60.0]])
    R_all   = GetR_All(PMT_pos = PMT_pos, Event_pos = pos)
    print(R_all)
