import json
import requests
import os

def handler(event, context):
  print('received event:')
  print(event)

  response = requests.get( os.getenv('FETCH_IMAGES_HOST') + '/all_files')
  print(response.text)
  body = json.loads(response.text)

  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps(body)
  }


if __name__ == "__main__":
  print(handler(None, None))
