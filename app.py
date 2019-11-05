import os
import atexit

from flask import Flask, jsonify,Response
from flask_pymongo import PyMongo
from bson.json_util import dumps,json
from bson.objectid import ObjectId
from bson import json_util
import time

from confluent_kafka import Producer

from confluent_kafka import Consumer, KafkaError
from threading import Thread


from bson import ObjectId
from flask.json import JSONEncoder
from werkzeug.routing import BaseConverter

from apscheduler.schedulers.background import BackgroundScheduler

#from flask_objectid_converter import ObjectIDConverter

class ObjectIdConverter(BaseConverter):
    def to_python(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)


p = Producer({'bootstrap.servers': 'localhost:9092'})
def delivery_report(err, msg):
	if err is not None:
		print('Message delivery failed: {}'.format(err))
	else:
		print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


consumer_poll = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'latest',
    'api.version.request': True

})

consumer_poll.subscribe(['mytopic'])

app = Flask(__name__)
app.secret_key = "narendra"

app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

app.url_map.converters['ObjectId'] = ObjectIdConverter


scheduler = BackgroundScheduler(daemon=True)


@scheduler.scheduled_job('interval', id='id', seconds=10)
def job_function():
	consumer_msg = consumer_poll.poll(timeout=1.0)
	if consumer_msg is None:
		print("consumer_msg is none")
	elif consumer_msg.error():
		print("Consumer error: {}".format(consumer_msg.error()))
	else:
		print("\n")
		print('Consumer Received message: {}'.format(consumer_msg.value().decode('utf-8')))
		print("\n")
		task=json.loads(consumer_msg.value().decode('utf-8'))
		print("unique_identifier: ",task['unique_identifier']['$oid'])
		print("\n")
		identifier=task['unique_identifier']['$oid']
		data=task['number1'] + task['number2']
		mongo.db.users.update_one({'_id':ObjectId(identifier)},{
			"$set": {"answer":data}
			})

scheduler.start()  	



@app.route("/",methods=['GET'])
def home_page():
	return jsonify(string="Hi from test API"),200



@app.route("/calculate/<int:num1>/<int:num2>",methods=['GET'])
def new(num1,num2):
    online_users = mongo.db.users.insert({"number1":num1,"number2":num2,"answer":""})
    print("online_users_id:    ",online_users)
    p.poll(0)
    data=dumps({"number1":num1,"number2":num2,"unique_identifier":online_users})
    p.produce('mytopic', data.encode('utf-8'), callback=delivery_report)
    p.flush()
    #mongo.db.consumer.insert(consumer_msg)
    return jsonify(identifier=str(online_users)),200


@app.route("/get_answer/<ObjectId:identifier>")
def get_answer(identifier):
	print("\n")
	print("\n")
	print("\n")
	print("unique_identifier:  ",identifier)
	identifier=str(identifier)
	#task = mongo.db.users.find_one_or_404({'_id':ObjectId(identifier)})
	task = mongo.db.users.find_one({'_id':ObjectId(identifier)})
	print("get_answer_route:      ",task)
	print("\n")


	if task != None:
		if task["answer"]=="":
			return app.response_class(
				response=dumps({"string":"Please wait"}),
				status=200,
				mimetype='application/json')
	else:
		return jsonify(string="identifier entry does not exist in the database"),404

	response = app.response_class(
		response=dumps(task),status=200,mimetype='application/json')
	return response

	
atexit.register(lambda: scheduler.shutdown(wait=False))

if __name__=="__main__":
	app.run(debug=True)
