import os
import json

# import db
# import utils

def jira(event):
    """
    A webhook function which basically triggered by changing the JIRA Ticket to Done state.
    """
    print(json.dumps(event, indent=2, sort_keys=True))
    return True
