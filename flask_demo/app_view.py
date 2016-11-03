# -*- coding:utf-8 -*-

from flask import Flask, request, render_template
from flask.views import view

app = Flask(__name__, template_folder='templates')


class BaseView(View):
	def get_template(self):
		raise NotImplementedError()

	def render_template(self, context):
		return render_template(self.get_template(), **context)

	def dispatch_request(self):
		if request.method != 'GET':
			return 'UNSUPPORTED!'
		
		context = {'user': self.get_users()}
		return self.render_template(context)


class UserView(BaseView):
	def get_template_name(self):
		return 'users.html'

	def get_users(self):
		return [{
			'username': 'fake',
			'avatar': 'http://lorempixel.com/100/100/nature/'
		}]

app.add_url_rule('/users', view_func=UserView.as_view('userview'))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9000)

