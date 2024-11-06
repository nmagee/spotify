import json
import os
import mysql.connector
import datetime
from chalice import Chalice

DBHOST = os.getenv('DBHOST')
DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')
DB = os.getenv('DB')
# db=MySQLdb.connect(host=DBHOST,user=DBUSER,passwd=DBPASS,db=DB)
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

app = Chalice(app_name='api')

@app.route('/')
def index():
    return {'hello': 'spotify'}

@app.route('/record', methods=['POST'], cors=True)
def new_record():
    print("RECORD POST")
    print(app.current_request.json_body)
    # payload = app.current_request.json_body
    # print(payload)
    return {'payload':'received'}

@app.route('/songs', methods=['GET'], cors=True)
def get_songs():
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre FROM songs INNER JOIN genres ON songs.genre = genres.genreid ORDER BY songs.title, songs.artist;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        db.commit()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        output = json.dumps(json_data)
        return(output)
    except mysql.connector.Error as e:
        print("MySQL Error: ", str(e))
        return None
    cur.close()
    # db.close()

@app.route('/genres', methods=['GET'], cors=True)
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        output = json.dumps(json_data)
        return(output)
    except mysql.connector.Error as e:
        print("MySQL Error: ", str(e))
        return None
    cur.close()
    # db.close()
