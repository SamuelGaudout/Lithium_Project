import matplotlib.pyplot as plt
import numpy as np
import csv

from edibles.utils import voigt_profile as vp
from edibles.utils import edibles_oracle

List1=[]
with open("Files_Lithium_6707A.txt","r") as files:
    for l in files:
        List1.append(l)

List=[]
for l in List1:
    p=l.replace('\n', '')
    List.append(p)


L1=List[0]
shift=(0,0.8391) #for List[0]

sp = edibles_oracle.EdiblesSpectrum(L1)
fluxN=[]
wa0=[]
wa1=[]
wa2=[]
for i in sp.flux:
    i=i/(sp.flux[2869]) #normalization
    fluxN.append(i)
for o in sp.wave:
    a=o-shift[0]
    b=o-shift[1]
    wa0.append(a)
    wa1.append(b)
    #print(fluxN)
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.plot(wa0, fluxN, label=L1, marker='D',fillstyle='none',color='black')


#############################################################################
'model with a simple line'


wavegrid = np.arange(1000) * 0.01 + 6705
AbsorptionLine = vp.voigt_absorption_line(
            wavegrid,
            lambda0=(6707.761+6707.912)/2,
            b=2.8,
            N=3.2e10,
            f=0.374,
            gamma=6e7,
            v_rad=37.5,
            v_resolution=7.75,
        )
# plt.plot(wavegrid, AbsorptionLine, marker="1",label='Voigt profile')
# plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.ylim((0.97,1.03))
# plt.xlim((6707,6712))
# plt.legend()
# plt.show()

#############################################################################
'model multiple lines, single cloud for the List[8]'

L1=List[5]
shift=[0,0.0895] #for List[0,1]

# sp = edibles_oracle.EdiblesSpectrum(L1)
# fluxN=[]
# wa0=[]
# wa1=[]
# wa2=[]
# for i in sp.flux:
#     i=i/(sp.flux[2869]) #normalization
#     fluxN.append(i)
# for o in sp.wave:
#     a=o-shift[0]
#     b=o-shift[1]
#     wa0.append(a)
#     wa1.append(b)
#     #print(fluxN)
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.figure()
# plt.plot(wa0, fluxN, label=L1)
# plt.ylim((0.975,1.015))
# plt.xlim((6707,6709))
# plt.show()


lambda0 = [6707.725, 6707.938]
f = [4.99e-01, 1.8e-01]
gamma = [6e7, 6e7]
b = [1]
N = [3.7e9]
v_rad = 11
v_resolution = 3.5

filename=L1
wrange = [6707.5, 6708.5]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )
# plt.figure()
# plt.plot(wave, flux,label=L1, marker='D',fillstyle='none',color='black')
# plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.plot(wave, AbsorptionLine, color="orange", marker="*", label="voigt model")
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.ylim((0.98,1.015))

# plt.legend()
# plt.show()
    

#############################################################################
'model multiple lines, single cloud for the List[5]'

L1=List[5]



lambda0 = [6707.725, 6707.938]
f = [4.99e-01, 1.8e-01]
gamma = [6e7, 6e7]
b = [1]
N = [3.7e9]
v_rad = 11
v_resolution = 3.5

filename=L1
wrange = [6707.5, 6708.5]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )
# plt.figure()
# plt.plot(wave, flux,label=L1, marker='D',fillstyle='none',color='black')
# plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.plot(wave, AbsorptionLine, color="orange", marker="*", label="voigt model")
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.ylim((0.98,1.015))

# plt.legend()
# plt.show()


#############################################################################
'model multiple lines, single cloud for the List[4]'


L1=List[4]

lambda0 = [6707.761, 6707.917]
f = [4.99e-01, 3.49e-01]
gamma = [6e7, 6e7]
b = [1]
N = [1.35e10]
v_rad = 17.31
v_resolution = 2.5

filename=L1
wrange = [6707.5, 6709]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )
# plt.figure()
# plt.plot(wave, flux,label=L1, marker='D',fillstyle='none',color='black')
# plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.plot(wave, AbsorptionLine, color="orange", marker="*", label="Voigt model")
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.ylim((0.95,1.015))

# plt.legend()
# plt.show()


#####################################################################################
'model multiple lines, single cloud for the List[10]'


L1=List[10]

lambda0 = [6707.761, 6707.912]
f = [4.3e-01, 2.49e-01]
gamma = [6e7,6e7]
b = [1]
N = [9e9]
v_rad = 10.1
v_resolution = 4.3

