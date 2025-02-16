import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('VisitorCountTable')

def lambda_handler(event, context, table=table):
    """
    Lambda function that handles updating a view count in a DynamoDB table.

    This function is triggered by an API Gateway event. It attempts to retrieve the current 
    view count from a DynamoDB table with the primary key 'viewcount'. If the item exists, 
    the count is incremented by 1 and updated in the table. If the item does not exist, 
    it initializes the count to 1 in the table.

    Args:
        event (dict): A dictionary containing the event data from API Gateway.
        context (object): An object providing methods and properties that provide 
                          information about the invocation, function, and execution 
                          environment.

    Returns:
        dict: A dictionary containing the status code and a message.
    """

    try:
        response = table.get_item(Key={"id": "viewcount"})  

        current_value = response["Item"]["count"]

        new_value = current_value + 1

        table.update_item(
            Key={"id": "viewcount"},
            UpdateExpression="SET #count = :new_value",
            ExpressionAttributeNames={
                "#count": "count"
            },
            ExpressionAttributeValues={
                ":new_value": new_value
            }
        )
    except KeyError:
        table.put_item(
            Item={
                'id': 'viewcount',
                'count': 1
            }
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
