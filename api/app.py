import json
import os
# import mysql.connector
import datetime
import boto3
from chalice import Chalice

# DBHOST = os.getenv('DBHOST')
# DBUSER = os.getenv('DBUSER')
# DBPASS = os.getenv('DBPASS')
# DB = os.getenv('DB')
# # db=MySQLdb.connect(host=DBHOST,user=DBUSER,passwd=DBPASS,db=DB)
# db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
# cur=db.cursor()

app = Chalice(app_name='api')
ddb = boto3.resource('dynamodb')
table = ddb.Table('songs')

@app.route('/')
def index():
    return {'hello': 'spotify'}

@app.route('/song', methods=['POST'], cors=True)
def new_record():
    print(app.current_request.json_body)
    # payload = app.current_request.json_body
    # print(payload)
    return {'payload':'received'}

@app.route('/songs', methods=['GET'], cors=True)
def get_songs():
    try:
        response = table.scan()
        items = response.get('Items', [])
        
        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
        
        # Convert year from Decimal to integer and sort items by title
        for item in items:
            if 'year' in item:
                item['year'] = int(item['year'])
        
        sorted_items = sorted(items, key=lambda x: x.get('title', '').lower())
            
        return sorted_items
    except Exception as e:
        return {'error': str(e)}, 500

