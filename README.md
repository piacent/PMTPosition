# PMTPosition
Code for the "results" of PMT position on CYGNO04

# To do list

* Get the actual z distance from GEM plane to PMTs [done]
* Produce a uniform xy set of spotlike events [done]
  * check the PMT intensity at 6 keV at LIME distance from the GEM and rescale [done]
  * We probably just need the energy (aka PMT integral) and not the full waveform [done]
* Compute the LY integral/amplitude for each PMT assuming R^-something [from 3.5 to 4.5]
* Test different positions [check well geometry] as a fuction from the distance from camera. We can actually play only with the x position (assuming 3 cameras and 8 PMTs)
* Test the different positions assuming the same "charge yield" of the PMTs (operated then at higher voltages wrt LIME)
* Evaluate the "goodness" of a position by means of:
  * Overall amplitude (for efficiency reasons)
  * Ratios among amplitudes
  * Apply Francesco's fit?
* (Optional) Implement some sort of distortion to emulate cam-pmt coordinate transformation
* (Optional) Exotic options? (Asymmetric, different number of PMTs)
