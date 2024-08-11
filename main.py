from flask import Flask, request, render_template, redirect, url_for, make_response
import json

from modules.session import Session
from modules.database import get_db_connection, init_db

with open('errors.json', 'r') as f:
    errors = json.load(f)

init_db()

##### Flask application #####

app = Flask(__name__)

@app.route('/', methods=['GET'])
def start():
    if not "token" in request.cookies:
        session = Session()
        response = make_response('setting token')
        response.set_cookie('token', session.id) # very important
        return response
    else:
        session = Session(request.cookies['token'])
    
    return render_template('index.html', session=session.to_dict())

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    # TODO check session
    print(data.keys())
    if not data['type'] in errors.keys():
        return "Invalid type.", 400
    for key in errors[data['type']].keys():
        if not key in data.keys():
            return errors[data['type']][key], 400
        
    match data['type']:

        case "class":
            #create_class(data)
            return 500
        

if __name__ == '__main__':
    app.run(port=5500)
