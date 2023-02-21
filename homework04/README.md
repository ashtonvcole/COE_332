# ISS Orbit API

This project creates a simple, locally-hosted Flask API to process HTTP requests for trajectory data for the International Space Station. It then accesses an XML-format Orbital Ephemeris Message from NASA, which it filters and processes to satisfy the query and returns to the user in text or JSON format. More information on the data set can be found [on the NASA website](https://spotthestation.nasa.gov/trajectory_data.cfm).

This assignment is important, because it demonstrates how Python, a relatively simple programming language, can be applied to create a web API capable of acessing and processing large data sets. It also has value from a user perspective, since instead of receiving a complicated XML file of the whole data set, a user can request only what they need, and receive it in JSON.

## Running the Project

This project requires Python 3 to run. It also requires a stable internet connection and the modules `requests` and `xmltodict`. The server can be started by changing the permissions of [`iss_tracker.py`](iss_tracker.py) to make it executable, or running it with the `python3` command. Alternatively, it can be run with the command `flask --app iss_tracker --debug run`. All put the server in debug mode. From another terminal window, you may usse the `curl` command to make HTTP requests.

## Project Structure

The project consists of a single Python file.

- `iss_tracker.py` [About](#iss_trackerpy) [File](iss_tracker.py)

### [`iss_tracker.py`](iss_tracker.py)

This script processes all HTTP requests to the API. In addition to code that initializes the server, it contains several functions which execute and return data for a certain endpoint.

## Endpoints

The following endpoints are available to the user.

- [`/`](#)
- [`/epochs`](#epochs)
- [`/epochs/<epoch>`](#epochsepoch)
- [`/epochs/<epoch>/speed`](epochsepochspeed)

### `/`

This returns the entire data set in JSON format. Each state vector is an item in a list associated with the nested dictionary entries `"ndm"`, `"oem"`, `"body"`, `"segment"`, `"data"`, and `"stateVector"`

```bash
curl localhost:5000/
```

```json
{
  "ndm": {
    "oem": {
      "@id": "CCSDS_OEM_VERS",
      "@version": "2.0",
      "body": {
        "segment": {
          "data": {
            "stateVector": [
              {
                "EPOCH": "2023-048T12:00:00.000Z",
                "X": {
                  "#text": "-5097.51711371908",
                  "@units": "km"
                },
                "X_DOT": {
                  "#text": "-4.5815461024513304",
                  "@units": "km/s"
                },
                "Y": {
                  "#text": "1610.3574036042901",
                  "@units": "km"
                },
                "Y_DOT": {
                  "#text": "-4.8951801207083303",
                  "@units": "km/s"
                },
                "Z": {
                  "#text": "-4194.4848049601396",
                  "@units": "km"
                },
                "Z_DOT": {
                  "#text": "3.70067961081915",
                  "@units": "km/s"
                }
              },
              ...
            ]
          },
          "metadata": {
            "CENTER_NAME": "EARTH",
            "OBJECT_ID": "1998-067-A",
            "OBJECT_NAME": "ISS",
            "REF_FRAME": "EME2000",
            "START_TIME": "2023-048T12:00:00.000Z",
            "STOP_TIME": "2023-063T12:00:00.000Z",
            "TIME_SYSTEM": "UTC"
          }
        }
      },
      "header": {
        "CREATION_DATE": "2023-049T01:38:49.191Z",
        "ORIGINATOR": "JSC"
      }
    }
  }
}
```

### `/epochs`

This returns a list of all epochs in JSON format. This is the time associated witha data point. They are in the form `YYYY-DDDTHH:MM:SS.000Z`.

```bash
curl localhost:5000/epochs
```

```json
[
  "2023-048T12:00:00.000Z",
  "2023-048T12:04:00.000Z",
  "2023-048T12:08:00.000Z",
  "2023-048T12:12:00.000Z",
  "2023-048T12:16:00.000Z",
  ...
]
```

### `/epochs/<epoch>`

This returns the state vector associated with a given epoch in JSON format. This includes the epoch, position, and velocity components. Epochs are in the form `YYYY-DDDTHH:MM:SS.000Z`, which means that `<epoch>` needs to be formatted with character codes as `YYYY-DDDTHH%3AMM%3ASS%2E000Z`. If a bad input is given, a 404 error is returned.

```bash
curl localhost:5000/epochs/2023-048T12%3A00%3A00%2E000Z
```

```json
{
  "EPOCH": "2023-048T12:00:00.000Z",
  "X": {
    "#text": "-5097.51711371908",
    "@units": "km"
  },
  "X_DOT": {
    "#text": "-4.5815461024513304",
    "@units": "km/s"
  },
  "Y": {
    "#text": "1610.3574036042901",
    "@units": "km"
  },
  "Y_DOT": {
    "#text": "-4.8951801207083303",
    "@units": "km/s"
  },
  "Z": {
    "#text": "-4194.4848049601396",
    "@units": "km"
  },
  "Z_DOT": {
    "#text": "3.70067961081915",
    "@units": "km/s"
  }
}
```

### `/epochs/<epoch>/speed`

This returns the speed, i.e. 2-norm, of the velocity components. It is returned in JSON format, along with the units associated with `"X_DOT"`. Epochs are in the form `YYYY-DDDTHH:MM:SS.000Z`, which means that `<epoch>` needs to be formatted with character codes as `YYYY-DDDTHH%3AMM%3ASS%2E000Z`. If a bad input is given, a 404 error is returned.

```bash
curl localhost:5000/epochs/2023-048T12%3A00%3A00%2E000Z/speed
```

```json
{
  "speed": 7.658223206788738,
  "units": "km/s"
}
```

As expected, the result is the square root of the sum of the squares of the velocity components.
