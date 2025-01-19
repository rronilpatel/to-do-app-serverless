import json
import uuid
import boto3
import os
from datetime import datetime


# define the DynamoDB table that Lambda will connect to
tableName = os.environ.get("taskTableName")

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def lambda_handler(event, context):
    
     # define the functions used to perform the CRUD operations
    def ddb_create(x):
        if x.get("id"):
            pass
        else:
            x['id'] = str(uuid.uuid1())
        x['created_at'] = str(datetime.now())
        response_json = {
            "result": "",
            "statusCode": 400
        }

        try:
            response = dynamo.put_item(Item=x)
            response_json['result'] = "Successfully added the Task."
            response_json['statusCode'] = 201

        except Exception as e:
            response_json['result'] = "Failed to add task. " + str(e)
            response_json['statusCode'] = 400

        return response_json

    response = ddb_create(event)
    
    return response
