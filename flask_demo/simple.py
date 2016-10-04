# -*- coding:utf-8 -*-
import os
from flask import Flask, config, request, abort, redirect, url_for, render_template

app = Flask(__name__)
app.config.from_object('config')

loginpath = os.path.join(os.getcwd())

@app.route('/people/')
def people():
	name = request.args.get('name')
	if not name:
		return redirect(url_for('login'))

	user_agent = request.headers.get('User-Agent')
	return 'Name:{0}; UA: {1}'.format(name, user_agent)

@app.route('/login/', methods=['Get', 'POST'])
def login():
	if request.method == 'POST':
		user_id = request.form.get('user_id')
		return 'User: {} login'.format(user_id)
	else:
		return render_template('login.html')

@app.route('/secret/')
def secret():
	abort(401)
	print('This is never executed!')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000, debug=app.debug)
