import os

def handler(event, context):
    response_body = {
            version = os.environ.get("VERSION", "0.0")
            "message": "Hello World",
            "version": version
        }
    return response_body