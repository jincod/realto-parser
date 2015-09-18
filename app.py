from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import Flask, redirect, render_template, url_for, request
import tasks
import json

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/realto')
db = client.get_default_database()

configurations = db.configurations
items = db.items

@app.route('/')
def configs():
	return render_template('index.html',
		configs = configurations.find({}))

@app.route('/execute/<config_id>', methods=['POST'])
def execute(config_id):
	config = configurations.find_one({'_id': ObjectId(config_id)})
	config['id'] = config_id;
	config['_id'] = config_id;
	# clear items
	items.remove({'config_id': config_id}, multi=True)
	tasks.process_new_config.delay(config)

	return redirect(url_for('config', config_id = config_id))

@app.route('/config/<config_id>')
def config(config_id):
	config = configurations.find_one({'_id': ObjectId(config_id)})
	return render_template('config.html',
		items = items.find({'config_id': config_id}),
		configuration = dumps(config))

@app.route('/add-json', methods=['POST'])
def add_configuration_json():
	config = json.loads(request.form.get('configuration'))
	configurations.insert(config)
	return redirect(url_for('configs'))


if __name__ == "__main__":
    app.run(debug=True)