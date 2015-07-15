# coding=utf-8
'''
Created on 26.07.2012
Dieses Programm ist fuer alten Labview txt-export daten 
@author: rene
'''

import glob
import re

import matplotlib.pyplot as plt
import pp


Liste_Gewicht = []
Liste_Druck = []
Liste_Kst = []
ppservers = ()


job_server = pp.Server(ppservers=ppservers)
print "Starting pp with", job_server.get_ncpus(), "workers"
ppservers = ()

# Jobliste füllen

def Calc2(name,timestep):
    from lib.ReadLab_Helper import Read_LabviewTxT
    dd = Read_LabviewTxT(name,timestep)
    return name,dd.Calc()

job_list = glob.glob('./data/Caro2015/*.txt')

jobs = []
timestep = 0.002

for name in job_list:
    #jobs.append(job_server.submit(Calc3, (name, timestep),(),modules=("",)))
    jobs.append(job_server.submit(Calc2, (name, timestep),(),modules=('lib.ReadLab_Helper',)))

job_server.print_stats()

#for job in jobs:
#    result = job()
#    if result:
#        break


for job in jobs:
    dateiname = job()[0]
    kst_max  = job()[1][2]
    max_P = job()[1][0][2]

    m = re.search("(V\d\d) (\d\d\d)g_\d",dateiname)

    if m:
        Versuch_Name = m.groups()[0]
        Gewicht = m.groups()[1]

    plt.plot([Gewicht],[kst_max],'ro',label=Versuch_Name)

    print Versuch_Name,Gewicht,max_P,kst_max

plt.show()
    #print job()[1]

'''for name in glob.glob('./data/Caro2014/*.txt'):
    dd = Read_LabviewTxT(name, timestep=0.002)

    dat_Num = dd.datarray
    zeit_achse = dd.timearray

    popt = dd.poptimport
    pcov = dd.pcov

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
plt.show()'''


