# PMT Position
This repository constains a small Toy MC used by the [CYGNO collaboration](https://web.infn.it/cygnus/cygno/) to assess the best positions for the PMTs in the upcoming CYGNO-04.

## Requirements

A running version of BAT, and the following repository: [BAT_PMTs](https://github.com/davidjgmarques/BAT_PMTs)

A running version of Python with the following libraries installed:

* numpy
* pandas
* scipy
* matplotlib
* argparse

## Classes

The `PMTPosition.py` class contains all the necessary functions for this simulation. 

### Scripts for comparisons

You can use ``sim_vs_MC.py`` to compare the simulated data with the fitted one.

Usage: ``python sim_vs_MC.py ./outputs/fitted_data/fitted_dx_0.txt ./outputs/dx_0_mc_truth.txt``

Similarly, you can use``compare_options`` to visually compare the different PMT options.

Usage: ``python compare_options.py ./outputs/fitted_data/fitted_dx_0.txt ./outputs/dx_0_mc_truth.txt ./outputs/fitted_data/fitted_dx_1666.txt  ./outputs/dx_1666_mc_truth.txt``

## Additional tests

Exotic options:

* Asymmetric distribution of PMTs
* Different number of PMTs


