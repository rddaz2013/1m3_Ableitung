Import Tools for Pressure Measurements
=================

This project provides tools for importing, processing, and analyzing pressure measurement data. It includes functionalities for logistic regression, derivation of pressure curves, and plotting results.

This project is written in Python 3.

## Prerequisites

This project requires Python 3 and the following packages:
- numpy
- pandas
- scipy
- matplotlib

You can install these dependencies using pip and the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Project Structure

The repository is organized as follows:

-   `lib/`: Contains core Python modules for data processing and utility functions (e.g., `ReadLab_Helper.py` for reading specific file formats, `cycler.py`, `rdp.py`).
-   `data/`: Contains example and test data files, organized into subdirectories based on the experiment type or source (e.g., `1m3_DeriveP/`, `20L_Example/`, `Caro2019/`). Many of these subdirectories include their own `readme.txt` or `readme.md` files with more specific details about the data.
-   `ipython/`: Contains Jupyter notebooks (`.ipynb` files) for interactive data analysis, visualization, and potentially as examples of how to use the tools in this project. Includes a `readme.md` for this directory.
-   `1m3_import/`: Contains Python scripts specifically for importing and processing data from "1m3" experiments (e.g., `Derive_Problem.py`, `read_zip_files.py`).
-   `20L_import/`: Contains Python scripts for importing and processing data from "20L" experiments (e.g., `read_single_20L.py`).
-   `requirements.txt`: Lists the Python package dependencies for this project.
-   `readme.md`: This file - providing an overview and guide to the project.

## Data

The `data/` directory contains various datasets used for testing and examples. Here's a summary of some of the subdirectories:

-   **`data/1m3_DeriveP/`**: Contains data from propane experiments conducted at 5% volume. Files ending with `.csv` are oscilloscope readings. The primary focus here was testing the measurement technology.
-   **`data/1m3_DeriveP2/`**: Includes data from propane experiments at 4% volume.
    -   `.txt` files represent normal measurements.
    -   `*r.txt` files are "resting measurements": the mixture was agitated, allowed to rest for 2 minutes, then ignited.
    -   `.csv` files are oscilloscope readings.
-   **`data/20L_Example/`**: Contains example data for the "20L" type experiments. (The specific readme for this was not read, but its existence can be inferred from the `ls` output).
-   **`data/Caro19/` (and `data/Caro2019/`)**: Contains data files in the TDMS format from "CaroVersuch 2019".
-   **`data/Caro2014/`** and **`data/Caro2015/`**: Contain older datasets. (The specific readmes for these were not read, but their existence can be inferred from the `ls` output).

Please refer to the `readme.txt` or `readme.md` files within each subdirectory for more specific details about the respective datasets.

## Usage and Functionality

This project aims to simplify the process of deriving rate of pressure rise data from pressure measurements, particularly for explosion testing.

### Core Capabilities
-   **Data Import:** Tools are provided to import data from various measurement setups and file formats.
-   **Data Processing:** Includes functionalities for data cleaning, normalization, and fitting using a logistic function.
-   **Derivative Calculation:** Calculates the rate of pressure rise (dp/dt) from the processed data.
-   **Plotting:** Enables the creation of diagrams for pressure curves and their derivatives.

### Measurement Types and Import Tools

The project supports different types of measurements:

-   **20L Sphere Measurements:**
    -   Data from 20L sphere experiments typically requires manual export to text files.
    -   The `lib/ReadLab_Helper.py` module contains the `Read_20LTxT` class for handling these files.
    -   Scripts in the `20L_import/` directory (e.g., `read_single_20L.py`) likely provide specific import routines.
-   **1m³ Vessel Measurements:**
    -   The import process for 1m³ vessel data has been undergoing updates.
    -   The `lib/ReadLab_Helper.py` module provides the `Read_LabviewTxT` class, which can be used for LabView text exports.
    -   Scripts in the `1m3_import/` directory (e.g., `Derive_Problem.py`, `read_zip_files.py`) offer tools for importing and processing this data, including handling zipped files.
-   **1XXm³ Vessel Measurements:**
    -   Data from these larger vessels can be directly converted from the measurement acquisition system. (Specific scripts for this are not explicitly detailed in the `lib` or import directories but this was mentioned in the original README).

### Analysis and Output
Once imported, the pressure data is typically:
1.  Converted and pre-processed (e.g., baseline correction, noise reduction).
2.  Fitted with a logistic function (`fitfunc_logist` in `lib/ReadLab_Helper.py`).
3.  The derivative (rate of pressure rise) is then calculated from this fit (`fitfunc_logist_dt` in `lib/ReadLab_Helper.py`).
The results, including plots of pressure curves and their derivatives, can then be generated.

### Jupyter Notebooks for Interactive Analysis
The `ipython/` directory contains Jupyter notebooks (`.ipynb` files). These notebooks are intended for:
-   Interactive data analysis and visualization.
-   Serving as examples or refactored versions of some of the core processing scripts.
Refer to the `ipython/readme.md` for more details on the notebooks.
