import os

from jira import JIRA


P1_PRIORITY_NAME = 'P1'


def pagerduty(event, context):
    """
    A webhook function that should be used by PagerDuty.
    """
    
    
    options = {
        'server': os.environ['JIRA_SERVER_URL'],
    }
    basic_auth = (
        os.environ['JIRA_USER_EMAIL'],
        os.environ['JIRA_API_TOKEN'],
    )
    jira = JIRA(options, basic_auth=basic_auth)
    messages = event.get('body', {}).get('messages', [])
    for message in messages:
        if message.get('event') != 'incident.trigger':
            # Ignore all incidents except newly created/triggered.
            continue
        incident = message.get('incident')
        if incident.get('priority', {}).get('name') != P1_PRIORITY_NAME:
            # Skip all incidents except with P1 priority.
            continue
        entries = message.get('log_entries', [])
        for entry in entries:
            issue_dict = {
                'project': {'key': os.environ['JIRA_PROJECT_KEY']},
                'summary': entry['channel']['summary'],
                'description': entry['channel']['details'],
                'issuetype': {'name': 'Bug'},
                'priority': {'name': 'Highest'},
            }
            jira.create_issue(fields=issue_dict)
