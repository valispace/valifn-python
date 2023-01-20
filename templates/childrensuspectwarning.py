from ast import Str
from collections.abc import Callable
from xmlrpc.client import Boolean
from valispace import API
import warnings
import time

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
            password = VALISPACE.get('password'),
            warn_https = VALISPACE.get('warn_https', False),
        )

    all_deployment_users = get_map(api, f"user/", "id")

    requirement_data = kwargs['triggered_objects'][0]

    #requirement_data = api.get('requirements/81') #just for testing now without automation to receive the trigger object
    print(requirement_data)
    time.sleep(15)
    
    user_changing_req = all_deployment_users[requirement_data['updated_by']]
    username = user_changing_req['first_name']+" "+user_changing_req['last_name']
    user = f"<span class=\"quill-autocomplete\" host=\"user\" itemid=\"{user_changing_req['id']}\" name=\"{username}\" field=\"displayName\"><user editable=\"true\" itemid=\"{user_changing_req['id']}\" field=\"displayName\">@{username}</user></span>"
    requirement = f"<span class=\"quill-autocomplete\" host=\"requirement\" itemid=\"{requirement_data['id']}\" name=\"{requirement_data['identifier']}\" field=\"identifier\"><requirement editable=\"true\" itemid=\"{requirement_data['id']}\" field=\"identifier\">${requirement_data['identifier']}</requirement></span>"

    print(requirement_data["children"])
    req_children = requirement_data["children"]
    if len(req_children)>0:
        for children in req_children:

            discussionData = {                                
                "title" : user + " -> Parent of "+ requirement + " was updated",
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
