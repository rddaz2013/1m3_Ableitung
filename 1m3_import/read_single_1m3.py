# coding=utf-8
"""
Script for processing and visualizing single 1m³ pressure data files from LabVIEW text exports.

This script reads pressure data from a specified file (presumably from a 1m³ experiment),
performs a logistic fit, calculates the rate of pressure rise (dp/dt),
and generates plots for analysis. It also demonstrates drawing multiple tangents
along the pressure curve.

Original creation date: 26.07.2012
Original author: rene
"""

from pandas import * # Consider replacing with specific imports if not all functions are needed
import numpy as N # It seems 'N' is used as an alias for numpy, standard is 'np'
import matplotlib.pyplot as plt # plt was used but not imported

# Importing necessary functions from the project's library
from lib.ReadLab_Helper import Read_LabviewTxT, fitfunc_logist, fitfunc_logist_dt
from lib.ReadLab_Helper import draw_tangent # Assuming this is the intended function for drawing tangents

# --- Script Configuration ---
Versuchname = ' Umbau' # Experiment name, appears to be a general placeholder
filename = 'data/1m3_DeriveP/propan_500hz_1_50L.txt' # Path to the data file
dd = Read_LabviewTxT(filename, timestep=0.002)

popt,pcov,temp_Kst = dd.Calc()

dat_Num = dd.datarray
zeit_achse = dd.timearray

max_value = dat_Num.max()
mat = N.column_stack((zeit_achse[:,N.newaxis],dat_Num[:,N.newaxis]))

plt.subplot(211)
xdata = np.linspace(0, N.max(mat[:, 0]), 50)
plt.plot(mat[:,0], mat[:,1], label="Original Data") # Plot the raw pressure data

# Loop to draw tangents and print their slopes at various points defined in xdata
# This is likely for detailed analysis or debugging of the curve's derivative.
for data_point_y_domain in xdata: # 'data' here is a y-axis value (time) from xdata array
    # The draw_tangent function plots the tangent and returns the slope.
    # Note: The original script prints the slope but doesn't store or use it further in this loop.
    print(f"Slope at y={data_point_y_domain:.4f}: {draw_tangent(mat[:, 1], mat[:, 0], data_point_y_domain)}")

plt.plot(xdata, fitfunc_logist(xdata, popt[0], popt[1], popt[2]), '+', label="Logistic Fit")
plt.ylabel(r"Druck [bar]", fontsize=12)
plt.legend()

text_params = 'Parameters \n G : %3.4f\n k : %3.4f\n c : %3.4f\n' % (popt[0], popt[1], popt[2])
plt.text(N.max(zeit_achse) * 0.1, max_value * 0.5, text_params)
# The following line for displaying the formula was commented out in the original code.
# plt.text(N.max(zeit_achse)*0.7,max_value*0.2,r'$f(t)=G\cdot \frac { 1 }{ 1+{ e }^{ -kGt-c } } $',fontsize=18)
plt.title(f"{Versuchname} // {filename.split('/')[-1]}") # Using f-string and extracting filename

# --- Derivative Plot ---
ableitung = fitfunc_logist_dt(xdata, popt[0], popt[1], popt[2]) # Calculate derivative from the logistic fit

plt.subplot(212)
# The histogram calculation was commented out in the original code.
# hist, bin_edges = N.histogram(ableitung, bins=60, normed=0)
plt.plot(xdata, ableitung, 'o', label="Derivative (dp/dt)")
text_derivative_params = u'Parameters \n bar/s_max : %3.4f\n barü_max : %3.4f\n P0 : %3.4f' % (N.max(ableitung), dd.Pmax, dd.P0)
plt.text(N.max(zeit_achse) * 0.8, N.max(ableitung) * 0.5, text_derivative_params)
plt.xlabel(r"Time [s]", fontsize=12)
plt.ylabel(r"Druck [bar/s]", fontsize=12)
plt.legend()

# Save the plot if needed
# savefig(filename.split('/')[-1] + '.png', bbox_inches='tight')
plt.show() # Display the combined plots