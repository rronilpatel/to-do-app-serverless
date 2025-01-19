import json
import uuid
import os
import boto3
from datetime import datetime

# define the DynamoDB table that Lambda will connect to
tableName = os.environ.get("userTableName")

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)


def list_topics():
    sns = boto3.resource("sns")
    topics_iter = sns.topics.all()
    return topics_iter


def subscribe(protocol, endpoint):
    to_do_topic = ""
    for topic in list_topics():
        if "todo-list-deadline-scheduler" in topic.arn:
            to_do_topic = topic
            break
    subscription = to_do_topic.subscribe(Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
    print(f'subscription is : {subscription}')
    return subscription


def lambda_handler(event, context):
    
    def ddb_create(x):
        x['id'] = str(uuid.uuid1())
        x['is_admin'] = False
        x['role'] = "user"
        
        response_json = {
            "result": "",
            "statusCode": 400
        }
    
        try:
            response = dynamo.put_item(Item=x)
            response_json['result'] = "Successfully Registered User"
            response_json['statusCode'] = 201
            subscribe("email", x.get("email"))
    
        except Exception as e:
            response_json['result'] = "Failed to register user. " + str(e)
            response_json['statusCode'] = 400
    
        return response_json

    response = ddb_create(event)
    
    status_code = response.get("statusCode")
    del response['statusCode']
    
    return {
        'statusCode': status_code,
        'body': response,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
    }
