# Turbididty REST API

A Mars rover needs to sift through turbidity data to determine if and when the water is safe to use for experiments. It accesses hourly samples from a REST API on [GitHub](https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json) and averages the calculated turbidities of 5 most recent data points to estimate the turbidity of the water. It then uses an exponential decay model to determine when the turbidity will reach a safe level. This assignment demonstrates leveraging Python to access and manipulate data from a REST API.

## Running the Project

This project requires Python 3 to run. You may change the permissions of the scripts to make them executable, or use the `python3` command. The main program is [`analyze_water.py`](analyze_water.py), while unit tests are conducted in [`test_analyze_water.py`](test_analyze_water.py).

## Project Structure
