import numpy as np
import matplotlib.pyplot as plt
from edibles import PYTHONDIR
from edibles.utils.edibles_oracle import EdiblesOracle
from edibles.utils.edibles_spectrum import EdiblesSpectrum
from edibles.utils.voigt_profile import *
from pathlib import Path
import astropy.constants as cst
from scipy.interpolate import interp1d
from scipy.stats import pearsonr


def determine_vrad_from_correlation(wave, flux, model):
    """
    Function to calculate the correlation between an observed spectrum and a model as a function of
    radial velocity and return the radial velocity with the highest correlation coefficient. 

    Args:
        wave (float64): array of wavelengths
        flux (float64): Flux (observed)
        model(float64): model

    Returns:
        vrad_best: radial velocity corresponding to highest correlation. 

        """
    # Create the grid of velocities at which to calculate the correlation. 
    # Using a step size of 0.1 km/s here, and a range of -50 to 50; this should 
    # suffice for most sightlines. 
    v_rad_grid = np.arange(-50.,50.,.1) # in km / s
    all_corr = v_rad_grid * 0.
    #print(v_rad_grid)
    for loop in range(len(v_rad_grid)):
        v_rad = v_rad_grid[loop]
        Doppler_factor = 1. + v_rad / cst.c.to("km/s").value
        #print(Doppler_factor)
        new_wave = wave * Doppler_factor
        # Interpolate shifted model to original wavelength grid
        interpolationfunction = interp1d(
        new_wave, model, kind="cubic", fill_value="extrapolate")
        interpolatedModel = interpolationfunction(wave)
        # Calculate correlation coefficient
        this_c, _ = pearsonr(flux, interpolatedModel)
        all_corr[loop] = this_c
        #print(v_rad, this_c)
        #plt.plot(wave, flux)
        #plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
        #plt.plot(wave, interpolatedModel, color="orange", marker="*")
        #plt.show()
    # Return the radial velocity at the maximum correlation.  
    v_rad_best = v_rad_grid[np.argmax(all_corr)]
    hcorr=all_corr[np.argmax(all_corr)]
    print("Highest correlation for v_rad = ",v_rad_best)
    print('Highest correlation =',hcorr)
    
    # plt.figure()
    # plt.plot(v_rad_grid, all_corr, marker='*')
    # plt.xlabel("v_rad [km/s]")
    # plt.ylabel("Correlation coefficient")
    # plt.axvline(v_rad_best, color='red')
    # plt.title(filename)
    # plt.show()
    Doppler_factor = 1. + v_rad_best / cst.c.to("km/s").value
    new_wave = wave * Doppler_factor
    interpolationfunction = interp1d(
        new_wave, model, kind="cubic", fill_value="extrapolate")
    interpolatedModel = interpolationfunction(wave)
    
    # plt.figure()
    plt.plot(wave, flux, marker='D',fillstyle='none',color='black')
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.plot(wave, interpolatedModel, marker="*")
    plt.xlabel("Wavelength (" + r"$\AA$" + ")")
    plt.title(filename)
    plt.show()

    return v_rad_best



##############################################################################
"HD 147889"

pythia = EdiblesOracle()
List = pythia.getFilteredObsList(object=["HD 147889"], MergedOnly=False, Wave=6708)
test = List.values.tolist()
filename = test[3]
print(filename)
wrange = [6707,6709]
sp = EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)


lambda0 = [6707.761, 6707.912]
f = [4.99e-01, 2.49e-01]
gamma = [6e7,6e7]
b = [1]
N = [1.75e10]
v_rad = 0
v_resolution = 3.75


ReferenceAbsorptionModel = voigt_absorption_line(
    wave,
    lambda0=lambda0,
    b=b,
    N=N,
    f=f,
    gamma=gamma,
    v_rad=v_rad,
    v_resolution=v_resolution,
    )


v_rad_guess1 = determine_vrad_from_correlation(wave, flux, ReferenceAbsorptionModel)


'model of multiples lines and multpiles cloud components'

lambda0 = [6707.761, 6707.912, 6707.921, 6708.072]
f = [4.982e-01, 2.491e-01, 4.982e-01, 2.491e-01]
gamma = [6e7,6e7,6e7,6e7]
b = [1, 1, 1, 1]
N = [1.75e10, 1.75e10, 1e9, 3e9]
v_rad = [0,0,0,0]#[19.1,19.1,20.1,19.1]
v_resolution = 3.75


AbsorptionLine = voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )

v_rad_guess2 = determine_vrad_from_correlation(wave, flux, AbsorptionLine)

######################################################################################
"HD 169454"

# pythia = EdiblesOracle()
# List = pythia.getFilteredObsList(object=["HD 169454"], MergedOnly=False, Wave=6708)
# test = List.values.tolist()
# filename = test[3]
# print(filename)
# wrange = [6707,6709]
# sp = EdiblesSpectrum(filename)
# wave = sp.wave
# flux = sp.flux
# idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
# wave = wave[idx]
# flux = flux[idx]
# flux = flux / np.median(flux)

# lambda0 = [6707.761, 6707.912]
# f = [4.99e-01, 2.49e-01]
# gamma = [6e7,6e7]
# b = [1]
# N = [9e9]
# v_rad = 0
# v_resolution = 4.3


# ReferenceAbsorptionModel = voigt_absorption_line(
#     wave,
#     lambda0=lambda0,
#     b=b,
#     N=N,
#     f=f,
#     gamma=gamma,
#     v_rad=v_rad,
#     v_resolution=v_resolution,
#     )


# v_rad_guess = determine_vrad_from_correlation(wave, flux, ReferenceAbsorptionModel)

# v_rad = [v_rad_guess]

# AbsorptionLine = voigt_absorption_line(
#     wave,
#     lambda0=lambda0,
#     b=b,
#     N=N,
#     f=f,
#     gamma=gamma,
#     v_rad=v_rad,
#     v_resolution=v_resolution,
#     )



# plt.show()   




