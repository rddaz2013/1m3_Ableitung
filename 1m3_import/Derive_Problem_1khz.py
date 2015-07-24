# coding=utf-8
'''
Created on 26.07.2012
Dieses Programm ist fuer alten Labview txt-export daten 
@author: rene
'''

from pandas import *
import matplotlib.pyplot as plt
from scipy import interpolate

from lib.ReadLab_Helper import *


def draw_tangent(x,y,a):
    # interpolate the data with a spline
    spl = interpolate.splrep(y,x)
    small_t = N.linspace(a-(a/10),a+(a/10),num=5)
    fa = interpolate.splev(a,spl,der=0)     # f(a)
    fprime = interpolate.splev(a,spl,der=1) # f'(a)
    tan = fa+(fprime*(small_t-a)) # tangent

    plt.plot(a,fa,'om')
    plt.plot(small_t,tan,'--r',lw=3)#
    return fprime


Versuchname = ' Umbau'
filename = 'Sensor2_propan.txt'
dd = Read_LabviewTxT('data/1m3_DeriveP/Sensor2_propan.txt', timestep=0.001)

popt,pcov,temp_Kst = dd.Calc()

dat_Num = dd.datarray
zeit_achse = dd.timearray

max_value = dat_Num.max()
mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

plt.subplot(211)
xdata = np.linspace(0, N.max(mat[:,0]), 200)
plt.plot(mat[:,0],mat[:,1])
plt.plot(xdata,fitfunc_logist(xdata,popt[0],popt[1],popt[2]),'+')
plt.ylabel(r"Druck [bar]", fontsize = 12)

text_fr= 'Parameters \n G : %3.4f\n k : %3.4f\n c : %3.4f\n'%(popt[0],popt[1],popt[2])
plt.text(N.max(zeit_achse)*1.2,max_value*0.5,text_fr)
plt.text(N.max(zeit_achse)*0.7,max_value*0.2,r'$f(t)=G\cdot \frac { 1 }{ 1+{ e }^{ -kGt-c } } $',fontsize=18)
plt.title(Versuchname + ' // ' + filename)

#print  N.sqrt(N.diag(pcov))


ableitung = fitfunc_logist_dt(xdata,popt[0],popt[1],popt[2])
plt.subplot(212)
hist, bin_edges = N.histogram(ableitung, bins=60,normed=0)
plt.plot(xdata,ableitung,'o')
text_fr= u'Parameters \n bar/s_max : %3.4f\n barü_max : %3.4f\n P0 : %3.4f'%(N.max(ableitung),dd.Pmax,dd.P0)
plt.text(N.max(zeit_achse)*0.1,N.max(ableitung)*0.5,text_fr)
plt.xlabel(r"Time [s]", fontsize = 12)
plt.ylabel(r"Druck [bar/s]", fontsize = 12)
#savefig(filename+'.png', bbox_inches='tight')
#plt.show()

Versuchname = ' Umbau'
filename = 'Sensor1_propan.txt'
dd = Read_LabviewTxT('data/1m3_DeriveP/Sensor1_propan.txt', timestep=0.001)

popt,pcov,temp_Kst = dd.Calc()

dat_Num = dd.datarray
zeit_achse = dd.timearray

max_value = dat_Num.max()
mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

plt.subplot(211)
xdata = np.linspace(0, N.max(mat[:,0]), 200)
plt.plot(mat[:,0],mat[:,1])
#print draw_tangent(mat[:,1],mat[:,0],0.04)
#print draw_tangent(mat[:,1],mat[:,0],0.0443)
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