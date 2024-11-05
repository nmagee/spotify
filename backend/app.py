import os
import json
import mysql.connector
import datetime
import boto3
from chalice import Chalice

app = Chalice(app_name='backend')
app.debug = True

S3_BUCKET = 'mst3k-dp1-spotify'

baseurl = 'http://mst3k-dp1-spotify.s3-website-us-east-1.amazonaws.com/'

s3 = boto3.client('s3')

@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'])
def s3_handler(event):
  keyhead = event.key
  identifier = keyhead.split('.')
  identifier = identifier[0]
  mp3 = baseurl + identifier + '.mp3'
  print(mp3)
  img = baseurl + identifier + '.jpg'
  print(img)  
  response = s3.get_object(Bucket=S3_BUCKET, Key=event.key)

  app.log.debug("Received new song: %s, key: %s", event.bucket, event.key)

"""
DBHOST = os.getenv('DBHOST')
DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')
DB = os.getenv('DB')
# db=MySQLdb.connect(host=DBHOST,user=DBUSER,passwd=DBPASS,db=DB)
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
"""
