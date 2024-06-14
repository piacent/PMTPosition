import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt


def GetGEMsDim():
    """
    Return GEM dimensions in cm (width and height, respectively)
    """
    GEM_width  = 50.0
    GEM_height = 80.0
    return GEM_width, GEM_height