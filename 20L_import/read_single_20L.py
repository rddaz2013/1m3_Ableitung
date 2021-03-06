# coding=utf-8
'''
Created on 26.07.2012
Dieses Programm ist fuer alten Labview txt-export daten 
@author: rene
'''

import matplotlib.pyplot as plt

from lib.ReadLab_Helper import *

Versuchname = ' 20L'
filename = '250g/m3'
dd = Read_20LTxT('data/20L_Example/250.txt', timestep=0.001)

x = dd.OpenFile('data/20L_Example/250.txt')

time_start = x.index[(x['Druck1'] > 0.) & (x['Druck2'] > 0)][1]
druck1_max = x['Druck1'].max()
druck2_max = x['Druck2'].max()

druck_end = x.index[(x['Druck1'] > druck1_max * 0.99) & (x['Druck2'] > druck2_max * 0.99)][1]

print x[time_start:druck_end]

plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck1'][time_start:druck_end + 15])
plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck2'][time_start:druck_end + 15])

x = dd.OpenFile('data/20L_Example/1000.txt')

time_start = x.index[(x['Druck1'] > 0.) & (x['Druck2'] > 0)][1]

druck1_max = x['Druck1'].max()
druck2_max = x['Druck2'].max()

druck_end = x.index[(x['Druck1'] > druck1_max * 0.95) & (x['Druck2'] > druck2_max * 0.95)][1]

plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck1'][time_start:druck_end + 15])
plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck2'][time_start:druck_end + 15])

x = dd.OpenFile('data/20L_Example/500.txt')

time_start = x.index[(x['Druck1'] > 0.) & (x['Druck2'] > 0)][1]

druck1_max = x['Druck1'].max()
druck2_max = x['Druck2'].max()

druck_end = x.index[(x['Druck1'] > druck1_max * 0.95) & (x['Druck2'] > druck2_max * 0.95)][1]

plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck1'][time_start:druck_end + 15])
plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck2'][time_start:druck_end + 15])

x = dd.OpenFile('data/20L_Example/1750.txt')

time_start = x.index[(x['Druck1'] > 0.) & (x['Druck2'] > 0)][1]

druck1_max = x['Druck1'].max()
druck2_max = x['Druck2'].max()

druck_end = x.index[(x['Druck1'] > druck1_max * 0.95) & (x['Druck2'] > druck2_max * 0.95)][1]

plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck1'][time_start:druck_end + 15])
plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck2'][time_start:druck_end + 15])

x = dd.OpenFile('data/20L_Example/2000.txt')

time_start = x.index[(x['Druck1'] > 0.) & (x['Druck2'] > 0)][1]

druck1_max = x['Druck1'].max()
druck2_max = x['Druck2'].max()

druck_end = x.index[(x['Druck1'] > druck1_max * 0.95) & (x['Druck2'] > druck2_max * 0.95)][1]

plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck1'][time_start:druck_end + 15])
plt.plot(x['Zeit'][time_start:druck_end + 15], x['Druck2'][time_start:druck_end + 15])
# popt,pcov = dd.Calc()

#dat_Num = dd.datarray
#zeit_achse = dd.timearray

#max_value = dat_Num.max()
#mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

#plt.subplot(211)
#xdata = np.linspace(0, N.max(mat[:,0]), 100)
#plt.plot(mat[:,0],mat[:,1])
#plt.plot(xdata,fitfunc_logist(xdata,popt[0],popt[1],popt[2]),'+')
#plt.ylabel(r"Druck [bar]", fontsize = 12)

#text_fr= 'Parameters \n G : %3.4f\n k : %3.4f\n c : %3.4f\n'%(popt[0],popt[1],popt[2])
#plt.text(N.max(zeit_achse)*0.1,max_value*0.5,text_fr)
#plt.text(N.max(zeit_achse)*0.7,max_value*0.2,r'$f(t)=G\cdot \frac { 1 }{ 1+{ e }^{ -kGt-c } } $',fontsize=18)
#plt.title(Versuchname + ' // ' + filename)

#print  N.sqrt(N.diag(pcov))


#ableitung = fitfunc_logist_dt(xdata,popt[0],popt[1],popt[2])

#plt.subplot(212)
#hist, bin_edges = N.histogram(ableitung, bins=60,normed=0)
#plt.plot(xdata,ableitung,'o')
#text_fr= u'Parameters \n bar/s_max : %3.4f\n barü_max : %3.4f\n P0 : %3.4f'%(N.max(ableitung),dd.Pmax,dd.P0)
#plt.text(N.max(zeit_achse)*0.1,N.max(ableitung)*0.5,text_fr)
#plt.xlabel(r"Time [s]", fontsize = 12)
#plt.ylabel(r"Druck [bar/s]", fontsize = 12)
#savefig(filename+'.png', bbox_inches='tight')
plt.show()
