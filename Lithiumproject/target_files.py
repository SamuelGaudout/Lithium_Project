# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:35:44 2021

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



List1=[]
with open("Files_Lithium_6707A.txt","r") as files:
    for l in files:
        List1.append(l)

List=[]
for l in List1:
    p=l.replace('\n', '')
    List.append(p)
print(List)

L1=[List[0],List[1],List[11]]
#L1=[List[12]]

for filename in L1:
    sp = edibles_oracle.EdiblesSpectrum(filename)
    fluxN=[]
    wa=[]
    for i in sp.flux:
        i=i/(sp.flux[2869]) #normalization
        fluxN.append(i)
    for o in sp.wave:
        wa.append(o)
    #print(fluxN)
    plt.xlabel("Wavelength (" + r"$\AA$" + ")")
    plt.plot(sp.wave, fluxN, label=filename)
    
plt.axvline(x=6707.95, linestyle='--', color='grey')
plt.ylim((0.97,1.03))
plt.xlim((6705,6712))
plt.show()
plt.legend()   

with open('Obslist.csv','w',newline='') as f:  
    ecrire=csv.writer(f)
    
    for i in range(len(fluxN)):                           
        ecrire.writerow((str(wa[i]),str(fluxN[i])))