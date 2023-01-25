# Mars Rover Distance Calculator

This assignment deals with estimating a hypothetical Martian rover's travel time between several meteorite sites. The rover travels at a constant speed, and takes some time to investigate each site which it visits. It demonstrates leveraging Python to write, read, and perform calculations with JSON data structures. These proficiencies are important because JSON is a commonly used format for trasmitting data.

## Running the Project

This project requires Python 3 to run. First, you may execute [`generate_sites.py`](generate_sites.py) to generate a `sites.json` file with random sample data. Then, you may execute [`calculate_distances.py`](calculate_distances.py), which will calculate travel times and output them to the console.

## Project Structure

### [`generate_sites.py`](generate_sites.py)

This script generates 5 random sites for the scenario to a `sites.json` file. Each site has an `index`, a `latitude` from 16 deg N to 18 deg N, a `longitude` from 82 deg E to 84 deg E, and a composition of `stony`, `iron`, or `stony-iron`. Refer to the sample below for an example output.

```json
{
  "sites": [
    {
      "site_id": 1,
      "latitude": 16.52475226160841,
      "longitude": 83.8228375434897,
      "composition": "stony"
    },
    {
      "site_id": 2,
      "latitude": 16.17685665015297,
      "longitude": 83.39194061360591,
      "composition": "stony"
    },
    {
      "site_id": 3,
      "latitude": 17.800931865389675,
      "longitude": 83.70138061801498,
      "composition": "iron"
    },
    {
      "site_id": 4,
      "latitude": 17.84330434302739,
      "longitude": 82.14598833038923,
      "composition": "iron"
    },
    {
      "site_id": 5,
      "latitude": 17.586771730248643,
      "longitude": 83.83064728710985,
      "composition": "stony"
    }
  ]
}
```

## [`calculate_trip.py`](calculate_trip.py)

This script calculates the travel time for any valid JSON file in the format described above. It uses the [haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) with a Martian radius of 3389.5 km to calculate the great circle distance between each point. The rover starts at 16 deg N, 82 deg E, and then travels to each site in the order in which they are presented in the file at a constant velocity of 10 km/hr. Each stop requires a varying amount of time, with `stony` sites taking 1 hr, `iron` sites taking 2 hr, and `stony-iron` sites taking 3 hr. These times are calculated and printed to the console. The example below uses the same data as above.

```
leg = 1, time to travel = 10.81 hr, time to sample = 1.00 hr
leg = 2, time to travel = 3.20 hr, time to sample = 1.00 hr
leg = 3, time to travel = 9.77 hr, time to sample = 2.00 hr
leg = 4, time to travel = 8.76 hr, time to sample = 2.00 hr
leg = 5, time to travel = 9.61 hr, time to sample = 1.00 hr
===============================
number of legs = 5, total time elapsed = 49.15 hr
```
