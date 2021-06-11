import numpy as np
import matplotlib.pyplot as plt
from edibles import PYTHONDIR
from edibles.utils.edibles_oracle import EdiblesOracle
from edibles.utils.edibles_spectrum import EdiblesSpectrum
from edibles.utils.voigt_profile import *
from pathlib import Path
from scipy.stats import pearsonr
from Li_model import fit_LiI_Lines



def determine_correlation(wave, flux, model):
    'This program returns the value of the Pearson correlation coefficient'
    
    this_c, _ = pearsonr(flux, model)
    
    print("Correlation coefficient =",this_c)

    return this_c


#############################################################################
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
v_rad = 19.1
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


coeff_guess1= determine_correlation(wave, flux, ReferenceAbsorptionModel)
plt.plot(wave, flux,label='Data', marker='D',fillstyle='none',color='black')
plt.plot(wave, ReferenceAbsorptionModel, color="blue", marker="*", label="Without continuum")
plt.legend()
# 'model of multiples lines and multpiles cloud components'

# lambda0 = [6707.761, 6707.912, 6707.921, 6708.072]
# f = [4.982e-01, 2.491e-01, 4.982e-01, 2.491e-01]
# gamma = [6e7,6e7,6e7,6e7]
# b = [1, 1, 1, 1]
# N = [1.75e10, 1.75e10, 1e9, 3e9]
# v_rad = [19.1,19.1,20.1,19.1]
# v_resolution = 3.75


# AbsorptionLine = voigt_absorption_line(
#             wave,
#             lambda0=lambda0,
#             b=b,
#             N=N,
#             f=f,
#             gamma=gamma,
#             v_rad=v_rad,
#             v_resolution=v_resolution,
#         )

# coeff_guess2= determine_correlation(wave, flux, AbsorptionLine)






##############################################################################
# "HD 169454"

# pythia = EdiblesOracle()
# List = pythia.getFilteredObsList(object=["HD 169454"], MergedOnly=False,OrdersOnly=True, Wave=6708)
# test = List.values.tolist()
# filename = test[1]
# print(filename)
# sp = EdiblesSpectrum(filename)
# wave = sp.wave
# flux = sp.flux
# wrange = [6707.5, 6708.5]
# idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
# wave = wave[idx]
# flux = flux[idx]
# flux = flux / np.median(flux)

# lambda0 = [6707.761, 6707.912]
# f = [4.3e-01, 2.49e-01]
# gamma = [6e7,6e7]
# b = [1]
# N = [9e9]
# v_rad = 10.1
# v_resolution = 4.3

# ReferenceAbsorptionModel = voigt_absorption_line(
#             wave,
#             lambda0=lambda0,
#             b=b,
#             N=N,
#             f=f,
#             gamma=gamma,
#             v_rad=v_rad,
#             v_resolution=v_resolution,
#         )

# coeff_guess1= determine_correlation(wave, flux, ReferenceAbsorptionModel)


# 'model of multiples lines and multpiles cloud components'

# lambda0 = [6707.761, 6707.912, 6707.921, 6708.072]
# f = [4.982e-01, 2.491e-01, 4.982e-01, 2.491e-01]
# gamma = [6e7,6e7,1e7,1e7]
# b = [1, 1, 1, 1]
# N = [7e9, 3e9, 2e9, 2e9]
# v_rad = [10.1,10.1,10.1,6.1]
# v_resolution = 3.75



# AbsorptionLine = voigt_absorption_line(
#             wave,
#             lambda0=lambda0,
#             b=b,
#             N=N,
#             f=f,
#             gamma=gamma,
#             v_rad=v_rad,
#             v_resolution=v_resolution,
#         )

# coeff_guess2= determine_correlation(wave, flux, AbsorptionLine)

# plt.figure()
# plt.plot(wave, flux, marker='D',fillstyle='none',color='black')
# plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.plot(wave, AbsorptionLine, color="orange", marker="*", label="Voigt model")
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.ylim((0.978,1.015))
# plt.legend()
# plt.show()


###############################################################################

'with or without (you) a continuum'

o=fit_LiI_Lines('HD147889', '20160807')

print(o[0][1])
flux = sp.flux[idx]
coeff_guess2= determine_correlation(wave, flux, o[0])

plt.figure()
plt.plot(wave, flux,label='Data', marker='D',fillstyle='none',color='black')

plt.plot(wave, o[0], color='orange',marker='*', label='With continuum')
plt.legend()













