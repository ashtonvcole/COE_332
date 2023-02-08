#!/usr/bin/env python3

import requests
import json
import math

# Constants
turbidity_safe = 1.0 # threshold for safe water in NTU
decay_factor = 0.02 # decay rate per hour

def turbidity_of(a0: float, I90: float) -> float:
    """Calculates the turbidity of a given sample.

    This function uses a simple equation to convert a 90 degree detector
    current into the appropriate turbidity, given a calibrating constant. It
    uses the following simple formula, where T is the turbidity, a0 is a
    calibration constant, and I90 is the measured 90 degree detector contant.

    T = a0 * I90

    Args:
        a0: A calibration constant.
        I90: Measured 90 degree detector current.

    Returns:
        The calculated turbidity of the water in NTU. Note that this
        calculation is only considered valid for turbidities in the range of
        0-40 NTU.
    """
    return a0 * abs(I90)

def turbidity_min_time(Ts: float, T0: float, d: float) -> float:
    """Calculates the minimum time for turbid water to be safe.

    This function determines the minimum time for turbid water to reach a
    safe level using the following inequality, where T0 is the current
    turbidity, d is a decay factor per hour b is the number of hours
    elapsed, and Ts is the safe turbidity level. When this is true, the
    water is considered safe.

    Ts >= T0 * (1 - d) ** b

    Args:
        Ts: Turbudity threshold for safe water, in NTU.
        T0: Current turbidity of a sample, in NTU.
        d: Decay factor, per hour.

    Returns:
        The minimum time to reach the safe threshold, in hours.
    """
    return math.log(Ts / T0) / math.log(1 - d)

def main():
    response = requests.get(url = 'https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
    data = json.loads(response.content)
    # Sort the data chronologically
    data['turbidity_data'].sort(key = lambda i: (i['datetime']))
    # Use 5 most recent data points, if possible
    T0 = 0.0
    if len(data['turbidity_data']) >= 5:
        for i in range(len(data['turbidity_data']) - 5, len(data['turbidity_data'])):
            T0 += turbidity_of(data['turbidity_data'][i]['calibration_constant'], data['turbidity_data'][i]['detector_current'])
        T0 /= 5
    elif len(data['turbidity_data']) > 0:
        for item in data['turbidity_data']:
            T0 += turbidity_of(item['calibration_constant'], item['detector_current'])
        T0 /= len(data['turbidity_data'])
    else:
        print('No data found! Drink at your own risk...')
        return
    b = turbidity_min_time(turbidity_safe, T0, decay_factor)
    print(f'Average turbidity based on most recent five measurements: {T0:.4f}')
    if b > 0:
        print('Warning: Turbidity is above threshold for safe use')
        print(f'Minimum time required to return to a safe threshold: {b:.2f} hours')
    else:
        print('Info: Turbidity is below threshold for safe use')
        print('Minimum time required to return to a safe threshold: 0 hours')

if __name__ == "__main__":
    main()
