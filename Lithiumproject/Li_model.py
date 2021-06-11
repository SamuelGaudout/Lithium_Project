import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from edibles.models import ContinuumModel, VoigtModel
from edibles.utils.edibles_spectrum import EdiblesSpectrum
from edibles.utils import edibles_oracle


def fit_LiI_Lines(target, date):
    """A function to fit Li I doublet lines 
    
    7LiI_1 = 6707.761
    7LiI_2 = 6707.912
    
    """
    wavelength = 6708

    pythia = edibles_oracle.EdiblesOracle()
    Lilist = pythia.getObsListByWavelength(wavelength, OrdersOnly=True)

    files = []
    for filename in Lilist:
        if target in filename:
            if date in filename:
                files.append(filename)
    
    print(files)
    sp = EdiblesSpectrum(files[0])
    print(sp.target)
    sp.getSpectrum(xmin=6707, xmax=6709)
    
    sigma = np.std(sp.flux)
    prominence = sigma
    peaks, _ = find_peaks(-sp.flux, prominence=prominence)
    peak_wavelengths = [sp.wave[i] for i in peaks]
    print(peak_wavelengths)
    
    # #########################################################################

    cont = ContinuumModel(n_anchors=4)
    cont_pars = cont.guess(sp.flux, x=sp.wave)
    
    # #########################################################################

    voigt1 = VoigtModel(prefix='v1_')
    voigt1_pars = voigt1.guess(sp.flux, x=sp.wave)

    # #########################################################################

    voigt2 = VoigtModel(prefix='v2_')
    voigt2_pars = voigt2.make_params(lam_0=peak_wavelengths[1], b=1, d=0.001, tau_0=0.01)

    voigt2_pars['v2_lam_0'].set(expr='v1_lam_0 + 0.151')
    voigt2_pars['v2_b'].set(expr='v1_b')

    # #########################################################################

    model = cont * voigt1 * voigt2
    pars = cont_pars + voigt1_pars + voigt2_pars
    
       
    # #########################################################################
    
    result = model.fit(data=sp.flux, params=pars, x=sp.wave)
    
    comps=result.eval_components(x=sp.wave)
    result_cont=cont.fit(data=sp.flux, params=result.params, x=sp.wave)
    
    #print(comps['cont'])
    
     # #########################################################################
    'normalization'
    fluxN=[]
    for i in range(len(sp.flux)):
        fluxN.append(sp.flux[i]/comps['cont'])
    
    bestfitN=[]
    for i in range(len(sp.flux)):
        bestfitN.append(result.best_fit[i]/comps['cont'])
    
    # #########################################################################

    #result.params.pretty_print()
    #print('Ratio: ', result.params['v1_tau_0'] / result.params['v2_tau_0'])
    #print(result.fit_report())
    # #########################################################################
    
    resi=[]
    for i in range(len(sp.flux)):
        a=result.best_fit[i]-sp.flux[i]
        resi.append(a + result_cont.best_fit[i])
    
    print(result.fit_report())
    print(result)
    #result.plot_fit()
    plt.plot(sp.wave, result_cont.best_fit, label='First continuum', color='green')
    plt.plot(sp.wave, comps['cont'], label='Best continuum', color='blue')
    
    plt.plot(sp.wave,sp.flux, marker='D',fillstyle='none',color='black',label='Data')
    # plt.plot(sp.wave, result.best_fit, color='orange', label='lm_fit')
    plt.title('Li I 6708')
    plt.legend()

    plt.figure()
    plt.plot(sp.wave,sp.flux,marker='D',fillstyle='none',color='black',label='Data')
    plt.plot(sp.wave, result.best_fit, color='orange', label='lm_fit')
    #plt.plot(sp.wave, (-result.best_fit+sp.flux)/comps['cont'] +1, color='blue', label='Residual Flux')
    plt.legend()

    return(result.best_fit, comps['cont'])


if __name__ == "__main__":
    
    fil=['HD63804','HD147084','HD147084','HD147889','HD147889']
    dates=['20190204','20160403','20160419','20160807','20160728']
    fil=['HD147889','HD147889']
    dates = ['20160728','20160807']
    fil=['HD147889']
    dates=['20160807']
    
    
    for i in range(len(fil)):
        plt.figure()
        fit_LiI_Lines(target=fil[i], date=dates[i])[1]
    
    





