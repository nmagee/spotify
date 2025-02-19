import os
import json
import mysql.connector
import boto3
from chalice import Chalice

app = Chalice(app_name='backend')
app.debug = True

# s3 things
S3_BUCKET = 'nem2p-dp1-spotify'
s3 = boto3.client('s3')
ddb = boto3.resource('dynamodb')
table = ddb.Table('songs')

# base URL for accessing the files
baseurl = 'http://nem2p-dp1-spotify.s3-website-us-east-1.amazonaws.com/'

# file extensions to trigger on
_SUPPORTED_EXTENSIONS = (
    '.json'
)

# ingestor lambda function
@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'])
def s3_handler(event):
  if _is_json(event.key):
    # get the file, read it, load it into JSON
    response = s3.get_object(Bucket=S3_BUCKET, Key=event.key)
    text = response["Body"].read().decode()
    data = json.loads(text)

    # parse out the data fields 1-by-1
    TITLE = data['title']
    ALBUM = data['album']
    ARTIST = data['artist']
    YEAR = data['year']
    GENRE = data['genre']

    # get the unique ID for the bundle to build the mp3 and jpg urls
    keyhead = event.key
    identifier = keyhead.split('.')
    ID = identifier[0]
    MP3 = baseurl + ID + '.mp3'
    IMG = baseurl + ID + '.jpg'

    app.log.debug("Received new song: %s, key: %s", event.bucket, event.key)

    # try to insert the song into the database
    try:
        response = table.put_item(
            Item={
                'id': ID,
                'title': TITLE,
                'album': ALBUM,
                'artist': ARTIST,
                'year': YEAR,
                'genre': GENRE,
                'file': MP3,
                'image': IMG
            }
        )
        return {
            'statusCode': 200,
            'body': f'Successfully inserted song {TITLE} into DynamoDB'
        }
    except Exception as e:
        print(e)
        app.log.error(f"Error inserting into DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error inserting into DynamoDB: {str(e)}'
        }

# performs suffix matching against the tuple of supported extensions
def _is_json(key):
  return key.endswith(_SUPPORTED_EXTENSIONS)
