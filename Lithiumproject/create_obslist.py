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


List1=[]
with open("Files_Lithium_6707A.txt","r") as files:
    for l in files:
        List1.append(l)

List=[]
for l in List1:
    p=l.replace('\n', '')
    List.append(p)
print(List)

for filename in List:
    sp = edibles_oracle.EdiblesSpectrum(filename)
    #plt.figure()
    # plt.title(filename)
    plt.xlabel("Wavelength (" + r"$\AA$" + ")")
    plt.xlim(wave-5, wave+10)
    plt.ylim(-1000, 10000)
    plt.plot(sp.wave, sp.flux, label=filename)
    #plt.plot(sp.wave, sp.flux)
    print(sp.flux)
    plt.show()
    plt.legend()
        
#############################################################################
'Normalize'

L1=[List[0],List[1],List[11]]
#L1=[List[12]]
plt.figure()
for filename in L1:
    sp = edibles_oracle.EdiblesSpectrum(filename)
    fluxN=[]
    wa=[]
    for i in sp.flux:
        i=i/(sp.flux[2869])
        fluxN.append(i)
    for o in sp.wave:
        wa.append(o)
    #print(fluxN)
    plt.xlabel("Wavelength (" + r"$\AA$" + ")")
    plt.plot(sp.wave, fluxN, label=filename)

plt.axvline(x=6707.95)
plt.show()
plt.legend()   

with open('Obslist.csv','w',newline='') as f:  
    ecrire=csv.writer(f)
    
    for i in range(len(fluxN)):                           
        ecrire.writerow((str(wa[i]),str(fluxN[i])))
    
    
    
    
    
    
    
    
    
    
    

