# Weak signal reconstruction demo. 

A simulation-based demonstration of weak-signal reconstruction using CMB patchy screening as a test case.
This project generates simulated CMB data with a known optical-depth fluctuation field and reconstructs the injected signal using a quadratic estimator.

# Pipeline
1.) Generate GRF CMB simulations with injected patchy screening signal from literature

2.) Pass sims through falafel reconstruction for patchy screening

3.) Normalize the reconstructed maps using tempura

4.) Check that the result contains the desired input signal by taking the cross-power spectrum of the input signal and output map

# Status
Work in progress
