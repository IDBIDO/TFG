

# TFG (Final Degree Project)

This repository is dedicated to the Final Degree Project titled "HERRAMIENTAS Y BANCO DE PRUEBAS PARA LA DETECCIÓN DE ANOMALÍAS EN FLUJOS DE DATOS" (Tools and benchmark for Anomaly Detection in Data Streams).
Project final grade: 9.5/10.

## Repository Structure

Here's an overview of the key files included in this repository:

- `config/mdcgen_config.json`: Configuration file for data generation.
- `src/clusterGenDemo.py`: Script for data generation (plots the entire dataset if in 2 Dimension).
- `src/plotter/raw_data_plotter_2D.py`: Script for plotting raw data (only for dataset in 2 Dimension).
- `src/plotter/plot1.py`: Script for plotting experiment results.
- `src/plotter/plot2.py`: Another script for plotting experiment results.
- `data`: Directory containing the data set for experiments. 
- `SENCForest`: Directory containing the SENCForest algorithm implementation in Matlab.

## Data Generation Configuration

The data generator used in this project is a modified version of mdcgenpy. For configuration details, please refer to the [mdcgenpy documentation](https://mdcgenpy.readthedocs.io/en/latest/mdcgenpy.clusters.html#submodules).

The original mdcgenpy generator is available on GitHub: [mdcgenpy GitHub repository](https://github.com/CN-TU/mdcgenpy).

### Custom Parameters

In this modified version of the generator, we have introduced additional parameters:

- `"n_samples_per_period"`: The number of samples per period (integer).
- `"n_periods"`: The number of periods (integer).
- `"n_old_cluster"`: The number of old clusters (integer).
- `"n_new_cluster"`: The number of new clusters (integer).
- `"dead_factor"`: A factor ranging from 0.0 to 4.0 (1.0 recommended). The higher the factor, the more likely a cluster is to die.
Note: The `"n_samples"` parameter now does not influences the number of samples per cluster and is involved in cluster probability computation for each period. For smaller data streams, a value of 100000 is recommended.

## Installation & Dependencies

To install the required dependencies for this project, run the following command:

```sh
pip install -r requirements.txt
```

## Running DAGADENC Generator

### Data Generation

To generate data, navigate to your project's directory and set the `PYTHONPATH`:

```sh
cd [TFG_file_path]
export PYTHONPATH=[TFG_file_path]:$PYTHONPATH
cd src
python3 clusterGenDemo.py
```
For example, my [TFG_file_path] is `/home/he/Desktop/TFG` 
The resulting data will be stored in the `data` directory with name 'float_data.csv' and 'float_data.mat'.
Each executing of the script will overwrite the previous data, so make sure to rename the data files if you want to keep them.

### Data Plotting

To run the data plotting scripts, follow these steps:

```sh
cd src/plotter
python3 raw_data_plotter_2D.py
python3 plot1.py
python3 plot2.py
```

---

## SENCForest
The original repository of SENCForest is available on GitHub: https://github.com/Orzza/SENCForest. This version of SENCForest is modified to work with the data generated by the DAGADENC generator.
To run a SENCForest experiment, open Matlab and follow these steps:

1. **Choose a Dataset**:
   - Select a dataset from the `data` directory (`.mat` file format). Load the dataset by double-clicking on it or by using the `load` command in the Matlab command window.

2. **Prepare Matlab Environment**:
   - Open Matlab and navigate to the `SENCForest` directory.
   - Right-click and select `Add to Path -> Selected Folders and Subfolders`.

3. **Run the Experiment**:
   - Enter `Main` in the Matlab command window and press enter.

**Results**:
After the experiment is finished, the results will be printed in the Matlab command window. You can expect the following results:
   1. Training time (displayed at the beginning of the printed results).
   2. Testing time.
   3. EN_Accuracy.
   4. F-measure.

**Note**: `Main.m` script is configured to run the dataset generated by the DAGADENC generator. 


 
