import json
import uuid
import os
import boto3
from datetime import datetime


# define the DynamoDB table that Lambda will connect to
tableName = os.environ.get("taskTableName")

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)

print('Loading function')

def lambda_handler(event, context):
    
     # define the functions used to perform the CRUD operations
    def delete_task(task_id):
        response_json = {
            "result": "",
            "statusCode": 400
        }
        try:
            print(f"Task id is: {task_id}")
            response = dynamo.delete_item(Key={
                'id': task_id
            })
            print(f"Delete task response is: {response}")
            response_json['result'] = "Successfully deleted the Task..."
            response_json['statusCode'] = 200
            response_json['data'] = {}

        except Exception as e:
            response_json['result'] = "Failed to delete the Task. " + str(e)
            response_json['statusCode'] = 400
            response_json['data'] = {}
        
        print(f"json response is: {response_json}")
        return response_json

    pathParameters = event.get("pathParameters")
    if pathParameters:
        print("path Param is present...")
        task_id = pathParameters.get("task_id")
        print(f"Task id is: {task_id}")
        response = delete_task(task_id)
    else:
        print("path param not present")
        response = {
            "result": "No such record found!",
            "statusCode": 404,
            "data": {}
        }

    status_code = response.get("statusCode")
    del response['statusCode']

    return {
        "statusCode": status_code,
        "body": json.dumps(response)
    }
