# coding=utf-8
"""
Processes multiple LabVIEW text export files in parallel using Parallel Python (pp).

This script iterates through all '.txt' files in the './data/Caro2015/' directory.
It uses the `pp` library to distribute the processing of each file to
available workers. For each file, the `Calc2` function is called, which
reads pressure data using `Read_LabviewTxT` and performs calculations (fitting, etc.).

The script then retrieves results, extracts experiment name and weight using regex
from the filename, and plots Kst_max vs. Gewicht, labeling points with the
experiment name.

Original creation date: 26.07.2012
Original author: rene
Note: The filename 'read_zip_files_pp.py' might be misleading as the script
currently processes .txt files from './data/Caro2015/', not .zip files.
"""

import glob
import re
import matplotlib.pyplot as plt
import pp # Parallel Python library
import numpy as N # Assuming N is used within ReadLab_Helper or for consistency

# These lists are defined but not used in the current script logic.
# They might be remnants of a previous version or intended for future use.
# Liste_Gewicht = []
# Liste_Druck = []
# Liste_Kst = []

# Tuple of Parallel Python servers. Empty means autodiscovery or local machine.
ppservers = ()

# Create a Parallel Python job server.
# Uses autodiscovered servers or local machine if ppservers is empty.
job_server = pp.Server(ppservers=ppservers)
# Using job_server.get_ncpus() - 1 to leave one core for the main process if desired,
# or simply job_server.get_ncpus() to use all available cores.
print(f"Starting Parallel Python (pp) with {job_server.get_ncpus()} workers.")


def Calc2(name, timestep):
    """
    Worker function to process a single LabVIEW data file.

    This function is intended to be submitted to a Parallel Python (pp) server.
    It initializes a Read_LabviewTxT object with the given filename and timestep,
    then calls its Calc() method to perform data processing and fitting.

    Args:
        name (str): The path to the LabVIEW text export file.
        timestep (float): The timestep of the data.

    Returns:
        tuple: A tuple containing the input filename and the result of dd.Calc()
               (which typically includes fitting parameters and calculated values like Kst, Pmax, P0).
    """
    # Import is inside the function as it's executed by remote workers
    # that might not have the global context.
    from lib.ReadLab_Helper import Read_LabviewTxT
    dd = Read_LabviewTxT(name, timestep)
    # dd.Calc() is expected to return a tuple, e.g., (popt, pcov, kst_max_calculated, pmax_val, p0_val)
    # The exact structure of job()[1] (result of dd.Calc()) needs to be known
    # based on ReadLab_Helper.Calc() method's return value.
    # Assuming job()[1] = (popt, pcov, kst_val_from_calc, pmax_val, p0_val)
    # And popt = [G, k, c] (fit parameters)
    return name, dd.Calc()

# Prepare job list from files in the specified directory
job_list = glob.glob('./data/Caro2015/*.txt')
print(f"Found {len(job_list)} files to process in './data/Caro2015/'.")

jobs = [] # List to hold submitted jobs
timestep = 0.002 # Timestep for data reading

# Submit jobs to the server
for name in job_list:
    # Submit Calc2 function with (filename, timestep) arguments.
    # Modules to be available for the job: 'lib.ReadLab_Helper'
    jobs.append(job_server.submit(Calc2, (name, timestep), modules=('lib.ReadLab_Helper',)))

job_server.print_stats() # Print statistics about the jobs executed

# Process results
plt.figure(figsize=(10, 6)) # Create a figure for the plot

for job in jobs:
    result = job() # Get the result from the completed job
    if result:
        dateiname = result[0]
        # Assuming result[1] from dd.Calc() is structured like: (popt, pcov, kst_max_calc, Pmax_actual, P0_actual)
        # And popt = [G_val, k_val, c_val]
        # So, kst_max is result[1][2]
        # And max_P (related to G from fit, or Pmax_actual) needs clarification.
        # Original: max_P = job()[1][0][2] -> this would be popt[2] which is 'c' from the fit.
        # This seems incorrect if max_P is meant to be the max pressure.
        # Let's assume kst_max is result[1][2] (calculated Kst)
        # and Pmax (actual max pressure from data) is result[1][3]
        
        calc_output = result[1] # (popt, pcov, kst_val, pmax_val, p0_val)
        popt_params = calc_output[0] # [G, k, c]
        kst_max = calc_output[2] # Calculated Kst
        actual_max_P = calc_output[3] # Actual Pmax from data
        
        # Regex to extract Experiment Name (e.g., V01) and Weight (e.g., 020g)
        # Example filename: "./data/Caro2015/V01 020g_1.txt"
        m = re.search(r"(V\d+) (\d+)g", dateiname) # Simplified and corrected regex

        Versuch_Name = "Unknown"
        Gewicht_str = "0" # Default string for weight

        if m:
            Versuch_Name = m.group(1) # e.g., V01
            Gewicht_str = m.group(2)  # e.g., 020
            Gewicht_val = float(Gewicht_str) # Convert weight to float
        else:
            print(f"Warning: Could not parse experiment name or weight from filename: {dateiname}")
            Gewicht_val = N.nan # Use NaN if parsing fails

        if Gewicht_val is not N.nan:
             plt.plot([Gewicht_val], [kst_max], 'ro', label=Versuch_Name if Versuch_Name not in plt.gca().get_legend_handles_labels()[1] else "")
        else:
            print(f"Skipping plot for {dateiname} due to parsing error.")

        print(f"Experiment: {Versuch_Name}, Weight: {Gewicht_str}g, Max Pressure (actual): {actual_max_P:.2f}, Kst: {kst_max:.2f}")

# Plotting final results
plt.xlabel("Weight (g)")
plt.ylabel("Kst_max (bar m/s)") # Assuming Kst is in bar m/s
plt.title("Kst_max vs. Weight for Caro2015 Data (Parallel Processed)")

# Create a unique legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
if by_label: # Check if there are any labels
    plt.legend(by_label.values(), by_label.keys(), title="Experiment Series")

plt.grid(True)
plt.show()


