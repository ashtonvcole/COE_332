# Turbididty REST API

A Mars rover needs to sift through turbidity data to determine if and when the water is safe to use for experiments. It accesses hourly samples from a REST API on [GitHub](https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json) and averages the calculated turbidities of the 5 most recent data points to estimate the turbidity of the water. It then uses an exponential decay model to determine when the turbidity will reach a safe level. This assignment demonstrates leveraging Python to access and manipulate data from a REST API. REST API's are popular because they enabple data to be accesed through the Internet with HTTP requests. The assignment also verifies its functions with `pytest` unit tests, which is a crucial step of software development.

## Running the Project

This project requires Python 3 to run. It also requires a stable internet connection and the modules `requests`, `json`, `math`, and `pytest`. The main program is [`analyze_water.py`](analyze_water.py). You may change the permissions of the script to make it executable, or simply use the `python3` command. Unit tests are conducted in [`test_analyze_water.py`](test_analyze_water.py), and are executed by typing the command `pytest` in the directory of the project.

## Project Structure

The project consists of two separately executable Python files.

- [`analyze_water.py`](analyze_water.py)
- [`test_analyze_water.py`](test_analyze_water.py)

### [`analyze_water.py`](analyze_water.py)

This script accesses the [turbidity JSON data](https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json) with a HTTP GET request and filters the 5 most recent entries. It takes the `calibration_constant` and the magnitude of the `detector_current` to calculate an average turbidity of the water. From this, it uses an exponential decay model with a decay rate of 2% and a maximum safe turbidity threshold of 1 to estimate the minimum time it takes for the turbidity to become safe. If the initial turbidity is above the threshold, it will produce output like the following.

```
Average turbidity based on most recent five measurements: 1.1246
Warning: Turbidity is above threshold for safe use
Minimum time required to return to a safe threshold: 5.81 hours
```

On the other hand, if the initial turbidity is already below 1, it will clarify that the water is safe.

```
Average turbidity based on most recent five measurements = 0.9852 NTU
Info: Turbidity is below threshold for safe use
Minimum time required to return below a safe threshold = 0 hours
```

### [`test_analyze_water.py`](test_analyze_water.py)

This script makes several assertions to ensure that all of the functions within [`analyze_water.py`](analyze_water.py) function as intended. It is expected to provide successful results like the following.

```
=========================== test session starts ============================
platform linux -- Python 3.8.10, pytest-7.2.1, pluggy-1.0.0
rootdir: <your_directory>
collected 2 items

test_analyze_water.py ..                                             [100%]

============================ 2 passed in 0.08s =============================
```
