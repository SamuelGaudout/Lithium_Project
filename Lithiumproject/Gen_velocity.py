import matplotlib.pyplot as plt

from edibles.utils import edibles_oracle
from edibles.utils.edibles_spectrum import EdiblesSpectrum

def Local_minimum(object,Wave):
    pythia = edibles_oracle.EdiblesOracle()
    List=pythia.getFilteredObsList(object=object,Wave=Wave, OrdersOnly=True)
    test = List.values.tolist()
    filename = test[0]
    # print(filename)
    wrange = [3301.5, 3304.0]
    sp = EdiblesSpectrum(filename)
    wave = sp.wave
    flux = sp.flux
    Localmin=1e90
    LocalminWave=0
    for i in range(1,len(flux)-1):
        if wave[i]<(Wave+0.8) and wave[i]>(Wave-0.5):
            if flux[i]<Localmin:
                Localmin=flux[i]
                LocalminWave=wave[i]
            
    return(LocalminWave,Localmin)

print(Local_minimum(object=['HD 161056'],Wave=3302.37)[0])


def velocity_calculation(object,Wave):
    Lobs=Local_minimum(object, Wave)[0]
    u=0
    c=299792458
    if Wave>Lobs :
        u=c*((Wave/Lobs)-1)
        shift='Blue shift'
    else :
        u=c*(1-(Wave/Lobs))        
        shift='Red shift'
    return 'Velocity in km/s :', u*1e-3, shift



v1=velocity_calculation(object=['HD 303308'], Wave=3302.37)

print(v1)


















