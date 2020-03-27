import os

from jira import JIRA

import db


P1_PRIORITY_NAME = 'P1'


def pagerduty(event):
    """
    A webhook that should be used by PagerDuty.
    """
    options = {
        'server': os.environ['JIRA_SERVER_URL'],
    }
    basic_auth = (
        os.environ['JIRA_USER_EMAIL'],
        os.environ['JIRA_API_TOKEN'],
    )
    jira = JIRA(options, basic_auth=basic_auth)
    severity_field_id = None
    messages = event.get('messages', [])
    for message in messages:
        if message.get('event') != 'incident.trigger':
            # Ignore all incidents except newly created/triggered.
            continue
        incident = message.get('incident')
        if incident.get('priority', {}).get('name') != P1_PRIORITY_NAME:
            # Skip all incidents except with P1 priority.
            continue
        if severity_field_id is None:
            fields = jira.fields()
            severity_fields = [f for f in fields if f['name'] == 'Severity']
            severity_field_id = severity_fields[0]['id']
        entries = message.get('log_entries', [])
        severity_field_value = 'SEV-0'
        for entry in entries:
            issue_dict = {
                'project': {'key': os.environ['JIRA_PROJECT_KEY']},
                'summary': entry['channel']['summary'],
                'description': entry['channel']['details'],
                'issuetype': {'name': 'Bug'},
                'priority': {'name': 'Highest'},
            }
            if severity_field_id:
                issue_dict[severity_field_id] = {'value': severity_field_value}
            issue = jira.create_issue(fields=issue_dict)
            db.put_incident(incident['id'], issue.id)
