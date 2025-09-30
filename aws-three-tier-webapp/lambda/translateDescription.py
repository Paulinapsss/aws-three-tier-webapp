import json
import boto3

# Amazon Translate client
translate = boto3.client('translate', region_name='eu-north-1')

# Allowed languages
allowed_languages = ['it', 'pl', 'ru']

# CORS headers
CORS_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': 'https://d31opzenb97zag.cloudfront.net',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
}

def lambda_handler(event, context):
    # Parse body from request (handling None)
    body = json.loads(event.get('body') or '{}')
    text = body.get('text', '')
    target_lang = body.get('targetLang', 'it')  # default to Italian

    # Validate target language
    if target_lang not in allowed_languages:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Invalid target language. Choose one of {allowed_languages}'}),
            'headers': CORS_HEADERS
        }

    # Check if text is provided
    if not text:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Text is required'}),
            'headers': CORS_HEADERS
        }

    # Call Amazon Translate
    result = translate.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=target_lang
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'translatedText': result['TranslatedText']}),
        'headers': CORS_HEADERS
    }
