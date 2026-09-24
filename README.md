# Demonstration of weak signal reconstruction with the cosmic microwave background

A simulation-based demonstration of weak-signal reconstruction using CMB patchy screening as a test case.
This project generates simulated CMB data with a known optical-depth fluctuation field and reconstructs the injected signal using a quadratic estimator.

## Pipeline

1. **Simulate:** Generate Gaussian random field CMB simulations and inject a known patchy screening signal based on a theoretical model from the literature.

2. **Reconstruct:** Apply a temperature-based quadratic estimator to the simulated CMB data and normalize the reconstructed optical-depth field.

3. **Validate:** Calculate the cross-power spectrum between the input optical-depth field and the reconstructed field to check for recovery of the injected signal.

## Example Results

The following plots illustrate the simulated CMB data, reconstructed optical-depth field, and pipeline validation.

### Input Simulation

<img src="output/inputmap.png" width="500">

### Reconstructed Signal

<img src="output/reconmap.png" width="500">

### Pipeline Validation

<img src="output/pipeline_verification.png" width="500">

## Installation and Usage

Clone the repository and create a Python virtual environment:

```bash
git clone https://github.com/darbykramer/signal-reconstruction-demo.git
cd signal-reconstruction-demo

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Run the simulation, reconstruction, and plotting scripts:

```bash
cd src

python simulate.py --savepath ../output/ --noiselevel 10 --nsims 1

python reconstruct.py --simpath ../output/

python plotting.py --simpath ../output/ --savepath ../output/
```

The generated figures and simulation files are saved in the `output/` directory.

## Status

The simulation, reconstruction, and validation pipeline runs end-to-end using the dependencies listed in `requirements.txt`.

MPI support may be added in a future update.
