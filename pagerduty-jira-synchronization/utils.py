import os

from jira import JIRA


jira = None


def get_jira():
    global jira
    if jira is None:
        options = {
            'server': os.environ['JIRA_SERVER_URL'],
        }
        basic_auth = (
            os.environ['JIRA_USER_EMAIL'],
            os.environ['JIRA_API_TOKEN'],
        )
        jira = JIRA(options, basic_auth=basic_auth)
    return jira
