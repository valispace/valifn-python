#!/usr/bin/env python

"""
    Can take input from automation or be triggered manually
    Returns string placed on predefined Dashboard 
    text blocks with calculated test run statistics.
"""

__author__ = "Gonçalo Ivo"
__copyright__ = "Copyright 2022, Valispace"
__credits__ = ["Gonçalo Ivo"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Valispace"
__email__ = "support@valispace.com"
__status__ = "Development"

# Standard packages
import csv, json
from valispace import API

import warnings
import urllib.request
import site
site.addsitedir('script_code/') # Required to import other files in script
from .settings import Username, Password # Required to User Secrets defined at Settings

from ast import Str
from collections.abc import Callable
from xmlrpc.client import Boolean

VALISPACE = {
    'domain': 'https://.valispace.com/',
    'username': Username,
    'password': Password
}

DEFAULT_VALUES = {
    "project": 24, 
}

def get_map(api: API, endpoint: Str = "/", name: Str = "id", name_map_func: Callable[[Str], Boolean] = None, filter_func: Callable[[Str], Boolean]= None):
    """
    Function that given an endpoint returns a dict with specific keys.
    If function is provided it generates the key. name_map_func must receive an object instance.
    Otherwise key will be the property of each object specified in name.
    """
    mapping = {}
    if not name_map_func:
        name_map_func = lambda x: x[name]
    for inst in api.get(endpoint):
        if filter_func and not filter_func(inst):
            # Filtered out
            continue

        key = name_map_func(inst)
        if not mapping.get(key):
            mapping[key] = inst
        else:
            warnings.warn(f"Warning ---> Key: {key} already has an object. Some data may be lost in mapping.")
    return mapping

def main(**kwargs):

    api = API(
            url = VALISPACE.get('domain'),
            username = VALISPACE.get('username'),
            password = VALISPACE.get('password')
        )
    
    all_project_test_runs = get_map(api, f"testing/test-runs/?project="+str(DEFAULT_VALUES["project"]), "id")

    pass_runs = 0
    failed_runs = 0

    for run in all_project_test_runs:
        if all_project_test_runs[run]['status'] == 50:
            pass_runs += 1
        elif all_project_test_runs[run]['status'] == 40:
            failed_runs += 1

    #The following lines will place the Passed and Failed information into two text blocks a Dashboard. It can, for example, also be placed in an Analysis block or Valis.
    api.request('patch', "dashboards/blocks/blocktext/12/", {"text": "Number of Passed Test Runs ->  "+ str(pass_runs) + "<p>new line</p>"})    
    api.request('patch', "dashboards/blocks/blocktext/13/", {"text": "Number of Failed Test Runs ->  "+ str(failed_runs)})
    pass

if __name__=='__main__':
    main()
