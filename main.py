from flask import Flask, request, render_template, redirect, url_for, make_response
import json

from modules.session import Session
from modules.classes import Class
from modules.database import init_db
from urllib.parse import parse_qs

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


@app.route('/getClass', methods=['GET'])
def get_class():
    token = request.cookies['token']
    data = request.query_string.decode('utf-8')
    data = parse_qs(data)
    
    data = {"id": data['id'][0]}
    
    if not data['id']:
        return "Invalid class ID.", 400
    
    class_ = Class(teacher=token, id=data['id'])
    return class_.to_dict(), 200

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    token = request.cookies['token']
    print(data.keys())

    if not data['type'] in errors.keys():
        return "Invalid type.", 400
    
    for key in errors[data['type']].keys():
        if not key in data.keys():
            return errors[data['type']][key], 400
        
    match data['type']:

        case "class":
            new_class = Class(teacher=token, name=data['name'])
            return new_class.to_dict(), 200
        

if __name__ == '__main__':
    app.run(port=5500)
