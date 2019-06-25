from flask import Flask
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import *
from datetime import datetime

app = Flask(__name__)
CORS(app, resources=r'/*')
client = MongoClient('localhost', 27017) 
collection=client.dou.jiaoyou

@app.route('/')
def index():
  return 'hello!'
  
@app.route('/jiaoyou')
def find_desc():
  search = request.args.get('s')
  results='{}'
  if search!='':
      col=collection.find({'$and':[{'desc':{'$regex':search}},{'invisible':{'$ne':True}}]})
      # for item in col:
      #     item['create_time']=item['create_time'].strftime('%Y-%m-%d %H:%M:%S')
      results=dumps(col)
  return results

@app.route('/jiaoyou/all')
def find_all():
  results=collection.find().limit(10)
  return dumps(results)

@app.route('/jiaoyou/up', methods=['POST'])
def update():
  json=request.json
  # json.pop('_id',None)
  #.strftime('%Y-%m-%dT%H:%M:%S.000Z')
  json['modified_time']=datetime.now()
  results=collection.update_one({'url':json['url']},{'$set':json},upsert=False)
  return ''