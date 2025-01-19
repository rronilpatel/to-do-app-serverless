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

def publish_message(topic, message):
    response = topic.publish(Message=message)
    message_id = response['MessageId']
    return message_id


def get_task(task_id):
    task = None
    
    try:
        print(f"task id is: {task_id}")
        response = dynamo.scan(FilterExpression=Attr('id').eq(task_id))
        print(f"Get Task response is: {response}")
        task = response["Items"]
        if task:
            task = task[0]
    except Exception as e:
        print(str(e))
        task = None
    
    return task


def list_topics():
    sns = boto3.resource("sns")
    topics_iter = sns.topics.all()
    return topics_iter


def publish_notification(task):
    to_do_topic = ""
    for topic in list_topics():
        if "todo-list-deadline-scheduler" in topic.arn:
            to_do_topic = topic
            break

    notification_message = "Congratulations on completing the Task \n\n" + json.dumps(task)
    task_info = "Hey " + task.get("user").get("name") + "! You have completed the Task with following information: " + f"\n\nTask Title: {task.get('title')} \n" + f"Task Description: {task.get('description')} \n" + f"Task Date: {task.get('date')} \n" + f"Task Time: {task.get('time')} \n" + f"Task Priority: {task.get('priority')} \n" + "\n\nKeep doing the great work!!"
    response = to_do_topic.publish(Message=task_info, Subject="Congratulations on Completing the Task")
    message_id = response['MessageId']
    print(f"message id is: {message_id}")
    return message_id


def check_for_task_completion(current_status, updated_status):

    if current_status == "incomplete" and updated_status == "complete":
        return True

    return False


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
            response_json['result'] = "Successfully updated the Task."
            response_json['statusCode'] = 201

        except Exception as e:
            response_json['result'] = "Failed to update task. " + str(e)
            response_json['statusCode'] = 400

        return response_json
    
    request_body = json.loads(event.get('body'))
   
    task_id = request_body.get("task_id")
    updated_status = request_body.get("status")

    task = get_task(task_id)
    current_status = task.get("status")
    
    task["status"] = updated_status
    response = ddb_create(task)

    should_notify = check_for_task_completion(current_status, updated_status)

    if should_notify:
        publish_notification(task)

    status_code = response.get("statusCode")
    del response['statusCode']
    
    return {
        "statusCode": status_code,
        "body": json.dumps(response)
    }

