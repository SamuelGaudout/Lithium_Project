# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:27:54 2021

@author: Samuel
"""
import csv
import matplotlib.pyplot as plt

'''I use sys in order to find the files of EDIBLES code.
I'm a windows user, change the path written here by your own path (where the EDIBLES
code is saved). If you're using Linux ou Mac you can erase the two following lines'''
import sys
sys.path.insert(1,"/Users/Samuel/Desktop/Programs/ImportGithub")

from edibles.utils import edibles_oracle


pythia = edibles_oracle.EdiblesOracle()

print("Results from getObsListByWavelength: ")
wave=6707
List=pythia.getObsListByWavelength(wave=6707, MergedOnly=False, OrdersOnly=True)
print(List)

#List1=["/HD93843/RED_860/HD93843_w860_redl_20170427_O1.fits","/HD164073/RED_860/HD164073_w860_redl_20160913_O1.fits"]

obslist=open("Files_Lithium_6707A.txt","r")
filesInt=obslist.read()
#print(filesInt)

for filename in List:
    sp = edibles_oracle.EdiblesSpectrum(filename)
    #plt.figure()
    # plt.title(filename)
    plt.xlabel("Wavelength (" + r"$\AA$" + ")")
    plt.xlim(wave-5, wave+10)
    plt.ylim(-1000, 10000)
    #plt.plot(sp.wave, sp.flux, label=filename)
    plt.plot(sp.wave, sp.flux)
    #print(sp.flux)
    plt.show()
    #plt.legend()
    
'''All interesting files found by edibles_oracle, the list of the most interesting
files is into the Files_Lithium_6707A document'''







