# Play with the function signature so the no. of components can be flexible
# It keeps saying "b_CLoud1" for some reason I don't understand.... But it works.


import numpy as np
import inspect
import collections
from scipy.interpolate import CubicSpline
from lmfit import Model
from lmfit.models import update_param_vals
from edibles.utils.voigt_profile import voigt_absorption_line


class multiNaModel(Model):
    def __init__(self, n_components, independent_vars=["x"], prefix="", nan_policy="raise", **kwargs):

        if not isinstance(n_components, int):
            raise TypeError("n_components (%.1f) must be an integer!" % n_components)
        self.n_components = n_components

        kwargs.update({"prefix": prefix,
                       "nan_policy": nan_policy,
                       "independent_vars": independent_vars})

        self.b_names = ["b_Cloud%i" % (i) for i in range(n_components)]
        self.N_names = ["N_Cloud%i" % (i) for i in range(n_components)]
        self.V_names = ["V_off_Cloud%i" % (i) for i in range(n_components)]
        kwargs["param_names"] = self.b_names + self.N_names + self.V_names


        params = {}
        for name in kwargs["param_names"]:
            if name[0] == "b":
                params[name] = 1.0
            if name[0] == "N":
                params[name] = 1.0
            if name[0] == "V":
                params[name] = 0.0

        # Other than the default parameters from Cloud0, other parameters are passed in kwargs
        def calcMultiNa(x, b_Cloud0=1.0, N_Cloud0=1.0, V_off_Cloud0=0.0, **kwargs):
            lambda0 = [6707.761, 6707.912, 6707.921, 6708.072] * self.n_components
            f = [4.982e-01, 2.491e-01, 4.982e-01, 2.491e-01] * self.n_components
            gamma = [6.280e7, 6.280e7, 6.280e7, 6.280e7] * self.n_components
            N_mag = 9.0
            v_resolution = 3.0

            # parse parameters
            bs = [b_Cloud0]*4
            Ns = [N_Cloud0 * 10**N_mag]*4
            V_offs = [V_off_Cloud0]*4
            # just something to print so we know it's working...
            #print("Cloud velocities at:", np.unique(V_offs))
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
        sig = inspect.signature(calcMultiNa)
        base_b = inspect.signature(calcMultiNa).parameters["b_Cloud0"]
        base_N = inspect.signature(calcMultiNa).parameters["N_Cloud0"]
        base_V_off = inspect.signature(calcMultiNa).parameters["V_off_Cloud0"]

        d = {'x': sig.parameters['x']}
        for i in range(n_components):
            b_key = "b_Cloud" + str(i)
            b_val = base_b.replace(name=b_key)
            d[b_key] = b_val

            N_key = "N_Cloud" + str(i)
            N_val = base_N.replace(name=N_key)
            d[N_key] = N_val

            V_off_key = "V_off_Cloud" + str(i)
            V_off_val = base_V_off.replace(name=V_off_key)
            d[V_off_key] = V_off_val

        d = collections.OrderedDict(d)
        calcMultiNa.__signature__ = sig.replace(parameters=tuple(d.values()))

        super().__init__(calcMultiNa, **kwargs)

    def guess(self, V_off=[0.0], **kwargs):
        # For now just type in V_off but we can include v_correlation in the future

        assert len(V_off) == self.n_components, "Number of components do not match."

        pars = self.make_params()
        for i, v in enumerate(V_off):
            pars["%sb_Cloud%i" % (self.prefix, i)].set(value=1.0, min=0, max=10)
            pars["%sN_Cloud%i" % (self.prefix, i)].set(value=1.0, min=0, max=1000)
            pars["%sV_off_Cloud%i" % (self.prefix, i)].set(value=v, min=-50, max=50)
            # if we have better estimate on v, consider using v pm 15 as min and max

        return update_param_vals(pars, self.prefix, **kwargs)


if __name__ == "__main__":
    from edibles.utils.edibles_oracle import EdiblesOracle
    from edibles.utils.edibles_spectrum import EdiblesSpectrum
    import matplotlib.pyplot as plt

    pythia = EdiblesOracle()

    # data for 3300 segment
    List = pythia.getFilteredObsList(object=["HD 147889"], OrdersOnly=True, Wave=6708.0)
    test = List.values.tolist()
    filename = test[1]
    print("=="*15)
    print(filename)
    print("==" * 15)
    wrange = [6707, 6708.2]
    sp = EdiblesSpectrum(filename)
    wave1, flux1 = sp.bary_wave, sp.flux
    idx1 = np.where((wave1 > wrange[0]) & (wave1 < wrange[1]))
    wave1, flux1 = wave1[idx1], flux1[idx1]
    flux1 = flux1 / np.median(flux1)

    # data for 5900 segment
    List = pythia.getFilteredObsList(object=["HD 147889"], OrdersOnly=True, Wave=6708.0)
    test = List.values.tolist()
    filename = test[1]
    print("==" * 15)
    print(filename)
    print("==" * 15)
    wrange = [6707, 6708.2]
    sp = EdiblesSpectrum(filename)
    wave2, flux2 = sp.bary_wave, sp.flux
    idx2 = np.where((wave2 > wrange[0]) & (wave2 < wrange[1]))
    wave2, flux2 = wave2[idx2], flux2[idx2]
    flux2 = flux2 / np.median(flux2)

    # merge two segments to make data2fit
    wave = np.append(wave1, wave2)
    flux = np.append(flux1, flux2)

    # try single component first
    # we actually know the v_offs are roughly [-12, 4]
    print("\n"*3)
    print("="*20)
    print("Single component")

    model = multiNaModel(n_components=1)
    pars = model.guess(V_off = [-21])
    result = model.fit(data=flux, params=pars, x=wave)

    # output result in 2 panels to see detail
    fig = plt.figure(figsize=[8,3], dpi=200)
    ax = fig.add_subplot(1,2,1)
    ax.plot(wave1, flux1)
    ax.plot(wave1, model.eval(params=result.params, x=wave1))

    ax = fig.add_subplot(1,2,2)
    ax.plot(wave2, flux2)
    ax.plot(wave2, model.eval(params=result.params, x=wave2))
    plt.show()

    print(result.fit_report())

    # now double
    print("\n" * 3)
    print("=" * 20)
    print("Double components")

    model = multiNaModel(n_components=2)
    pars = model.guess(V_off=[-21,14])
    result = model.fit(data=flux, params=pars, x=wave)

    fig = plt.figure(figsize=[8, 3], dpi=200)
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(wave1, flux1)
    ax.plot(wave1, model.eval(params=result.params, x=wave1))

    ax = fig.add_subplot(1, 2, 2)
    ax.plot(wave2, flux2)
    ax.plot(wave2, model.eval(params=result.params, x=wave2))
    plt.show()

    print(result.fit_report())





    

