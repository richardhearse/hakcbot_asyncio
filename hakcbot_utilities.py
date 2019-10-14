#!/usr/bin/env python3

import os
import json

#will load json data from file, convert it to a python dict, then return as object
def load_from_file(filename):
    with open(f'{filename}', 'r') as settings:
        settings = json.load(settings)

    return settings

def write_to_file(data, filename, folder='data'):
    with open(f'{filename}', 'w') as settings:
        json.dump(data, settings, indent=4)