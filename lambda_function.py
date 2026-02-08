import boto3
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("EmpTable")  # type: ignore


def lambda_handler(event, context):
    path = event.get("path")
    method = event.get("httpMethod")

    if method == "POST" and path == "/employee":
        body = json.loads(event["body"])
        table.put_item(Item=body)
        return response(201, {"message": "Employee created successfully"})
    elif method == "GET" and path == "/employee":
        empId = event["queryStringParameters"]["empId"]

        if not empId:
            return response(400, {"error": "Missing empId"})

        result = table.get_item(Key={"empId": empId})
        item = result["Item"]
        print(f"Retrieved record: {item}")

        if item:
            return response(200, item)

        return response(404, {"error": "Employee not found"})


def response(statusCode, body):
    return {"statusCode": statusCode, "body": json.dumps(body)}
