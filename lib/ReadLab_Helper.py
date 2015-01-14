import fileinput

import numpy as N
from pandas import read_table
from scipy.optimize import curve_fit


__author__ = 'rened'

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


class Read_LabviewTxT():
    """"""
    def __init__(self,filename,timestep=0.,delimiter='\t'):

        self.datarray = []
        self.timearray = []
        self.filename = filename
        self.timestep = timestep
        self.bin =[]
        self.edges = []
        self.P0 = 0.
        self.Pmax =0.
        self.P0_offset = 0.2
        self.delimiter = delimiter

        """ Daten_lesen """
        self.datarray, self.timearray = self.OpenFile(filename,timestep)
        self.popt, self.pcov = curve_fit(fitfunc_logist, self.timearray, self.datarray,maxfev = 8000,ftol=0.49012e-09)
        # self.fit_data()



    def OpenFile(self,filename,timestep=0.):

        '''Baut das File direkt um wegen US/DE '''
        for line in fileinput.FileInput(filename, inplace=1):
            line=line.replace(',','.')
            line=line.replace('\n','')
            print line

        ''' delimiter skriprow, skip_footer noch in der Klasse implementieren
            orginale Zeitreihe und Druckreihe abrufbar machen '''
        data_frame = read_table(filename,self.delimiter,names=['Zeit','Druck'],skiprows=7,skip_footer=7)
        dat_Num1 = data_frame['Druck'].astype(float)

        ''' Das P0 aus den ersten 10% der Messdaten mitteln
            Umrechnung auf Startdruck = 0bar somit bar '''

        P10 = int(N.size(dat_Num1)*0.1)
        self.P0 = N.mean(dat_Num1[1:P10])

        ''' alles was kleiner als 0.1 bar ist nicht betrachten'''
        wo = N.where((dat_Num1-self.P0) > self.P0_offset)[0][0]
        dat_Num1 = dat_Num1[wo:-1]

        ''' Nur bis zuimport numpym maximalen Druck*0.995 anzeigen '''
        wo = N.where(dat_Num1 > (dat_Num1.max()*0.995))[0][0]
        dat_Num1 = dat_Num1[1:wo]

        ''' Zeitachse noch trimmen'''
        if timestep==0.:
            timestep = N.mean(N.diff(data_frame['Zeit'].astype(float)))

        self.Pmax=N.max(data_frame['Druck'].astype(float))-self.P0

        return dat_Num1-self.P0-self.P0_offset, N.arange(N.size(dat_Num1))*self.timestep

        """Constructor for Read_LabviewTxT"""