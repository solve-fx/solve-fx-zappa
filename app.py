from flask import Flask, render_template
from dash_application import create_avgcandle

application = Flask(__name__)

create_avgcandle(application)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/api')
def api():
    return {'hello' : 'world'}