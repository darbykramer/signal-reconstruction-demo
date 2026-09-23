# Demonstration of weak signal reconstruction with the cosmic microwave background

A simulation-based demonstration of weak-signal reconstruction using CMB patchy screening as a test case.
This project generates simulated CMB data with a known optical-depth fluctuation field and reconstructs the injected signal using a quadratic estimator.

# Pipeline
1.) Generate GRF CMB simulations with injected patchy screening signal from literature

2.) Pass sims through manual reconstruction for patchy screening and normalize

3.) Check that the result contains the desired input signal by taking the cross-power spectrum of the input signal and output map

# Status
Pipeline functional for all three stages in simulate.py, reconstruct.py, and plotting.py. Just need cleanup and documentation. May add MPI functionality.
