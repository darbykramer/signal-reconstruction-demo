import numpy as np
import healpy as hp
from pixell import curvedsky as cs
from tempura.pytempura.norm import get_norms
import camb
import argparse

parser = argparse.ArgumentParser(description='Reconstruct tau signal from inputted CMB sims.')
parser.add_argument("--simpath", type=str, default=None)
parser.add_argument("--lmax", type=int, default=3000, help="What is the largest multipole ell you want to use in the reconstruction?")
parser.add_argument("--lmin", type=int, default=600, help="What is the smallest multipole ell you want to use in the reconstruction?")
parser.add_argument("--rlmax", type=int, default=3000, help="What is the largest multipole L you want to reconstruct?")
parser.add_argument("--rlmin", type=int, default=600, help="What is the lowest multipole L you want to reconstruct?")
parser.add_argument("--nside", type=int, default=2048, help="What healpix resolution would you like to use?")

args = parser.parse_args()

sim_path = args.simpath

mlmax = args.lmax

lmax = args.lmax
lmin = args.lmin

rlmin, rlmax = args.rlmin, args.rlmax  # CMB multipole range for reconstruction

nside = args.nside

############## Get CMB theory from camb ####################

pars = camb.CAMBparams()
pars.set_cosmology(H0=67.5, ombh2=0.022, omch2=0.122)
pars.InitPower.set_params(As=2e-9, ns=0.965)
pars.set_for_lmax(lmax, lens_potential_accuracy=0)

results = camb.get_results(pars)

powers = results.get_cmb_power_spectra(
    pars,
    CMB_unit='muK',
    raw_cl=True
)

ucl = powers['unlensed_scalar']

cl_tt = ucl[:lmax+1, 0]
cl_ee = ucl[:lmax+1, 1]
cl_bb = ucl[:lmax+1, 2]
cl_te = ucl[:lmax+1, 3]

#### Load in screened CMB simulation ########################################################

alm = hp.read_alm(
    sim_path + "modulated_cmb_alm_00001.fits"
)

cl_tot = cs.alm2cl(alm)

#### Filter & Reconstruct ##############################################################################

ivfilt = np.zeros(lmax + 1)
ivfilt[lmin:lmax+1] = 1. / cl_tot[lmin:lmax+1] # inverse variance filter

wfilt = np.zeros(lmax + 1)
wfilt[lmin:lmax+1] = cl_tt[lmin:lmax+1] / cl_tot[lmin:lmax+1] # Wiener filter

falm = hp.almxfl(alm, ivfilt) # apply IV filter
walm = hp.almxfl(alm, wfilt) # apply Wiener filter

fmap = hp.alm2map(falm, nside=nside) # inverse SHT the IV filtered alms to real space
wmap = hp.alm2map(walm, nside=nside) # inverse SHT the Wiener-filtered alms to real space

recon_alm = hp.map2alm(fmap * wmap, lmax=mlmax) # multiply the IV and Wiener-filtered maps together

# this is now an un-normalized screening map that contains our inputted signal.

### Normalization #################################################################################

cl = np.zeros((4,lmax+1)) # TT, EE, BB, TE

cl[:,2:] = [cl_tt[2:], cl_ee[2:], cl_bb[2:], cl_te[2:]]

ocl = [(cl[0])*1., (cl[1])*1., (cl[2])*1., (cl[3])*1.]

oclsnoise = {'TT' : cl_tot, 'EE': 0, 'BB': 0, 'TE': 0}
ocls = {'TT' : ocl[0], 'EE': ocl[1], 'BB': ocl[2], 'TE': ocl[3]}
ucls = {'TT' : cl[0], 'EE': cl[1], 'BB': cl[2], 'TE': cl[3]}

Aestnoise = get_norms(['tt'],ucls,oclsnoise,rlmin,rlmax,coupling=["tau"])

### Apply Normalization ###################################################

final_alm = hp.almxfl(recon_alm, Aestnoise['tt'])

#### Save alm ########

hp.write_alm(
    sim_path + "/reconstructed_tau_alm_00001.fits",
    final_alm,
    overwrite=True
)