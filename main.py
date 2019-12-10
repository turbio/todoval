import os
from flask import Flask, render_template, request
from db import DB

if 'DB' not in os.environ:
	raise Exception('the DB env var must be set')

db = DB(os.environ['DB'])
count = db.write('''
if (typeof tasks === 'undefined') {
  tasks = []
}

return tasks.length
''')

print('we have', count, 'tasks')

app = Flask('app')

@app.route('/')
def index():
	tasks = db.read('return tasks')
	return render_template('index.html', tasks=tasks)

@app.route('/new', methods=['POST'])
def new():
	db.write(
		'tasks.push(newtask)',
		newtask={ 'name': request.form['name'] },
	)

	return index()

@app.route('/remove/<item>', methods=['POST'])
def remove(item):
	db.write('''
tasks = tasks.slice(0, item).concat(tasks.slice(item + 1))
	''', item=int(item))

	return index()

app.run(host='0.0.0.0', port=8080)