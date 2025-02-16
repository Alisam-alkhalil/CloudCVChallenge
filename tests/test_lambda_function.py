import pytest
import boto3
from moto import mock_dynamodb2
from lambda_function import lambda_handler 

@pytest.fixture
def dynamo_db_table():
    """
    Pytest fixture that creates a DynamoDB table 'VisitorCountTable' for use in unit tests.
    
    The table is created with a single hash key 'id' of type 'S' and provisioned with 5 read and
    write capacity units. The table is cleaned up after each test, so you can assume that it will
    be empty at the start of each test.

    Returns:
        table: A boto3 DynamoDB Table object.
    """
    with mock_dynamodb2():
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

        table = dynamodb.create_table(
            TableName='VisitorCountTable',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'} 
            ],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        yield table


def test_lambda_increment_count(dynamo_db_table):
    """
    Unit test for lambda_handler.

    Verifies that the lambda_handler increments the view count by 1 and returns a 200 status code
    and the expected message when the item 'viewcount' exists in DynamoDB.

    Asserts that the 'Item' exists in DynamoDB and that its count is incremented correctly.
    Asserts that the response status code is 200 and the response body is the expected message.
    """
    dynamo_db_table.put_item(Item={'id': 'viewcount', 'count': 10})
    
    event = {}
    context = {}

    response = lambda_handler(event, context, dynamo_db_table)

    item = dynamo_db_table.get_item(Key={'id': 'viewcount'})
    
    assert 'Item' in item, "Item 'viewcount' not found in DynamoDB"
    assert item['Item']['count'] == 11  # The count should have been incremented to 11
    
    assert response['statusCode'] == 200
    assert response['body'] == '"Hello from Lambda!"'

def test_lambda_initialize_count(dynamo_db_table):

    """
    Unit test for lambda_handler.

    Verifies that the lambda_handler initializes the view count to 1 and returns a 200 status code
    and the expected message when the item 'viewcount' does not exist in DynamoDB.

    Asserts that the 'Item' exists in DynamoDB and that its count is initialized correctly.
    Asserts that the response status code is 200 and the response body is the expected message.
    """
    event = {}
    context = {}

    response = lambda_handler(event, context, dynamo_db_table)

    item = dynamo_db_table.get_item(Key={'id': 'viewcount'})

    assert 'Item' in item, "Item 'viewcount' not found in DynamoDB after Lambda execution"
    assert item['Item']['count'] == 1 

    assert response['statusCode'] == 200
    assert response['body'] == '"Hello from Lambda!"'
