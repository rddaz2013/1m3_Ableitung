# coding=utf-8
'''
Created on 26.07.2012
Dieses Programm ist fuer alten Labview txt-export daten 
@author: rene
'''

import fileinput

import numpy as N
from pandas import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class Read_LabviewTxT(object):
    """"""
    def __init__(self,filename,timestep=0.):
        self.filename = filename
        self.timearray = []
        self.timestep = timestep
        self.datarray = []
        self.popt = []
        self.pcov = []
        self.bin =[]
        self.edges = []

        """ Daten_lesen """
        self.datarray, self.timearray = self.OpenFile(filename,timestep)
        self.popt, self.pcov = curve_fit(fitfunc_logist, self.timearray, self.datarray,maxfev = 6000,ftol=0.49012e-09)


    def OpenFile(self,filename,timestep=0.):

        '''Baut das File direkt um wegen US/DE '''
        for line in fileinput.FileInput(filename, inplace=1):
            line=line.replace(',','.')
            line=line.replace('\n','')
            print line

        data_frame = read_table(filename,delimiter='\t',names=['Zeit','Druck'],skiprows=5,skip_footer=7)
        dat_Num1 = data_frame['Druck'].astype(float)

        ''' alles was kleiner als 0.25 bar ist nicht betrachten'''
        wo = np.where(dat_Num1 > 0.25)[0][0]
        dat_Num1 = dat_Num1[wo:-1]

        wo = np.where(dat_Num1 > (dat_Num1.max()*0.997))[0][0]
        ''' Nur bis zum maximalen Druck*0.995 anzeigen '''
        dat_Num1 = dat_Num1[1:wo]

        ''' Zeitachse noch trimmen'''
        if timestep==0.:
            timestep = N.mean(N.diff(data_frame['Zeit'].astype(float)))

        return dat_Num1, N.arange(N.size(dat_Num1))*timestep

        """Constructor for Read_LabviewTxT"""


def fitfunc_logist(x,k,c,G):
    '''  Dient zum Anpassen der Parameter k,c,G auf die Druck/Zeit Kurve von Explosionsdruckverlaeufen
    fuer die Logistik Funktion
    :param x: Zeitachse
    :param k: Faktor
    :param c: entspricht maximaler Druck
    :param G: Faktor
    :return: Funktionwert
    '''
    return G*(1./(1.+N.exp(-k*G*x-c)))

def fitfunc_logist_dt(x,k,c,G):
    ''' Dient zum Berechnen der Ableitung bei gegeben x,k,c,G

    :param x: Zeitachse
    :param k: Faktor
    :param c: entspricht maximaler Druck
    :param G: Faktor
    :return:
    '''
    return k*fitfunc_logist(x,k,c,G)*(G-fitfunc_logist(x,k,c,G))

dd = Read_LabviewTxT('Caro2014__750g_12.txt',timestep=0.002)

dat_Num = dd.datarray
zeit_achse = dd.timearray

popt = dd.popt
pcov = dd.pcov

max_value = dat_Num.max()
mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

plt.subplot(211)
plt.plot(mat[:,0],mat[:,1])
plt.plot(mat[:,0],fitfunc_logist(mat[:,0],popt[0],popt[1],popt[2]),'+')
plt.ylabel(r"Druck [bar]", fontsize = 12)

text_fr= 'Parameters \n G : %3.4f\n k : %3.4f\n c : %3.4f\n'%(popt[0],popt[1],popt[2])
plt.text(0.003,max_value*0.5,text_fr)
plt.text(N.max(zeit_achse)*0.7,max_value*0.2,r'$f(t)=G\cdot \frac { 1 }{ 1+{ e }^{ -kGt-c } } $',fontsize=18)
plt.title(u'Sigmoidfunktion')

print  N.sqrt(N.diag(pcov))

xdata = np.linspace(0, N.max(mat[:,0]), 60)
ableitung = fitfunc_logist_dt(xdata,popt[0],popt[1],popt[2])

plt.subplot(212)
hist, bin_edges = N.histogram(ableitung, bins=60,normed=0)
#print hist
anzahl_mon = N.cumsum(hist)+0.
max_mon = N.max(anzahl_mon)+0.
pro = 1.
pro = anzahl_mon/max_mon
print N.size(pro)
print N.size(bin_edges)
plt.plot(xdata,ableitung,'o')
plt.xlabel(r"Time [s]", fontsize = 12)
plt.ylabel(r"Druck [bar/s]", fontsize = 12)
plt.show()