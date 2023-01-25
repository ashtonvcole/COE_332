#!/usr/bin/env python3

import json
import math

def coord_distance(lat_1: float, lon_1: float, lat_2: float, lon_2: float, r: float) -> float:
    lat_1 = lat_1 * math.pi / 180.0
    lon_1 = lon_1 * math.pi / 180.0
    lat_2 = lat_2 * math.pi / 180.0
    lon_2 = lon_2 * math.pi / 180.0
    dl_lam = (lon_2 - lon_1)
    dl_phi = (lat_2 - lat_1)
    dl_sig = 2 * math.asin(math.sqrt( \
            (math.sin(dl_phi / 2)) ** 2 + \
            (1 - (math.sin(dl_phi / 2)) ** 2 - (math.sin((lat_1 + lat_2) / 2)) ** 2) * \
            (math.sin(dl_lam / 2)) ** 2 \
            ))
    return r * dl_sig

def main():
    # Import JSON file
    with open('sites.json', 'r') as f:
        data = json.load(f)
    # Constants for problem
    lat_0 = 16.0 # deg
    lon_0 = 82.0 # deg
    v_max = 10.0 # km / h
    R = 3389.5 # km
    t_s = 1.0 # hr
    t_i = 2.0 # hr
    t_si = 3.0 # hr
    # Accumulators for problem
    i = 0
    t_total = 0.0 # hr
    # Calculate time in order
    for site in data['sites']: # For each site object
        i += 1
        # Calculate time elapsed, add to total
        t_travel = coord_distance(lat_0, lon_0, site['latitude'], site['longitude'], R) / v_max
        t_sample = 0.0
        if site['composition'] == 'stony':
            t_sample = 1.0
        elif site['composition'] == 'iron':
            t_sample = 2.0
        elif site['composition'] == 'stony-iron':
            t_sample = 3.0
        t_total = t_total + t_travel + t_sample
        # Print to console
        print(f'leg = {i}, time to travel = {t_travel:.2f} hr, time to sample = {t_sample:.2f} hr')
        # Set new starting point
        lat_0 = site['latitude']
        lon_0 = site['longitude']
    print('===============================')
    print(f'number of legs = {i}, total time elapsed = {t_total:.2f} hr')

if __name__ == "__main__":
    main()
