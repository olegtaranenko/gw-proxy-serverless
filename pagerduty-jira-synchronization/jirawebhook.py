import os
import json
import requests
import db

PAGERDUTY_SERVER_URL = os.environ['PAGERDUTY_SERVER_URL'] + '/incidents'


def jira(event):
    """
    A webhook function which basically triggered by changing the
    JIRA Ticket to Done state.
    """
    # print(json.dumps(event, indent=2, sort_keys=True))
    changelog = event.get('changelog', {})
    changes = changelog.get('items', [{}])

    has_done = False
    for item in changes:
        if item.get('fieldId') == 'status' and item.get('toString') == 'Done':
            has_done = True
            break

    issue_key = None
    if has_done:
        issue_key = event.get('issue', {}).get('key')
    if issue_key is not None:
        incident_key = db.get_incident_id_by_issue_key(issue_key)
        payload = {
            'incidents': [{
                'id': incident_key,
                'type': 'incident',
                'status': 'resolved',
            }]
        }
        token_key = os.environ['PAGERDUTY_TOKEN_KEY']
        email = os.environ['PAGERDUTY_USER_EMAIL']
        headers = {
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Authorization': 'Token token=' + token_key,
            'From': email,
            'Content-Type': 'application/json'
        }
        response = requests.put(PAGERDUTY_SERVER_URL, json=payload,
                                headers=headers)
        # if response.status_code != 200:
            # raise exception ?