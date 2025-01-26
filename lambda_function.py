import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CVViewCount')

def lambda_handler(event, context):
    
    response = table.get_item(Key={"views": "viewcount"})  

    current_value = response["Item"]["count"]

    new_value = current_value + 1

    table.update_item(
        Key={"views": "viewcount"},
        UpdateExpression="SET #count = :new_value",
        ExpressionAttributeNames={
            "#count": "count"
        },
        ExpressionAttributeValues={
            ":new_value": new_value
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
