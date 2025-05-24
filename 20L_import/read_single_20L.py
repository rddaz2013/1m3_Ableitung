# coding=utf-8
"""
Reads and plots pressure data from multiple 20L experiment text files.

This script processes a predefined list of data files from the 'data/20L_Example/'
directory. For each file, it uses the `Read_20LTxT` class (specifically its
`OpenFile` method) to load the data. It then identifies a relevant time window
based on pressure thresholds and plots the 'Druck1' and 'Druck2' pressure curves
against 'Zeit' for this window. All plots are overlaid on a single figure.

Original creation date: 26.07.2012
Original author: rene
"""

import matplotlib.pyplot as plt
# Assuming Read_20LTxT is correctly imported from lib.ReadLab_Helper
# Also assuming OpenFile is a method of Read_20LTxT instances.
# If N or np are used within Read_20LTxT, they should be handled there.
from lib.ReadLab_Helper import Read_20LTxT 

# General experiment type, not used in plot titles currently.
Versuchname = ' 20L' 
# Filename variable, reassigned implicitly by the files processed. Not directly used for titles.
# The initial Read_20LTxT instance 'dd' is only used to access its 'OpenFile' method.
# This is slightly awkward; typically, one might create an instance per file or have OpenFile be static
# if it doesn't depend on instance state from the constructor.
dd_helper = Read_20LTxT(filepath='data/20L_Example/dummy.txt', timestep=0.001) # Dummy init, method used is OpenFile

# List of file identifiers to process
file_ids = ["250", "1000", "500", "1750", "2000"] 

plt.figure(figsize=(12, 8)) # Create a single figure for all plots

for i, file_id in enumerate(file_ids):
    filepath = f'data/20L_Example/{file_id}.txt'
    print(f"Processing file: {filepath}")
    
    # x is a pandas DataFrame returned by OpenFile
    x = dd_helper.OpenFile(filepath) 

    # Determine the start of the relevant data range
    # time_start is the index (likely a timestamp or row number) where both pressures are positive.
    # [1] is used to pick the second such occurrence, perhaps to skip an initial noisy trigger.
    # This logic might need adjustment if the data doesn't always fit this pattern.
    try:
        time_start_candidates = x.index[(x['Druck1'] > 0.) & (x['Druck2'] > 0.)]
        if len(time_start_candidates) > 1:
            time_start = time_start_candidates[1]
        elif len(time_start_candidates) == 1:
            time_start = time_start_candidates[0] # Fallback if only one such point
            print(f"  Warning: Only one point found for time_start condition in {filepath}. Using it.")
        else:
            print(f"  Warning: No data points found for time_start condition in {filepath}. Skipping this file.")
            continue # Skip to next file if no valid start time
    except IndexError:
        print(f"  Warning: IndexError while determining time_start for {filepath}. Skipping this file.")
        continue


    druck1_max = x['Druck1'].max()
    druck2_max = x['Druck2'].max()

    # Determine the end of the relevant data range
    # druck_end is the index where both pressures are near their maximum (99% or 95%).
    # The percentage seems to vary (0.99 for the first file, 0.95 for others in original script).
    # Standardizing to 0.95 for consistency here, or could be made file-specific if needed.
    # [1] is used, assuming multiple points might satisfy this; might need robust selection.
    try:
        threshold_factor = 0.99 if file_id == "250" else 0.95 # As per original logic
        druck_end_candidates = x.index[(x['Druck1'] > druck1_max * threshold_factor) & (x['Druck2'] > druck2_max * threshold_factor)]
        if len(druck_end_candidates) > 1:
            druck_end = druck_end_candidates[1]
        elif len(druck_end_candidates) == 1:
            druck_end = druck_end_candidates[0] # Fallback
            print(f"  Warning: Only one point found for druck_end condition in {filepath}. Using it.")
        else:
            print(f"  Warning: No data points found for druck_end condition in {filepath}. Using last data point as druck_end.")
            druck_end = x.index[-1] # Fallback to last data point
    except IndexError:
        print(f"  Warning: IndexError while determining druck_end for {filepath}. Using last data point as druck_end.")
        druck_end = x.index[-1] # Fallback

    # Debug print for the first file, can be removed or kept for specific debugging.
    if file_id == "250":
        print(f"  Data slice for {filepath} (from index {time_start} to {druck_end}):")
        # print(x[time_start:druck_end]) # This prints a slice of the DataFrame by index positions

    # Plotting range extension: `druck_end + 15` adds 15 more data points past the determined end.
    # Ensure this doesn't go out of bounds.
    plot_end_index = min(druck_end + 15, len(x) -1) # Ensure we don't exceed DataFrame bounds

    plt.plot(x['Zeit'][time_start:plot_end_index], x['Druck1'][time_start:plot_end_index], label=f'Druck1 - {file_id}g/m³')
    plt.plot(x['Zeit'][time_start:plot_end_index], x['Druck2'][time_start:plot_end_index], label=f'Druck2 - {file_id}g/m³', linestyle='--')

plt.xlabel("Zeit (s)")
plt.ylabel("Druck (bar)")
plt.title("20L Experiment Pressure Curves")
plt.legend(loc='best')
plt.grid(True)
plt.show()
