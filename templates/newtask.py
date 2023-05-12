#!/usr/bin/env python

"""
    Posts a task assigned to user who triggered it (via automation)
    Should assign object that triggered it
    Functionality not fully developed.
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
from valispace import API
from datetime import datetime, timedelta
import site
site.addsitedir('script_code/') # Required to import other files in script
from .settings import Username, Password # Required to User Secrets defined at Settings


VALISPACE = {
    'domain': 'https://.valispace.com/',
    'username': Username,
    'password': Password
}

DEFAULT_VALUES = {
    "project": 24,
    "start_date": "",
    "today_date": ""    
}

def main(**kwargs):

    api = API(
            url = VALISPACE.get('domain'),
            username = VALISPACE.get('username'),
            password = VALISPACE.get('password')
        )
    DEFAULT_VALUES["start_date"] = api.get('project/'+str(DEFAULT_VALUES["project"]))['start_date']
    DEFAULT_VALUES["today_date"] = datetime.now().strftime("%Y-%m-%d")
    print (DEFAULT_VALUES["today_date"])
    
    #It will get the object (requirement, vali,...) that triggerd the automation
    object_id = kwargs['triggered_objects'][0]['id']

    taskData = {                                
        "title" : "testing Task Creation",
        "project": DEFAULT_VALUES["project"],
        "description" :  "this is the description of the testing tasks",
        "duration" : 5,                                
        "duration_unit" :  "days",                                
        "start_date" :  DEFAULT_VALUES["today_date"],
        "content_type" : 38,
        "object_id": object_id,
        "public" : True
        }
    createdTask = api.post('user-tasks/', data=taskData)
    #here it's adding by default the User with ID #5 to the task. Can be expanded/changed to other users 
    updatedTask = api.request('PUT', 'user-tasks/'+str(createdTask['id'])+"/add-member/", data={"member": "5"})
   
    pass

if __name__=='__main__':
    main()
