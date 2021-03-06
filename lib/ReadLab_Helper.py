import fileinput

from matplotlib import pyplot as plt
import numpy as N
from pandas import read_table
from scipy import interpolate
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
        self.P0_offset = 0.10
        self.delimiter = delimiter
        self.temp_kst = 0.

    def Calc(self):

        """ Daten_lesen """
        self.datarray, self.timearray = self.OpenFile(self.filename,self.timestep)
        self.popt, self.pcov = curve_fit(fitfunc_logist, self.timearray, self.datarray, maxfev=19000, ftol=0.89012e-09)
        self.temp_kst = N.max(fitfunc_logist_dt(self.timearray, self.popt[0], self.popt[1], self.popt[2]))
        return self.popt,self.pcov,self.temp_kst
        # self.fit_data()



    def OpenFile(self,filename,timestep=0.):

        '''Baut das File direkt um wegen US/DE '''
        for line in fileinput.FileInput(filename, inplace=1):
            line=line.replace(',','.')
            line=line.replace('\n','')
            print line

        ''' delimiter skriprow, skip_footer noch in der Klasse implementieren
            orginale Zeitreihe und Druckreihe abrufbar machen '''
        data_frame = read_table(filename,self.delimiter,names=['Zeit','Druck'],skiprows=7,skip_footer=7,engine='python')
        dat_Num1 = data_frame['Druck'].astype(float)

        ''' Das P0 aus den ersten 10% der Messdaten mitteln
            Umrechnung auf Startdruck = 0bar somit bar '''

        P10 = int(N.size(dat_Num1)*0.1)
        self.P0 = N.mean(dat_Num1[1:P10])

        ''' alles was kleiner als 0.1 bar ist nicht betrachten'''
        wo = N.where((dat_Num1-self.P0) > self.P0_offset)[0][0]
        dat_Num1 = dat_Num1[wo:-1]

        ''' Nur bis zuimport numpym maximalen Druck*0.995 anzeigen '''
        wo = N.where(dat_Num1 > (dat_Num1.max() * 0.998))[0][0]
        dat_Num1 = dat_Num1[1:wo]

        ''' Zeitachse noch trimmen'''
        if timestep==0.:
            timestep = N.mean(N.diff(data_frame['Zeit'].astype(float)))

        self.Pmax=N.max(data_frame['Druck'].astype(float))-self.P0

        return dat_Num1-self.P0-self.P0_offset, N.arange(N.size(dat_Num1))*self.timestep

        """Constructor for Read_LabviewTxT"""


class Read_20LTxT():
    """"""

    def __init__(self, filename, timestep=0., delimiter=';'):
        self.datarray = []
        self.timearray = []
        self.filename = filename
        self.timestep = timestep
        self.bin = []
        self.edges = []
        self.P0 = 0.
        self.Pmax = 0.
        self.P0_offset = 0.1
        self.delimiter = delimiter

    def Calc(self):
        """ Daten_lesen """
        self.datarray, self.timearray = self.OpenFile(self.filename, self.timestep)
        self.popt, self.pcov = curve_fit(fitfunc_logist, self.timearray, self.datarray, maxfev=8000, ftol=0.49012e-09)
        return self.popt, self.pcov
        # self.fit_data()


    def OpenFile(self, filename, timestep=0.):
        '''Baut das File direkt um wegen US/DE '''
        for line in fileinput.FileInput(filename, inplace=1):
            line = line.replace(',', '.')
            line = line.replace('\n', '')
            print line

        ''' delimiter skriprow, skip_footer noch in der Klasse implementieren
            orginale Zeitreihe und Druckreihe abrufbar machen '''
        data_frame = read_table(filename, self.delimiter, names=['Zeit', 'Druck1', 'Druck2'], skiprows=7, skip_footer=7)

        dat_Zeit = data_frame['Zeit'].astype(float)
        dat_Num1 = data_frame['Druck1'].astype(float)
        dat_Num2 = data_frame['Druck2'].astype(float)

        ''' Das P0 aus den ersten 10% der Messdaten mitteln
            Umrechnung auf Startdruck = 0bar somit bar '''

        # P10 = int(N.size(dat_Num1)*0.1)
        #self.P0 = N.mean(dat_Num1[1:P10])

        ''' alles was kleiner als 0.1 bar ist nicht betrachten'''
        #wo = N.where((dat_Num1-self.P0) > self.P0_offset)[0][0]
        #dat_Num1 = dat_Num1[wo:-1]

        ''' Nur bis zuimport numpym maximalen Druck*0.995 anzeigen '''
        #wo = N.where(dat_Num1 > (dat_Num1.max() * 0.998))[0][0]
        #dat_Num1 = dat_Num1[1:wo]

        ''' Zeitachse noch trimmen'''
        #if timestep==0.:
        #    timestep = N.mean(N.diff(data_frame['Zeit'].astype(float)))

        #self.Pmax=N.max(data_frame['Druck'].astype(float))-self.P0



        #return dat_Num1-self.P0-self.P0_offset, N.arange(N.size(dat_Num1))*self.timestep
        return data_frame
        """Constructor for Read_LabviewTxT"""


def draw_tangent(x, y, a):
    # interpolate the data with a spline
    spl = interpolate.splrep(y, x)
    small_t = N.linspace(a - (a / 20), a + (a / 20), num=5)
    fa = interpolate.splev(a, spl, der=0)  # f(a)
    fprime = interpolate.splev(a, spl, der=1)  # f'(a)
    tan = fa + (fprime * (small_t - a))  # tangent

    plt.plot(a, fa, 'om')
    plt.plot(small_t, tan, '--r', lw=3)  #
    return fprime
