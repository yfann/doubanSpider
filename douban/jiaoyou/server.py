from flask import Flask
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import *
from datetime import datetime
import pymongo

app = Flask(__name__)
CORS(app, resources=r'/*')
client = MongoClient('localhost', 27017) 
collection=client.dou.jiaoyou

@app.route('/')
def index():
  return 'hello!'
  
@app.route('/jiaoyou')
def find_desc():
  keys = request.args.get('s').split(' ')
  hasPhoto = request.args.get('p')
  results='{}'
  keylist=[{'desc':{'$regex':k}} for k in keys if k != '']
  searchParam={'$and':[{'$or':keylist},{'invisible':{'$ne':True}}]}
  if hasPhoto=='true':
      searchParam['$and'].append({'imgs':{"$not":{"$size": 0}}})
      print(searchParam)
  col=collection.find(searchParam).sort('create_time',pymongo.DESCENDING)
  result_list=[]
  for item in col:
      item['create_time']=item['create_time'].strftime('%Y-%m-%d %H:%M:%S')
      result_list.append(item)
  results=dumps(result_list)
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