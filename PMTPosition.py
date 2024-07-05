import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt


def GetGEMsDim():
    """
    Returns GEM dimensions in cm (width and height, respectively)
    """
    #There's only one GEM face
    GEM_width  = 50.0
    GEM_height = 80.0
    return GEM_width, GEM_height

def GetGEMsZ():
    """
    Returns z distance GEM distance form PMT in cm 
    """
    GEM_z = 59.0 # Updated to the latest design of 17/06/2024
    return GEM_z

def GenEventPosition(x_offset = 0.0, y_offset = 0.0, x_start = 0.0, x_end = 0.0, size = 10, distribution = 'uniform'):
    """
    Returns N=size randomly generated spot positions with the specified spacial `distribution`, and
    assuming an offset = [x_offset, y_offset]
    """

    if size <= 0:
        raise ValueError("Size must be a positive integer.")

    GEM_width, GEM_height = GetGEMsDim()

    if distribution == 'uniform':
        x = st.uniform.rvs(loc = x_offset, scale = GEM_width,  size = size)
        y = st.uniform.rvs(loc = y_offset, scale = GEM_height, size = size)

    elif distribution == 'fixedY':

        x = np.linspace(x_start, x_end, size)
        y = np.full(size, y_offset)

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

def GetIntegrals(R_all = np.array([[0.0, 0.0]]), energy = 5.9, LY = 10000.0):
    """
    Returns integrals of PMT waveforms for all the PMTs in C, given the distance between the PMT and the events (R_all),
    the energy of the event in keV (energy), and the light yield of 55Fe events in the detector in sc_integral (LY)
    """
    # Assuming I = A * Energy / R^4
    # A is extracted by the plot of Fig. 3.27 of M. Folcarelli's thesis [screenshot at doc/Folcarelli_3_27.]
    # N.B. there Li is expressed in nC
    
    A = (np.exp(17.26)/1e+9) # C * cm^4 / sc_integral
    
    # Express now A in C * cm^4 / keV, where 1 sc_integral = (5.9/LY) keV
    A = A / (5.9 / LY)

    # Rescale A such to properly take into account the difference in GEM_z
    GEM_z_LIME = 19.0
    GEM_z      = GetGEMsZ()
    L_0    = A * 5.9 / GEM_z_LIME**4
    L_1    = L_0 * GEM_z_LIME**2 / GEM_z**2
    A_corr = L_1 * GEM_z**4 / 5.9
    # Previous equations equivalent to A_corr = A / (GEM_Z_lime^2 * GEM_z^2) / (5.9/LY)
    
    if not isinstance(energy, np.ndarray):
        all_energies = np.repeat(energy, len(R_all.T[0]))
    else:
        if len(energies) != len(R_all.T[0]):
            raise Exception("PMTposition.GetIntegrals: energy input has wrong size.")
        all_energies = energy

    integrals = np.array([])
    for R in R_all.T:
        if len(integrals) == 0:
            integrals = A_corr * all_energies / R**4
        else:
            integrals = np.vstack((integrals, A_corr * all_energies / R**4))
            
    return integrals.T

def create_bat_input(fname = "./outputs/output_for_bat.txt", run=10000, n_evts=0, trigger=0, ints=[]):
    """
    Creates a file for BAT input containing waveform slice integrals.
    
    Inout format:
    - run: The run number.
    - event: The event number.
    - trigger: The trigger number.
    - ints: A list of lists where each sublist contains the waveform integrals for each PMT.

    -- Example:
    run     event trigger peak_ind/slice    ints[[pmt1,pmt2,pmt3,pmt4]]
    10000	0	    0	        0  	        8.874e-10	5.862e-10	1.285e-09	7.877e-10
    10000	1	    0	        0  	        9.109e-10	6.976e-10	1.326e-09	9.652e-10
    10000	2	    0	        0  	        8.839e-10	8.001e-10	1.278e-09	1.135e-09            
    """
    # Conversion factor from ADU to nC
    ## -> Not required for this version since we already have the results in nC
    # vtg_to_nC = (1. / 4096.) * (4. / 3.) * (1. / 50.)
    vtg_to_nC = 1
    
    slice = 0  # We don't have multiple slices/peaks in this case
    with open(fname, "w") as outFile:
        for evt in range(n_evts):
            outFile.write(f"{run}\t{evt}\t{trigger}\t{slice}")
            
            for pmt_i in range(len(ints[0])):
                outFile.write(f"\t{ints[evt][pmt_i] * vtg_to_nC}")
            
            outFile.write("\n")

if __name__ == "__main__":

    print("\nPositions:")
    pos = GenEventPosition()
    print(pos)

    print("\nR:")
    R   = GetR(PMT_pos = np.array([25.0, 40.0]), Event_pos = pos)
    print(R)

    print("\nR_all:")
    PMT_pos = np.array([[25.0, 20.0], [25.0, 60.0]])
    PMT_pos = np.array([[10.0, 10.0], [10.0, 10.0]])
    R_all   = GetR_All(PMT_pos = PMT_pos, Event_pos = pos)
    print(R_all)

    print("\nIntegrals:")
    ints = GetIntegrals(R_all, energy = 5.9, LY = 8500.0)
    print(ints)