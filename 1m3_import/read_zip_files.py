# coding=utf-8
"""
Processes multiple LabVIEW text export files from a specified directory.

This script iterates through all '.txt' files in the './data/Caro2014/' directory.
For each file, it reads the pressure data using `Read_LabviewTxT`, performs
a logistic fit, calculates the maximum rate of pressure rise (Kst value),
and extracts a weight value from the filename.

The script collects the maximum pressure, extracted weight, and calculated Kst
for each file. It also plots the logistic fit for each file on a combined plot.
Finally, it prepares lists of these collected values, which could be used for
further analysis or plotting (e.g., Kst vs. weight).

Original creation date: 26.07.2012
Original author: rene
Note: The filename 'read_zip_files.py' might be misleading as the script
currently processes .txt files from './data/Caro2014/', not .zip files.
If .zip file processing is intended, the glob pattern and file reading logic
would need to be updated.
"""

import glob
import matplotlib.pyplot as plt # plt was used but not explicitly imported
import numpy as N # N was used but not explicitly imported (assuming it's numpy)

# Consider specific imports if not all pandas functions are needed
from pandas import DataFrame # Example, adjust as necessary if pandas is used. Currently, pandas DataFrame/Series not explicitly used.

# Importing necessary functions from the project's library
from lib.ReadLab_Helper import Read_LabviewTxT, fitfunc_logist, fitfunc_logist_dt

# Lists to store aggregated results from all processed files
Liste_Gewicht = []  # List to store extracted weights from filenames
Liste_Druck = []    # List to store maximum pressure values
Liste_Kst = []      # List to store calculated maximum Kst values (max rate of pressure rise)

# Iterate over all .txt files in the specified directory
for name in glob.glob('./data/Caro2014/*.txt'):
    print(f"Processing file: {name}") # Log which file is being processed
    dd = Read_LabviewTxT(name, timestep=0.002) # Initialize data reading class
    popt, pcov = dd.Calc()  # Perform calculations (fitting, etc.)

    dat_Num = dd.datarray       # Pressure data array
    zeit_achse = dd.timearray   # Time data array

    max_value = dat_Num.max()   # Maximum pressure value from the current file
    # Stack time and pressure data for some operations if needed, though mat is not directly used later
    mat = N.column_stack((zeit_achse[:, N.newaxis], dat_Num[:, N.newaxis]))

    # Generate x-values for plotting the fitted function
    xdata = N.linspace(0, N.max(zeit_achse), 100) # Corrected to use zeit_achse for max limit
    
    # Calculate the maximum rate of pressure rise (Kst) from the derivative of the logistic fit
    temp_kst = N.max(fitfunc_logist_dt(xdata, popt[0], popt[1], popt[2]))
    
    # Print summary for the current file: filename, max pressure, Kst, and fit parameters
    print(f"  File: {name.split('/')[-1]}, Max Pressure: {N.max(dat_Num):.2f}, Kst: {temp_kst:.2f}, Fit Params: {popt}")
    
    # Extract weight from filename (e.g., "Sensor_XYZ_1.23g_more.txt" -> 1.23)
    # This parsing is specific to a particular filename convention.
    try:
        temp_gewicht = float(name.split('/')[-1].replace('.txt', '').split('_')[2].replace('g', ''))
    except (IndexError, ValueError) as e:
        print(f"  Warning: Could not parse weight from filename: {name}. Error: {e}. Using NaN.")
        temp_gewicht = N.nan # Use NaN if parsing fails

    # Plot the logistic fit for the current file's data
    plt.plot(xdata, fitfunc_logist(xdata, popt[0], popt[1], popt[2]), '+', label=f"Fit for {name.split('/')[-1]}")
    
    # Append results to the aggregate lists
    Liste_Druck.append(N.max(dat_Num))
    Liste_Gewicht.append(temp_gewicht)
    Liste_Kst.append(temp_kst)

# Example of how the collected data could be plotted (Kst vs. Weight)
# plt.figure() # Create a new figure for this summary plot
# plt.plot(Liste_Gewicht, Liste_Kst, 'ro', label='Kst vs. Weight')
# plt.xlabel("Weight (g)")
# plt.ylabel("Kst (bar/s)")
# plt.title("Kst vs. Weight from Caro2014 Data")
# plt.legend()

plt.xlabel("Time (s)")
plt.ylabel("Pressure (bar) / Fitted Pressure")
plt.title("Logistic Fits for Caro2014 Data Files")
# plt.legend() # Adding legend for individual fits might make the plot too busy if many files. Optional.
plt.show() # Display the combined plot of all logistic fits


