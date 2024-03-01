import os
import boto3

def handler(event, context):
    # Raw event data; kill the favicon hit
    path = event["rawPath"]
    if path != "/":
        return {"statusCode": 404, "body": "Not found."}

    # get a reference to dynamoDB 
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ.get("TABLE_NAME"))   

    # Read the "VISIT COUNT" key (or create it if it doesn't exist)
    response = table.get_item(Key={"key": "visit_count"})
    if "Item" in response:
        visit_count = response["Item"]["value"]
    else:
        visit_count = 0

    # Increment the visit count and write it back to the table.
    new_visit_count = visit_count + 1
    table.put_item(Item={"key": "visit_count", "value": new_visit_count})

    # get current version from .env
    version = os.environ.get("VERSION", "0.0")
    response_body = {
        "message": "Hello World",
        "version": version,
        "visit_count": new_visit_count,
    }
    return {"statusCode": 200, "body": response_body}