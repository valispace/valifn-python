import csv, json
from valispace import API

import warnings
import os
import urllib.request
import time

from ast import Str
from collections.abc import Callable
from xmlrpc.client import Boolean

VALISPACE = {
    'domain': 'https://demonstration.valispace.com/',
    'username': 'AutomationsAPI',
    'password': 'AutomationsAPI'
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
    
    all_project_requirements = get_map(api, f"requirements/complete/?project="+str(DEFAULT_VALUES["project"]), "id")

    nr_reqs = 0 #15093
    nr_req_w_children = 0 #15094
    nr_req_w_vm = 0 #15095
    nr_req_vm_analysis = 0 #15099
    nr_req_vm_review = 0 #15100
    nr_req_vm_inspection = 0 #15101
    nr_req_vm_rules = 0 #15102
    nr_req_vm_tests = 0 #15103
    nr_req_state_draft = 0 #15096
    nr_req_state_in_review = 0 #15097
    nr_req_state_final = 0 #15098
    nr_req_verified = 0 #15104
    nr_req_not_verified = 0 #15105

    nr_reqs = len(all_project_requirements)

    for requirement in all_project_requirements:
        req_data=all_project_requirements[requirement]
        
        if req_data['verified'] == True:
            nr_req_verified += 1
        elif req_data['verified'] == False:
            nr_req_not_verified += 1

        if req_data['total_children'] != 0:
            nr_req_w_children += 1
        
        if req_data['state'] == 7: #but for other projects we need to get by state name
            nr_req_state_draft += 1
        elif req_data['state'] == 8:
            nr_req_state_in_review += 1
        elif req_data['state'] == 9:
            nr_req_state_final += 1

        if req_data['verification_methods'] != None:
            nr_req_w_vm += 1
            for vm in req_data['verification_methods'] :                
                if vm['method'] != None:
                    vm_name = vm['method']['name']
                    if vm_name == "Analysis":
                        nr_req_vm_analysis += 1
                    elif vm_name == "Inspection":
                        nr_req_vm_inspection += 1
                    elif vm_name == "Review":
                        nr_req_vm_review += 1
                    elif vm_name == "Rules":
                        nr_req_vm_rules += 1
                    elif vm_name == "Test":
                        nr_req_vm_tests += 1

    print("going to patch")
    time.sleep(15)

    api.request("patch", "valis/15093/", data={"formula":nr_reqs})
    api.request("patch", "valis/15094/", data={"formula":nr_req_w_children})
    api.request("patch", "valis/15095/", data={"formula":nr_req_w_vm})    
    api.request("patch", "valis/15096/", data={"formula":nr_req_state_draft})
    api.request("patch", "valis/15097/", data={"formula":nr_req_state_in_review})
    api.request("patch", "valis/15098/", data={"formula":nr_req_state_final})    
    api.request("patch", "valis/15099/", data={"formula":nr_req_vm_analysis})
    api.request("patch", "valis/15100/", data={"formula":nr_req_vm_review})
    api.request("patch", "valis/15101/", data={"formula":nr_req_vm_inspection})
    api.request("patch", "valis/15102/", data={"formula":nr_req_vm_rules})
    api.request("patch", "valis/15103/", data={"formula":nr_req_vm_tests})
    api.request("patch", "valis/15104/", data={"formula":nr_req_verified})
    api.request("patch", "valis/15105/", data={"formula":nr_req_not_verified})

    pass

if __name__=='__main__':
    main()
