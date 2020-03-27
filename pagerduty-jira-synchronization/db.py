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


def put_incident_issue_relation(incident_id, issue_key):
    return client.put_item(
        TableName=INCIDENTS_TABLE,
        Item={
            'incidentId': {'S': incident_id },
            'issueKey': {'S': issue_key },
        }
    )


def get_issue_key_by_incident_id(incident_id):
    response = client.query(
        ExpressionAttributeValues={
            ':incident_id': {
                'S': incident_id,
            },
        },
        KeyConditionExpression='incidentId = :incident_id',
        TableName=INCIDENTS_TABLE,
    )
    if response.get('Count', 0) > 0:
        return response.get('Items', [{}])[0].get('issueKey', {}).get('S')
