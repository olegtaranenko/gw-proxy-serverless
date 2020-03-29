import os

import boto3
from boto3.dynamodb.conditions import Key, Attr

INCIDENTS_TABLE = os.environ['INCIDENTS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8002'
    )
    resource = boto3.resource(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8002'
    )
else:
    client = boto3.client('dynamodb')
    resource = boto3.resource('dynamodb')


def put_incident_issue_relation(incident_id, issue_key):
    return client.put_item(
        TableName=INCIDENTS_TABLE,
        Item={
            'incidentId': {'S': incident_id },
            'issueKey': {'S': issue_key },
        }
    )


def get_issue_key_by_incident_id(incident_id):
    # incidents = resource.Table(INCIDENTS_TABLE)
    response = client.query(
        ExpressionAttributeValues={
            ':incident_id': {
                'S': incident_id,
            },
        },
        KeyConditionExpression='incidentId = :incident_id',
        TableName=INCIDENTS_TABLE,
        # KeyConditionExpression=Key('incidentId)').eq(incident_id),
    )
    if response.get('Count', 0) > 0:
        return response.get('Items')[0].get('issueKey', {}).get('S')


def get_incident_id_by_issue_key(issue_key):
    table = resource.Table(INCIDENTS_TABLE)
    response = table.scan(FilterExpression=Attr('issueKey').eq(issue_key)
    )
    # response = client.scan(
    #     TableName=INCIDENTS_TABLE,
    #     ExpressionAttributeValues={
    #         ':issue_key': {
    #             'S': issue_key,
    #         },
    #     },
    #     FilterExpression='issueKey = :issue_key'
    # )
    if response.get('Count', 0) > 0:
        incident_id = response.get('Items')[0].get('incidentId')
        # print('incident_id', incident_id, )
        return incident_id
