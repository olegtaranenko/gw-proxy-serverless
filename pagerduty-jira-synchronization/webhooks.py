import os
import json

import db
import utils


P1_PRIORITY_NAME = 'P1'
severity_field_id = None

def jira(event):
    """
    A webhook function that handles creating or updating of the JIRA tickets.
    """
    print(json.dumps(event, indent=2, sort_keys=True))
    return True



def handle_triggered_incident(message):
    global severity_field_id
    jira = utils.get_jira()
    incident = message.get('incident')
    if incident.get('priority', {}).get('name') != P1_PRIORITY_NAME:
        # Skip all incidents except with P1 priority.
        return
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
        db.put_incident_issue_relation(incident['id'], issue.id)


def handle_resolved_incident(message):
    incident = message.get('incident')
    issue_id = db.get_issue_by_incident_id(incident['id'])
    if issue_id is not None:
        jira = utils.get_jira()
        issue = jira.issue(issue_id)
        jira.transition_issue(issue, '5', resolution={'name': 'Done'})


def pagerduty(event):
    """
    A webhook that should be used by PagerDuty.
    """
    messages = event.get('messages', [])
    for message in messages:
        if message.get('event') == 'incident.trigger':
            handle_triggered_incident(message)
        elif message.get('event') == 'incident.resolve':
            handle_resolved_incident(message)
