# Play with the function signature so the no. of components can be flexible
# It keeps saying "b_CLoud1" for some reason I don't understand.... But it works.


import numpy as np
import inspect
import collections
from scipy.interpolate import CubicSpline
from edibles.models import ContinuumModel
from lmfit import Model
from lmfit.models import update_param_vals
from edibles.utils.voigt_profile import voigt_absorption_line


class IsotopicLiModel(Model):
    def __init__(self, independent_vars=["x"], prefix="", nan_policy="raise", **kwargs):


        kwargs.update({"prefix": prefix,
                       "nan_policy": nan_policy,
                       "independent_vars": independent_vars})

        self.b_names7 = ["b_Cloud7Li"]
        self.N_names7 = ["N_Cloud7Li"]
        self.b_names6 = ["b_Cloud6Li"]
        self.N_names6 = ["N_Cloud6Li"]
        self.V_names = ["V_off_Cloud"]
        kwargs["param_names"] = self.b_names7 + self.N_names7+ self.b_names6 + self.N_names6 + self.V_names


        params = {}
        for name in kwargs["param_names"]:
            if name[0] == "b":
                params[name] = 1.0
            if name[0] == "N":
                params[name] = 1.0
            if name[0] == "V":
                params[name] = 0.0

        
        def calcLiIsotop(x, b_Cloud7Li=1.0,b_Cloud6Li=1.0, N_Cloud7Li=1.0, N_Cloud6Li=1.0, V_off_Cloud=0.0, **kwargs):
            lambda0 = [6707.761, 6707.912, 6707.921, 6708.072] 
            f = [4.982e-01, 2.491e-01, 4.982e-01, 2.491e-01] 
            gamma = [3.689e7, 3.689e7, 3.689e7, 3.689e7]
            N_mag = 9.0
            v_resolution = 3.0

            # parse parameters
            bs = [b_Cloud7Li]*2 + [b_Cloud6Li]*2
            Ns = [N_Cloud7Li * 10**N_mag]*2 + [N_Cloud6Li * 10**N_mag]*2
            V_offs = [V_off_Cloud]*4
            # just something to print so we know it's working...
            print("Cloud velocities at:", np.unique(V_offs))
            #print(kwargs.keys())
            
            for name in kwargs.keys():
                if name[0] == "b":
                    #print(name) # will be popped up as Cloud idx??
                    bs = bs + [kwargs[name]]*4
                if name[0] == "N":
                    Ns = Ns + [kwargs[name] * 10**N_mag]*4
                if name[0] == "V":
                    V_offs = V_offs + [kwargs[name]]*4
            #print(bs)
            # no problem for convolution since we only call voigt_absorption_line once.
            flux = voigt_absorption_line(
                x,
                lambda0=lambda0,
                b=bs,
                N=Ns,
                f=f,
                gamma=gamma,
                v_rad=V_offs,
                v_resolution=v_resolution,
            )

            return flux

        # play with the signature of the calculation function
        # I don't really understand what is happening...
        sig = inspect.signature(calcLiIsotop)
        base_b7Li = inspect.signature(calcLiIsotop).parameters["b_Cloud7Li"]
        base_b6Li = inspect.signature(calcLiIsotop).parameters["b_Cloud6Li"]
        base_N7Li = inspect.signature(calcLiIsotop).parameters["N_Cloud7Li"]
        base_N6Li = inspect.signature(calcLiIsotop).parameters["N_Cloud6Li"]
        base_V_off = inspect.signature(calcLiIsotop).parameters["V_off_Cloud"]

        d = {'x': sig.parameters['x']}
       
        
        b_key7 = "b_Cloud7Li" 
        b_val7 = base_b7Li.replace(name=b_key7)
        d[b_key7] = b_val7

        N_key7 = "N_Cloud7Li" 
        N_val7 = base_N7Li.replace(name=N_key7)
        d[N_key7] = N_val7
            
        b_key6 = "b_Cloud6Li" 
        b_val6 = base_b6Li.replace(name=b_key6)
        d[b_key6] = b_val6

        N_key6 = "N_Cloud6Li" 
        N_val6 = base_N6Li.replace(name=N_key6)
        d[N_key6] = N_val6

        V_off_key = "V_off_Cloud" 
        V_off_val = base_V_off.replace(name=V_off_key)
        d[V_off_key] = V_off_val

        d = collections.OrderedDict(d)
        calcLiIsotop.__signature__ = sig.replace(parameters=tuple(d.values()))

        super().__init__(calcLiIsotop, **kwargs)

    def guess(self, V_off=[0.0], **kwargs):
        # For now just type in V_off but we can include v_correlation in the future

        
        pars = self.make_params()
        for i, v in enumerate(V_off):
            pars["b_Cloud7Li"].set(value=1.0, min=0, max=10)
            pars["N_Cloud7Li"].set(value=1.0, min=0, max=1000)
            pars["b_Cloud6Li"].set(value=1.0, min=0, max=10)
            pars["N_Cloud6Li"].set(value=1.0, min=0, max=1000)
            pars["V_off_Cloud"].set(value=v, min=-50, max=50)
            # if we have better estimate on v, consider using v pm 15 as min and max

        return update_param_vals(pars, self.prefix, **kwargs)


if __name__ == "__main__":
    from edibles.utils.edibles_oracle import EdiblesOracle
    from edibles.utils.edibles_spectrum import EdiblesSpectrum
    import matplotlib.pyplot as plt

    pythia = EdiblesOracle()

    
    List = pythia.getFilteredObsList(object=["HD 186745"], OrdersOnly=True, Wave=6708.0)
    test = List.values.tolist()
    filename = test[0]
    print("=="*15)
    print(filename)
    print("==" * 15)
    wrange = [6707.3, 6707.9]
    sp = EdiblesSpectrum(filename)
    wave, flux = sp.bary_wave, sp.flux
    idx = np.where((wave > wrange[0]) & (wave < wrange[1]))
    wave, flux = wave[idx], flux[idx]
    flux = flux / np.median(flux)

       
    print("\n"*3)
    print("="*20)
    print("with continuum")
    
    cont = ContinuumModel(n_anchors=4)
    cont_pars =  cont.guess(data=flux, x=wave)
    
    isotop = IsotopicLiModel()
    isotop_pars = isotop.guess(V_off = [-10])
    
    
    model = isotop * cont
    pars = isotop_pars + cont_pars
    
    result = model.fit(data=flux, params=pars, x=wave)
    #result1 = isotop.fit(data=flux, params=isotop_pars, x=wave)
    
    comps=result.eval_components(x=wave)
    
    plt.plot(wave, flux, label="Data", marker='D',fillstyle='none',color='black')
    plt.plot(wave, comps['cont'], label='continuum', color='green')
    plt.plot(wave, model.eval(params=result.params, x=wave), label="With continuum",marker='*')
    #plt.plot(wave, isotop.eval(params=result1.params, x=wave), label='Without continuum', marker='*')
    plt.title(filename)
    plt.xlabel('Wavelenght $\AA$')
    plt.legend()

    print(result.fit_report())
    
    print("\n"*3)
    print("="*20)
    print("without continuum")
    
    #print(result1.fit_report())




    

