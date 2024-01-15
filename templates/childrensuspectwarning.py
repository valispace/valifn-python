#!/usr/bin/env python

"""
    Takes input from automation that triggers it.
    Automation is triggered by updating a requirement
    Posts discussions to that requirement's children.    
"""

__author__ = "Gonçalo Ivo"
__copyright__ = "Copyright 2024, Valispace"
__credits__ = ["Gonçalo Ivo"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Valispace"
__email__ = "support@valispace.com"
__status__ = "Development"

# Standard packages
from valispace import API
import warnings
import time
import site
site.addsitedir('script_code/') # Required to import other files in script

# Installed packages
from ast import Str
from collections.abc import Callable
from xmlrpc.client import Boolean

VALISPACE = {
    'domain': 'https://deployment_name.valispace.com/',
    'username': '',
    'password': ''
}

DEFAULT_VALUES = {
    "project": PROJECT_ID,
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
            password = VALISPACE.get('password'),
            warn_https = VALISPACE.get('warn_https', False),
        )

    all_deployment_users = get_map(api, f"user/", "id")
    all_project_requirements = get_map(api, f"requirements/?project="+str(DEFAULT_VALUES['project']), "id") 
    requirement_data = kwargs['triggered_objects'][0]

    #requirement_data = api.get('requirements/90') #just for testing now without automation to receive the trigger object
    
    print(requirement_data)
    
    
    print(requirement_data["children"])
    req_children = requirement_data["children"]
    if len(req_children)>0:
        user_changing_req = all_deployment_users[requirement_data['updated_by']]
        username = user_changing_req['first_name']+" "+user_changing_req['last_name']
        requirement = f"<span class=\"quill-autocomplete\" host=\"requirement\" itemid=\"{requirement_data['id']}\" name=\"{requirement_data['identifier']}\" field=\"identifier\"><requirement editable=\"true\" itemid=\"{requirement_data['id']}\" field=\"identifier\">${requirement_data['identifier']}</requirement></span>"

        for children in req_children:
            print(all_project_requirements[children])
            if all_project_requirements[children]['owner'] != None:
                user_owner = all_deployment_users[all_project_requirements[children]['owner']['id']]
                ownername = user_owner['first_name']+" "+user_owner['last_name']
                user = f"<span class=\"quill-autocomplete\" host=\"user\" itemid=\"{user_owner['id']}\" name=\"{ownername}\" field=\"displayName\"><user editable=\"true\" itemid=\"{user_owner['id']}\" field=\"displayName\">@{ownername}</user></span>"
            else:
                user = f"<span class=\"quill-autocomplete\" host=\"user\" itemid=\"{user_changing_req['id']}\" name=\"{username}\" field=\"displayName\"><user editable=\"true\" itemid=\"{user_changing_req['id']}\" field=\"displayName\">@{username}</user></span>"
        
            discussionData = {                                
                "title" : user + " -> The Parent "+ requirement + " of this requirement was updated",
                "project": DEFAULT_VALUES["project"],
                "content_type" :  120,                             
                "group": 1,
                "object_id": children,
                }
            createdDiscussion = api.post('discussions/', data=discussionData)

    print("Discussions created for each Children")
    
    pass

if __name__=='__main__':
    main()
