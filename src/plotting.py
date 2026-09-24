import numpy as np
import healpy as hp
from pixell import enmap, curvedsky as cs
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Reconstruct tau signal from inputted CMB sims.')
parser.add_argument("--simpath", type=str, default=None)
parser.add_argument("--lmax", type=int, default=3000, help="What is the largest multipole ell you want to use in the reconstruction?")
parser.add_argument("--lmin", type=int, default=600, help="What is the smallest multipole ell you want to use in the reconstruction?")
parser.add_argument("--nside", type=int, default=2048, help="What healpix resolution would you like to use?")
parser.add_argument("--savepath", type=str, default=None)

args = parser.parse_args()

sim_path = args.simpath
save_path = args.savepath

lmax = args.lmax
nside = args.nside

##### Load up reconstructed and input signals ###################### 

recon_alm = hp.read_alm(sim_path + "/reconstructed_tau_alm_00001.fits") # load reconstructed tau alm
input_alm = hp.read_alm(sim_path + "/tau_alm_00001.fits") #load input tau alm

######## Plot the maps and save figures #######################
recon_map = hp.alm2map(recon_alm, nside=nside)
input_map = hp.alm2map(input_alm, nside=nside)

hp.mollview(input_map, title="Input Map")
plt.savefig(save_path + "/inputmap.png", dpi=300)

hp.mollview(recon_map, title="Reconstructed Map")
plt.savefig(save_path + "/reconmap.png", dpi=300)

######### Take the power spectra and verify that the input spectrum is reconstructed ############

recon_ps = cs.alm2cl(recon_alm) # get the raw, noisy power spectrum of the reconstructed map
tau_ps = cs.alm2cl(input_alm) # get the power spectrum of the tau simulation you put in
cross_ps = cs.alm2cl(recon_alm, input_alm) # get the cross-power spectrum of the input and reconstructed signals

ells, cltau = np.loadtxt("../data/cl_tau.txt", skiprows=1, unpack=True)

###### Make bins to plot the input x output spectrum ##############

bin_edges = np.arange(0, lmax + 1, 100)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

def bin_cl(cl):
    return np.array([
        np.mean(cl[bin_edges[i]:bin_edges[i+1]])
        for i in range(len(bin_edges)-1)
    ])

############# Plot the spectra and save #########################
plt.figure()
plt.semilogy(tau_ps, label="Input Signal Spectrum", c="orange", zorder=0)
plt.scatter(bin_centers, -bin_cl(cross_ps), label="Binned in x out",zorder=1)
plt.ylabel(r"$C_\ell$", fontsize=15)
plt.xlabel(r"$\ell$", fontsize=15)
#### There is a negative sign on the cross spectrum because the input tau signal is positive,
#### but we implement it with a negative sign on the CMB because it removes signal. 
#### Since we reconstruct it without the minus sign, we must correct with a minus sign.

# plt.plot(recon_ps, label="Raw Reconstructed Signal", c="brown") # can plot this, but you will likely have to mess with the axes
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig(save_path + "/pipeline_verification.png", dpi=300)