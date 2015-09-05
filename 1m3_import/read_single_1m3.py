# coding=utf-8
'''
Created on 26.07.2012
Dieses Programm ist fuer alten Labview txt-export daten 
@author: rene
'''

from pandas import *

from lib.ReadLab_Helper import *
from lib.ReadLab_Helper import draw_tangent


#filename = 'propan_1000hz_1_50L.txt'
#dd = Read_LabviewTxT('data/propan_1000hz_2_50L.txt', timestep=0.0013)

#popt,pcov,temp_Kst = dd.Calc()

#dat_Num = dd.datarray
#zeit_achse = dd.timearray

#max_value = dat_Num.max()
#mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

#plt.subplot(211)
#xdata = np.linspace(0, N.max(mat[:,0]), 200)
#plt.plot(mat[:,0],mat[:,1])
#plt.plot(xdata,fitfunc_logist(xdata,popt[0],popt[1],popt[2]),'+')
#plt.ylabel(r"Druck [bar]", fontsize = 12)

#text_fr= 'Parameters \n G : %3.4f\n k : %3.4f\n c : %3.4f\n'%(popt[0],popt[1],popt[2])
#plt.text(N.max(zeit_achse)*1.2,max_value*0.5,text_fr)
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
#plt.show()

Versuchname = ' Umbau'
filename = 'data/1m3_DeriveP/propan_500hz_1_50L.txt'
dd = Read_LabviewTxT(filename, timestep=0.002)

popt,pcov,temp_Kst = dd.Calc()

dat_Num = dd.datarray
zeit_achse = dd.timearray

max_value = dat_Num.max()
mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

plt.subplot(211)
xdata = np.linspace(0, N.max(mat[:, 0]), 50)
plt.plot(mat[:,0],mat[:,1])
for data in xdata:
    print draw_tangent(mat[:, 1], mat[:, 0], data)
# print draw_tangent(mat[:,1],mat[:,0],0.037)

plt.plot(xdata,fitfunc_logist(xdata,popt[0],popt[1],popt[2]),'+')
plt.ylabel(r"Druck [bar]", fontsize = 12)

text_fr= 'Parameters \n G : %3.4f\n k : %3.4f\n c : %3.4f\n'%(popt[0],popt[1],popt[2])
plt.text(N.max(zeit_achse)*0.1,max_value*0.5,text_fr)
#plt.text(N.max(zeit_achse)*0.7,max_value*0.2,r'$f(t)=G\cdot \frac { 1 }{ 1+{ e }^{ -kGt-c } } $',fontsize=18)
plt.title(Versuchname + ' // ' + filename)

#print  N.sqrt(N.diag(pcov))


ableitung = fitfunc_logist_dt(xdata,popt[0],popt[1],popt[2])

plt.subplot(212)
#hist, bin_edges = N.histogram(ableitung, bins=60,normed=0)
plt.plot(xdata,ableitung,'o')
text_fr= u'Parameters \n bar/s_max : %3.4f\n barü_max : %3.4f\n P0 : %3.4f'%(N.max(ableitung),dd.Pmax,dd.P0)
plt.text(N.max(zeit_achse)*0.8,N.max(ableitung)*0.5,text_fr)
plt.xlabel(r"Time [s]", fontsize = 12)
plt.ylabel(r"Druck [bar/s]", fontsize = 12)
#savefig(filename+'.png', bbox_inches='tight')
plt.show()