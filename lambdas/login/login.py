import json
import uuid
import os
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr, And

# define the DynamoDB table that Lambda will connect to
tableName = os.environ.get("userTableName")

# create the DynamoDB resource
dynamo = boto3.resource('dynamodb').Table(tableName)


def lambda_handler(event, context):
    
    def ddb_get_user(x):

        response_json = {
            "result": "",
            "statusCode": 400
        }
        try:
            email = x.get("email")
            response = dynamo.scan(FilterExpression=Attr('email').eq(email))
            print(f"The user is: {response}")

            user_obj = response['Items'][0] if response['Items'] else {}
            print(f"user_obj is : {user_obj}")

            if user_obj.get("password") == x.get("password"):
                msg = "Successfully Logged in user"
            else:
                msg = "Invalid user id or password!"
                user_obj = []
                
            response_json['result'] = msg
            response_json['statusCode'] = 200
            response_json['data'] = [user_obj] if user_obj else []

        except Exception as e:
            response_json['result'] = str(e)
            response_json['statusCode'] = 400
            response_json['data'] = []
        
        print(f"json response is: {response_json}")
        return response_json

    response = ddb_get_user(event)
    
    status_code = response.get("statusCode")
    del response['statusCode']
    
    return {
        'statusCode': status_code,
        'body': response
    }
