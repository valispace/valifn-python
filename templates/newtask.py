#!/usr/bin/env python

"""
    Posts a task assigned to user who triggered it
    Should assign object that triggered it
    Functionality not fully developed.
"""

__author__ = "Gonçalo Ivo"
__copyright__ = "Copyright 2022, Valispace"
__credits__ = ["Gonçalo Ivo"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Valispace"
__email__ = "support@valispace.com"
__status__ = "Development"

from valispace import API
from datetime import datetime, timedelta



VALISPACE = {
    'domain': 'https://.valispace.com/',
    'username': '',
    'password': ''
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
    print(kwargs)
    
    #object_id = triggers[0]['id']

    taskData = {                                
        "title" : "testing Task Creation",
        "project": DEFAULT_VALUES["project"],
        "description" :  "this is the description of the testing tasks",
        "duration" : 5,                                
        "duration_unit" :  "days",                                
        "start_date" :  DEFAULT_VALUES["today_date"],
        "content_type" : 38,
        #"object_id": object_id,
        "object_id": 13700,
        "public" : True
        }
    createdTask = api.post('user-tasks/', data=taskData)
    updatedTask = api.request('PUT', 'user-tasks/'+str(createdTask['id'])+"/add-member/", data={"member": "5"})
   
    pass

if __name__=='__main__':
    main()
