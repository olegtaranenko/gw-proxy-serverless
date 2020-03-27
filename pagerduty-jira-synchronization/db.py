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
