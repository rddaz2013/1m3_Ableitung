# coding=utf-8
"""
Created on 26.07.2012
Dieses Programm ist fuer alten Labview txt-export daten
@author: rene
"""

import glob

from pandas import *

from lib.ReadLab_Helper import *

Liste_Gewicht = []
Liste_Druck = []
Liste_Kst = []

for name in glob.glob('./data/Caro2014/*.txt'):
    dd = Read_LabviewTxT(name, timestep=0.002)
    popt,pcov = dd.Calc()

    dat_Num = dd.datarray
    zeit_achse = dd.timearray

    max_value = dat_Num.max()
    mat = N.column_stack((zeit_achse[:, N.newaxis], dat_Num[:, N.newaxis]))

    xdata = np.linspace(0, N.max(mat[:, 0]), 100)
    temp_kst = N.max(fitfunc_logist_dt(xdata, popt[0], popt[1], popt[2]))
    print name, N.max(dat_Num), temp_kst, popt
    temp_gewicht = float(name.split('/')[-1].replace('.txt', '').split('_')[2].replace('g', ''))

    plt.plot(xdata, fitfunc_logist(xdata, popt[0], popt[1], popt[2]), '+')
    Liste_Druck.append(N.max(dat_Num))
    Liste_Gewicht.append(temp_gewicht)
    Liste_Kst.append(temp_kst)

# plt.plot(Liste_Gewicht,Liste_Kst,'ro')
plt.show()


