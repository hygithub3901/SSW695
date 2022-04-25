from flask import render_template
from flask import Blueprint
import json
from flask import url_for

main = Blueprint('main', __name__, template_folder='templates', static_folder='static', static_url_path="/static")

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def index(path):
    return render_template('index.html')

@main.route('/readUserDate')
def read_date():
    filename = 'USER_INFO_EXAMPLE.json'
    with open(filename) as json_file:
        data = json.load(json_file)
        return data