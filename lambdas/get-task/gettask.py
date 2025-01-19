import json
import uuid
import boto3
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr, And


# define the DynamoDB table that Lambda will connect to
tableName = os.environ.get("taskTableName")

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def ddb_get_tasks(user_id):
        response_json = {
            "result": "",
            "statusCode": 400
        }
        try:
            print(f"user id is: {user_id}")
            response = dynamo.scan(FilterExpression=Attr('user.id').eq(user_id))
            print(f"Get question response is: {response}")
            response_json['result'] = "Successfully fetched the tasks..."
            response_json['statusCode'] = 200
            response_json['data'] = response['Items']

        except Exception as e:
            response_json['result'] = "Failed to fetch the tasks. " + str(e)
            response_json['statusCode'] = 400
            response_json['data'] = []
        
        print(f"json response is: {response_json}")
        return response_json

def ddb_get_all_tasks():
        response_json = {
            "result": "",
            "statusCode": 400
        }
        try:
            response = dynamo.scan()
            response_json['result'] = "All the tasks fetched Successfully."
            response_json['statusCode'] = 200
            response_json['data'] = response['Items']

        except Exception as e:
            response_json['result'] = "Failed to fetch tasks " + str(e)
            response_json['statusCode'] = 400
            response_json['data'] = []

        return response_json


def lambda_handler(event, context):
        
    print(f"The event is: {event}")
    print(f"The context is: {context}")
    
    pathParameters = event.get("pathParameters")
    if pathParameters:
        print("path Param is present...")
        user_id = pathParameters.get("user_id")
        print(f"Request id is: {user_id}")
        response = ddb_get_tasks(user_id)
    else:
        print("path param not present")
        response = ddb_get_all_tasks()
    
    status_code = response.get("statusCode")
    del response['statusCode']

    return {
        "statusCode": status_code,
        "body": json.dumps(response)
    }