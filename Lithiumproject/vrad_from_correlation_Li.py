import numpy as np
import matplotlib.pyplot as plt
from examples import vrad_from_correlation as vrd
from edibles.utils.edibles_oracle import EdiblesOracle
from edibles.utils.edibles_spectrum import EdiblesSpectrum
from edibles.utils import voigt_profile as vp


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


ReferenceAbsorptionModel = vp.voigt_absorption_line(
    wave,
    lambda0=lambda0,
    b=b,
    N=N,
    f=f,
    gamma=gamma,
    v_rad=v_rad,
    v_resolution=v_resolution,
    )


v_rad_guess = vrd.determine_vrad_from_correlation(wave, flux, ReferenceAbsorptionModel)

plt.show()   

######################################################################################
"HD 169454"

pythia = EdiblesOracle()
List = pythia.getFilteredObsList(object=["HD 169454"], MergedOnly=False, Wave=6708)
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
N = [9e9]
v_rad = 0
v_resolution = 4.3


ReferenceAbsorptionModel = vp.voigt_absorption_line(
    wave,
    lambda0=lambda0,
    b=b,
    N=N,
    f=f,
    gamma=gamma,
    v_rad=v_rad,
    v_resolution=v_resolution,
    )

plt.figure()
v_rad_guess = vrd.determine_vrad_from_correlation(wave, flux, ReferenceAbsorptionModel)

plt.show()   




