"""
Module for IO relevant functions
"""
import sys
import os
import json

def read_json(infile):
    """Reads data from a json file

    Parameters
    ----------
    infile : str
        Full path to json input file

    Returns
    -------
    data : dict
        dict with data
    """
    with open(infile, 'r') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []
    return data