filename=L1
wrange = [6707.5, 6708.5]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )
# plt.figure()
# plt.plot(wave, flux,label=L1, marker='D',fillstyle='none',color='black')
# plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.plot(wave, AbsorptionLine, color="orange", marker="*", label="Voigt model")
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.ylim((0.975,1.015))

# plt.legend()
# plt.show()


#####################################################################################
'model multiple lines, single cloud for the List[3]'

L1=List[3]

lambda0 = [6707.761, 6707.917]
f = [4.85e-01, 2.69e-01]
gamma = [6e7,6e7]
b = [1]
N = [1.75e10]
v_rad = 19
v_resolution = 3.75





filename=L1
wrange = [6707.5, 6709]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )
# plt.figure()
# plt.plot(wave, flux,label=L1, marker='D',fillstyle='none',color='black')
# plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
# plt.plot(wave, AbsorptionLine, color="orange", marker="*", label="Voigt model")
# plt.xlabel("Wavelength (" + r"$\AA$" + ")")
# plt.ylim((0.96,1.015))

# plt.legend()
# plt.show()

###############################################################################
'model multiple lines, multiples clouds components'



L1=List[3]

lambda0 = [6707.761, 6707.912, 6707.921, 6708.072]
f = [4.982e-01, 2.491e-01, 4.982e-01, 2.491e-01]
gamma = [6e7,6e7,6e7,6e7]
b = [1, 1, 1, 1]
N = [16.6977095e9, 16.6977095e9, 1.04770514e9, 1.04770514e9]
v_rad = [19.1,19.1,19.1,19.1]
v_resolution = 3.75





filename=L1
wrange = [6707.5, 6709]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )

res=[]
for i in range(len(AbsorptionLine)):
    res.append(-AbsorptionLine[i]+flux[i]+1)

plt.figure()
plt.plot(wave, flux,label=L1, marker='D',fillstyle='none',color='black')
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
#plt.plot(wave, AbsorptionLine, color="orange", marker="*", label="Voigt model")
#plt.plot(wave,res,color='green',label='Residual flux')
plt.xlabel("Wavelength (" + r"$\AA$" + ")")
plt.ylim((0.96,1.015))
plt.xlabel('Wavelength $\AA$')
plt.legend()
plt.show()


##########################################################################
'isotpic effect : contribution of the two isotop'


L1=List[3] 

lambda0 = [6707.761, 6707.912]
f = [4.982e-01, 2.491e-01]
gamma = [6e7,6e7]
b = [1, 1]
N = [1.7e10, 1.7e10]
v_rad = [19.1,19.1]
v_resolution = 3.75

filename=L1
wrange = [6707.5, 6709]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )

AbsorptionLine7 = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )


lambda0 = [6707.921, 6708.072]
f = [4.982e-01, 2.491e-01]
gamma = [6e7,6e7]
b = [1, 1]
N = [ 2e9, 2e9]
v_rad = [20.1,19.1]
v_resolution = 3.75





filename=L1
wrange = [6707.5, 6709]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine6 = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )


# plt.plot(wave, AbsorptionLine7, color="blue", marker="*", label="7Li contribution")
# plt.plot(wave, AbsorptionLine6, color="green", marker="*", label="6Li contribution")

# plt.legend()
# plt.show()

##############################################################################

'isotpic effect : contribution of the two isotops with the lm_fit params'


L1=List[3] 

lambda0 = [6707.761, 6707.912]
f = [4.982e-01, 2.491e-01]
gamma = [6e7,6e7]
b = [1.70304584, 1.70304584]
N = [16.6977095e9, 16.6977095e9]
v_rad = [19.1,19.1]
v_resolution = 3.75

filename=L1
wrange = [6707.5, 6709]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )

AbsorptionLine7 = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )


lambda0 = [6707.921, 6708.072]
f = [4.982e-01, 2.491e-01]
gamma = [6e7,6e7]
b = [1, 1]
N = [ 1.04770514e9, 1.04770514e9]
v_rad = [19.1,19.1]
v_resolution = 3.75





filename=L1
wrange = [6707.5, 6709]
sp = edibles_oracle.EdiblesSpectrum(filename)
wave = sp.wave
flux = sp.flux
idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
wave = wave[idx]
flux = flux[idx]
flux = flux / np.median(flux)
AbsorptionLine6 = vp.voigt_absorption_line(
            wave,
            lambda0=lambda0,
            b=b,
            N=N,
            f=f,
            gamma=gamma,
            v_rad=v_rad,
            v_resolution=v_resolution,
        )


plt.plot(wave, AbsorptionLine7, color="blue", marker="*", label="7Li contribution")
# plt.plot(wave, AbsorptionLine6, color="green", marker="*", label="6Li contribution")

# plt.legend()
# plt.show()

















