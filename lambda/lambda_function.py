import json
from amanzi.server.api import AmanziAPI

api = AmanziAPI()

def handler(event, context):

  resp = {}

  # parse path and method
  args = event['path'].split("/")
  method = args[2]

  try:
    if method == 'parameters':
      resp = api.parameters()
    elif method == 'solve':
      resp = api.solve(json.loads(event['body']), args[3])
    elif method == 'report':
      resp = api.report(json.loads(event['body']))
    elif method == 'design':
      resp = api.design(json.loads(event['body']), args[3], args[4])
    elif method == 'keyfigures':
      resp = api.keyfigures()
    elif method == 'version':
      resp = open("VERSION", "r").read()
    else:
      raise ValueError(f"Invalid method: {method}")

    return {
      'statusCode': 200,
      "headers": {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Headers": "*",
          "Access-Control-Allow-Methods": "*"
      },
      "body": resp
    }

  except Exception as e:
    return {
      'statusCode': 500,
      'body': str(e)
    }
