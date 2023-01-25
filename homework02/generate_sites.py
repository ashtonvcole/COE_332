#!/usr/bin/env python3

import json
import random

def main():
    # Create a dictionary
    data = {}
    # Create a list associated with sites
    data['sites'] = []
    # Append objects to the list within the dictionary
    for i in range(5):
        # Create a dictionary object
        data['sites'].append({ \
                'site_id' : (i + 1), \
                'latitude' : random.random() * 2.0 + 16.0, \
                'longitude' : random.random() * 2.0 + 82.0, \
                'composition' : random.choice(['stony', 'iron', 'stony-iron']) \
                })
    with open('sites.json', 'w') as f:
        json.dump(data, f, indent = 2)

if __name__ == "__main__":
    main()
