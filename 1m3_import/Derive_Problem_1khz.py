# coding=utf-8
"""
Script for processing and visualizing pressure data from LabVIEW text exports (1kHz variant).

This script reads pressure data (assumed to be sampled at 1kHz, based on filename
and `timestep=0.001`), performs a logistic fit, calculates the rate of pressure
rise (dp/dt), and generates plots for analysis. It appears to be designed for
specific older LabVIEW export formats. The script processes two example files sequentially.

Original creation date: 26.07.2012
Original author: rene
"""

from pandas import * # Consider replacing with specific imports if not all functions are needed
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as N # It seems 'N' is used as an alias for numpy, standard is 'np'

from lib.ReadLab_Helper import * # Consider specific imports


def draw_tangent(x, y, a):
    """
    Calculates, plots, and returns the derivative of a spline at a point 'a'.

    The function first fits a spline to the data (y, x) - note that x and y might
    be swapped in intent compared to typical mathematical notation (y as function of x).
    Here, it seems 'x' is the value array and 'y' is the time/domain array.
    It then evaluates the spline and its first derivative at point 'a' (on the y-domain).
    A tangent line based on this evaluation is plotted.

    Args:
        x (array-like): The dependent variable data (e.g., pressure values).
        y (array-like): The independent variable data (e.g., time values).
        a (float): The point in the 'y' domain at which to calculate and draw the tangent.

    Returns:
        float: The value of the first derivative of the spline (dx/dy) at point 'a'.
    """
    # Fit a spline: x = f(y)
    spl = interpolate.splrep(y, x)
    # Create a small range of y-values around 'a' for plotting the tangent line
    small_t = N.linspace(a - (a / 10), a + (a / 10), num=5)
    fa = interpolate.splev(a, spl, der=0)     # Value of the spline (x) at y=a
    fprime = interpolate.splev(a, spl, der=1) # Value of the first derivative (dx/dy) at y=a
    tan = fa + (fprime * (small_t - a)) # Equation of the tangent line: x_tan = x(a) + x'(a)*(y - a)

    plt.plot(a, fa, 'om') # Mark the point (a, x(a)) on the plot
    plt.plot(small_t, tan, '--r', lw=3) # Plot the tangent line
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


ableitung = fitfunc_logist_dt(xdata, popt[0], popt[1], popt[2])
plt.subplot(212)
hist, bin_edges = N.histogram(ableitung, bins=60, normed=0) # Calculate histogram of the derivative
plt.plot(xdata, ableitung, 'o')
text_fr = u'Parameters \n bar/s_max : %3.4f\n barü_max : %3.4f\n P0 : %3.4f' % (N.max(ableitung), dd.Pmax, dd.P0)
plt.text(N.max(zeit_achse) * 0.1, N.max(ableitung) * 0.5, text_fr)
plt.xlabel(r"Time [s]", fontsize=12)
plt.ylabel(r"Druck [bar/s]", fontsize=12)

# Save the first plot if needed
# savefig(filename + '.png', bbox_inches='tight')
# plt.show() # Display the first plot; commented out to allow the second plot to proceed

# --- Start of the second data processing block (largely a repetition of the first) ---
Versuchname = ' Umbau' # Experiment name
filename = 'Sensor1_propan.txt' # Filename for the second dataset
dd = Read_LabviewTxT('data/1m3_DeriveP/Sensor1_propan.txt', timestep=0.001)

popt,pcov,temp_Kst = dd.Calc()

dat_Num = dd.datarray
zeit_achse = dd.timearray

max_value = dat_Num.max()
mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

plt.subplot(211)
xdata = np.linspace(0, N.max(mat[:,0]), 200)
plt.plot(mat[:,0], mat[:,1])
# The following calls to draw_tangent were commented out in the original code.
# print draw_tangent(mat[:,1],mat[:,0],0.04)
# print draw_tangent(mat[:,1],mat[:,0],0.0443)
plt.plot(xdata, fitfunc_logist(xdata, popt[0], popt[1], popt[2]), '+')
plt.ylabel(r"Druck [bar]", fontsize=12)

text_fr = 'Parameters \n G : %3.4f\n k : %3.4f\n c : %3.4f\n' % (popt[0], popt[1], popt[2])
plt.text(N.max(zeit_achse) * 0.1, max_value * 0.5, text_fr)
# The following line for displaying the formula was commented out in the original code.
# plt.text(N.max(zeit_achse)*0.7,max_value*0.2,r'$f(t)=G\cdot \frac { 1 }{ 1+{ e }^{ -kGt-c } } $',fontsize=18)
plt.title(Versuchname + ' // ' + filename)


ableitung = fitfunc_logist_dt(xdata, popt[0], popt[1], popt[2])

plt.subplot(212)
# The histogram calculation was commented out in the original code for the second block.
# hist, bin_edges = N.histogram(ableitung, bins=60,normed=0)
plt.plot(xdata, ableitung, 'o')
text_fr = u'Parameters \n bar/s_max : %3.4f\n barü_max : %3.4f\n P0 : %3.4f' % (N.max(ableitung), dd.Pmax, dd.P0)
plt.text(N.max(zeit_achse) * 0.8, N.max(ableitung) * 0.5, text_fr)
plt.xlabel(r"Time [s]", fontsize=12)
plt.ylabel(r"Druck [bar/s]", fontsize=12)

# Save the second plot if needed
# savefig(filename + '.png', bbox_inches='tight')
plt.show() # Display the combined plots