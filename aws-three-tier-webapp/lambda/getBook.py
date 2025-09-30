import json
import boto3
from boto3.dynamodb.conditions import Attr

# Configure DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('BookCatalog')  # Table name

def lambda_handler(event, context):
    # Extract parameters from the query string (handling None)
    params = event.get('queryStringParameters') or {}
    title = params.get('title', '')

    # If the user did not provide a title, return an error
    if not title:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Title parameter is required'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://d31opzenb97zag.cloudfront.net'
            }
        }

    # Use scan because the partition key is BookId and we are searching by Title
    response = table.scan(
        FilterExpression=Attr('Title').eq(title)
    )
    items = response.get('Items', [])

    # If no items are found, return a 404 error
    if not items:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Book not found'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://d31opzenb97zag.cloudfront.net'
            }
        }

    # Take the first item found
    book = items[0]

    # Return the found book
    return {
        'statusCode': 200,
        'body': json.dumps(book),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'https://d31opzenb97zag.cloudfront.net'
        }
    }

