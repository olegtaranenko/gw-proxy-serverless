import os

import boto3


INCIDENTS_TABLE = os.environ['INCIDENTS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8002'
    )
else:
    client = boto3.client('dynamodb')


def put_incident(incident_id, issue_id):
    return client.put_item(
        TableName=INCIDENTS_TABLE,
        Item={
            'incidentId': {'S': incident_id },
            'issueId': {'S': issue_id },
        }
    )


def put_incident_issue_relation(incident_id, issue_id):
    return client.put_item(
        TableName=INCIDENTS_TABLE,
        Item={
            'incidentId': {'S': incident_id },
            'issueId': {'S': issue_id },
        }
    )


def get_issue_by_incident_id(incident_id):
    resp = client.get_item(
        TableName=INCIDENTS_TABLE,
        Key={
            'incidentId': {
                'S': incident_id,
            }
        }
    )
    item = resp.get('Item')
    if item:
        return item.get('issueId').get('S')
