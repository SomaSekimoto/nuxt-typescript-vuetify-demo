import requests
import os
import json

def handler(event, context):
  print('received event:')
  print(event)
  startDate = '2021-03-06'
  endDate = '2021-03-07'
  # token = os.getenv("MAYU_DELIVERY_TOKEN")
  url = f'{os.getenv("FETCH_IMAGES_HOST")}/fetch_files?from={startDate}&to={endDate}&token={os.getenv("MAYU_DELIVERY_TOKEN")}'

  response = requests.get(url)
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
