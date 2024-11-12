import os
import json
import time
import boto3
import requests
from chalice import Chalice

app = Chalice(app_name='grader')
s3 = boto3.client('s3')
ddb = boto3.client('dynamodb')
cwl = boto3.client('logs')

@app.route('/')
def index():
  return {'hello': 'grader'}

@app.route('/grader', methods=['POST'], cors=True)
def grade_submission():
  payload = app.current_request.json_body
  # We'll echo the json body back to the user in a 'user' key.
  # print(payload)
  bucket = payload['bucket']
  # os.chdir('vendor')
  files = ["8cijpjpy.json", "8cijpjpy.jpg", "8cijpjpy.mp3"]
  for file in files:
    upload(bucket, file)
  api = payload['api']
  check_api(api, bucket)
  return {'payload': payload}

def upload(bucket, file):
  try:
    with open(file, 'rb') as fileread:
      response = s3.put_object(
        Body=fileread,
        Bucket=bucket,
        Key=file,
      )
      # s3.upload_fileobj(file, bucket, file)
      print(f"File {file} uploaded to {bucket}/{file}.")
  except Exception as e:
    print(f"Error uploading file to S3: {e}")

def check_api(api, bucket):
  time.sleep(10)
  response = requests.get(api)
  rbody = response.text
  # print(rbody)
  uid = bucket.rstrip("-dp1-spotify")
  if "8cijpjpy" in response.text:
    write_log(bucket, api, uid, "SUCCESS")
    put_ddb(bucket, api, uid, "SUCCESS")
  else:
    write_log(bucket, api, uid, "FAILURE")
    put_ddb(bucket, api, uid, "FAILURE")

def put_ddb(bucket, api, uid, status):
  try:
    response = ddb.put_item(
        Item={
            'bucket': {
                'S': bucket,
            },
            'api': {
                'S': api,
            },
            'uid': {
                'S': uid,
            },
            'status': {
                'S': status,
            },
        },
        TableName='dp1-spotify',
    )
  except Exception as e:
    print(f"Error with put in DynamoDB: {e}")

def write_log(bucket, api, uid, status):
  try:
    response = cwl.put_log_events(
        logGroupName='dp1-spotify-lg',
        logStreamName='submissions',
        logEvents=[
            {
                'timestamp': int(round(time.time() * 1000)),
                'message': uid + " - " + status + " - " + bucket + " - " + api,
            },
        ],
    )
  except Exception as e:
    print(f"Error with put in CloudWatch Logs: {e}")