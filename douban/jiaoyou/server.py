from flask import Flask
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import *

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
  if search is not None:
      results=dumps(collection.find({'desc':{'$regex':search}}))
  return results

@app.route('/jiaoyou/all')
def find_all():
  results=collection.find()
  return dumps(results)