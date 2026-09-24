# Demonstration of weak signal reconstruction with the cosmic microwave background

A simulation-based demonstration of weak-signal reconstruction using CMB patchy screening as a test case.
This project generates simulated CMB data with a known optical-depth fluctuation field and reconstructs the injected signal using a quadratic estimator.

# Pipeline
1.) Generate GRF CMB simulations with injected patchy screening signal from literature

2.) Pass sims through manual reconstruction for patchy screening and normalize

3.) Check that the result contains the desired input signal by taking the cross-power spectrum of the input signal and output map

# Status
Working end-to-end from base installs in requirements.txt. May add MPI capability soon.

# Example execution sequence:

* I recommend making a new python virtual environment, then activate it and clone the repository *

cd signal-reconstruction-demo

pip install -r requirements.txt

cd src

python simulate.py --savepath ../output/ --noiselevel 10 --nsims 1

python reconstruct.py --simpath ../output/

python plotting.py --simpath ../output/ --savepath ../output/
