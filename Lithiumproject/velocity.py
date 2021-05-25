import matplotlib.pyplot as plt
import csv

from edibles.utils import edibles_oracle



List1=[]
with open("Nfiles/test_velocity.txt","r") as files:
    for l in files:
        List1.append(l)

List=[]
for l in List1:
    p=l.replace('\n', '')
    List.append(p)
print(List)

#L1=[List[0],List[1],List[11]]
L1=['/HD154368/RED_564/HD154368_w564_redu_20180630_O5.fits'] #sodium lines
L1=['/HD63804/RED_564/HD63804_w564_redu_20190203_O5.fits']
L1=['/HD63804/BLUE_346/HD63804_w346_blue_20190204_O12.fits']
L1=['/HD161056/BLUE_346/HD161056_w346_blue_20170701_O11.fits']

for filename in L1:
    sp = edibles_oracle.EdiblesSpectrum(filename)
    fluxN=[]
    wa=[]
    for i in sp.flux:
        #i=i/(sp.flux[2869]) #normalization
        fluxN.append(i)
    for o in sp.wave:
        wa.append(o)
    #print(fluxN)
    plt.xlabel("Wavelength (" + r"$\AA$" + ")")
    plt.ylabel('Flux')
    plt.plot(sp.wave, fluxN, label=filename, fillstyle='none',color='black')
    
# plt.axvline(x=6707.95, linestyle='--', color='grey')
# plt.ylim((-2000,6000))
#plt.xlim((5885,5900))
plt.show()
plt.legend()
with open('Obslist.csv','w',newline='') as f:  
    ecrire=csv.writer(f)
    
    for i in range(len(fluxN)):                           
        ecrire.writerow((str(wa[i]),str(fluxN[i])))