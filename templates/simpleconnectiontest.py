#!/usr/bin/env python

"""
    Test API connection to Valispace, holds for determined amount of time
    Returns run date.
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
import time

VALISPACE = {
    'domain': 'https://demonstration.valispace.com/',
    'username': 'AutomationsAPI',
    'password': 'AutomationsAPI'
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
            #warn_https=False
        )
    DEFAULT_VALUES["start_date"] = api.get('project/'+str(DEFAULT_VALUES["project"]))['start_date']
    DEFAULT_VALUES["today_date"] = datetime.now().strftime("%Y-%m-%d")
    print (DEFAULT_VALUES["today_date"])
    time.sleep(60)
    print(kwargs)

    pass

if __name__=='__main__':
    main()