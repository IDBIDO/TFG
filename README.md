

# TFG (Final Degree Project)

This repository is dedicated to the Final Degree Project titled "HERRAMIENTAS Y BANCO DE PRUEBAS PARA LA DETECCIÓN DE ANOMALÍAS EN FLUJOS DE DATOS" (Tools and benchmark for Anomaly Detection in Data Streams).

## Repository Structure

Here's an overview of the key files included in this repository:

- `config/mdcgen_config.json`: Configuration file for data generation.
- `src/clusterGenDemo.py`: Script for data generation (plots the entire dataset if in 2D).
- `src/plotter/raw_data_plotter_2D.py`: Script for plotting raw data (periodic plots in 2D).
- `src/plotter/plot1.py`: Script for plotting experiment results.
- `src/plotter/plot2.py`: Another script for plotting experiment results.

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

## Running the Project

### Data Generation

To generate data, navigate to your project's directory and set the `PYTHONPATH`:

```sh
cd [TFG_file_path]
export PYTHONPATH=[your_TFG_path]:$PYTHONPATH
cd src
python3 clusterGenDemo.py
```
For example, my [TFG_file_path] is `/home/he/Desktop/TFG` 


### Data Plotting

To run the data plotting scripts, follow these steps:

```sh
cd src/plotter
python3 raw_data_plotter_2D.py
python3 plot1.py
python3 plot2.py
```

## Contact


## License


---


 
