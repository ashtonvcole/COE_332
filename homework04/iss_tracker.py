#!/usr/bin/env python3

from flask import Flask
import requests
import xmltodict



app = Flask(__name__)



def get_data() -> dict:
    """Get the most recent ISS OEM data.

    This function accesses the most recent Orbital Ephemeris Message for the
    International Space Station available on the NASA website. It parses the
    XML file into a dictionary.

    Args:
        None

    Returns:
        A dictionary of nested lists and dictionaries corresponding to the
            entries in the XML file.
    """
    return xmltodict.parse(requests.get(url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml').text)



@app.route('/', methods = ['GET'])
def all() -> dict:
    """ Get all data.

    This function returns the entire contents of the most recent Orbital
    Ephemeris Message for the International Space Station.

    Args:
        None

    Returns:
        A dictionary of nested lists and dictionaries corresponding to the
            entries in the XML file.
    """
    return get_data()



@app.route('/epochs', methods = ['GET'])
def epochs() -> list:
    """Get data for all epochs.

    This function returns a list of all of the epochs within the most recent
    Orrbital Ephemeris Message for the International Space Station.

    Args:
        None

    Returns:
        A list of dictionaries corresponding to the entries in the XML file.
    """
    data = get_data()
    epochs = []
    for stateVector in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        epochs.append(stateVector['EPOCH'])
    return epochs



@app.route('/epochs/<string:epoch>', methods = ['GET'])
def epochs_state(epoch: str) -> dict:
    """Get state vectors for a specified epoch.

    This function takes in a string representing the desired epoch. If an
    exact match is found in the data set, its state vector is returned.
    Otherwise, the user is given a 404 error.

    Args:
        String representing the desired epoch.

            YYYY-DDDTHH:MM:SS.000Z, or in URL-friendly form
            YYYY-DDDTHH%3AMM%3ASS%2E000Z

    Returns:
        A dictionary of the entire state vector, i.e. EPOCH, X, Y, Z, X_DOT,
        Y_DOT, and X_DOT.
    """
    data = get_data()
    for item in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        if item['EPOCH'] == epoch:
            return item
    else: # No matching epoch
        return f'Epoch {epoch} not found', 404



@app.route('/epochs/<string:epoch>/speed', methods = ['GET'])
def epochs_speed(epoch):
    """Get speed for a specified epoch.

    This function takes in a string representing the desired epoch. If an
    exact match is found in the data set, its calculated speed is returned.
    Otherwise, the user is given a 404 error.

    Args:
        String representing the desired epoch.

            YYYY-DDDTHH:MM:SS.000Z, or in URL-friendly form
            YYYY-DDDTHH%3AMM%3ASS%2E000Z

    Returns:
        A dictionary of the speed in the following form.

            {"speed" : 0, "units" : "km/s"}
    """
    data = get_data()
    for item in data['ndm']['oem']['body']['segment']['data']['stateVector']:
        if item['EPOCH'] == epoch:
            return {'speed' : (float(item['X_DOT']['#text']) ** 2 + \
                    float(item['Y_DOT']['#text']) ** 2 + \
                    float(item['Z_DOT']['#text']) ** 2) ** 0.5, \
                    'units' : item['X_DOT']['@units']}
    else: # No matching epoch
        return f'Epoch {epoch} not found', 404



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')
