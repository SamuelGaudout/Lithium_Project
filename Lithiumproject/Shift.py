import csv
import matplotlib.pyplot as plt

from edibles.utils import edibles_oracle



List1=[]
with open("Files_Lithium_6707A.txt","r") as files:
    for l in files:
        List1.append(l)

List=[]
for l in List1:
    p=l.replace('\n', '')
    List.append(p)

L1=[List[3]]
print(L1)

u=(0,18.8)


for filename in L1:
    sp = edibles_oracle.EdiblesSpectrum(filename)
    fluxN=[]
    wa0=[]
    wa1=[]
    for i in sp.flux:
        i=i/(sp.flux[2869]) #normalization
        fluxN.append(i)
    for o in sp.wave:
        a=o/(1+(u[0]/299792.458))
        b=o/(1+(u[1]/299792.458))
        wa0.append(a)
        wa1.append(b)
    #print(fluxN)
    plt.xlabel("Wavelength (" + r"$\AA$" + ")")
    plt.plot(wa1, fluxN, label=filename, marker='D',fillstyle='none', color='black')
    # plt.plot(wa1, fluxN)

    
    
plt.axvline(x=6707.912, linestyle='--', color='grey')
plt.axvline(x=6707.761, linestyle='--', color='grey')
plt.ylim((0.97,1.03))
plt.xlim((6705,6712))
plt.title('Before correction')
plt.show()
plt.legend()   

with open('Obslist.csv','w',newline='') as f:  
    ecrire=csv.writer(f)
    
    for i in range(len(fluxN)):                           
        ecrire.writerow((str(wa0[i]),str(fluxN[i])))