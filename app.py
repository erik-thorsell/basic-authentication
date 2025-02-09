from flask import Flask, request, render_template, redirect, url_for, make_response
import json

# import modules
from modules.session import Session
from modules.classes import Class
from modules.database import init_db
from urllib.parse import parse_qs

# load error messages
with open('errors.json', 'r') as f:
    errors = json.load(f)

init_db() # initialize the database

##### Flask application #####

app = Flask(__name__) # create a new Flask application

@app.route('/', methods=['GET']) # index.html
def start():
    if not "token" in request.cookies: # if the user does not have a session, create one
        session = Session() # create a new session
        response = make_response('logging you in, please reload') # display a message to the user
        response.set_cookie('token', session.id) # very important, set the session ID in a cookie
        return response
    else:
        session = Session(request.cookies['token']) # get the session of the user
    
    return render_template('index.html', session=session.to_dict()) # render the index.html template with the session data

@app.route('/class', methods=['GET']) # class.html
def _class():
    id = request.args.get('id') # get the class ID from the URL
    teacher = request.cookies['token'] # get the session ID from the cookie
    __class = Class(teacher=teacher, id=id) # create a new class object with the teacher and class ID
    return render_template('class.html', session=__class.to_dict()) # render the class.html template with the class data

@app.route('/createLesson', methods=['GET']) # createLesson.html
def create_lesson(): 
    return render_template('createLesson.html') # render the createLesson.html template, all the data needed is in the url to be used by the client later on


@app.route('/getClass', methods=['GET']) # get the class data, used by the client
def get_class():
    token = request.cookies['token'] # get the session ID from the cookie
    data = request.query_string.decode('utf-8') # get the query string from the URL
    data = parse_qs(data) # parse the query string into a dictionary
    
    data = {"id": data['id'][0]} # get the class ID from the query string
    
    if not data['id']: # if the class ID is not provided, return an error
        return "Invalid class ID.", 400
    
    class_ = Class(teacher=token, id=data['id']) # create a new class object with the teacher and class ID
    return class_.to_dict(), 200 # return the class data as a JSON object to the client

@app.route('/lesson', methods=['GET']) # lesson.html
def lesson():
    token = request.cookies['token'] # get the session ID from the cookie
    class_id = request.args.get('class') # get the class ID from the URL
    lesson_id = request.args.get('id') # get the lesson ID from the URL
    fetch = request.args.get('fetch') # tell if it's to fetch lesson data or to do the lesson
    data = request.query_string.decode('utf-8') 
    data = parse_qs(data)
    
    data = {"id": data['id'][0]}
    
    if not data['id']: # if the lesson ID is not provided, return an error
        return "Invalid lesson ID.", 400
    
    class_ = Class(teacher=token, id=class_id)
    lesson = class_.get_lesson(lesson_id) # get the lesson data from the class
    if fetch: # if the client wants to fetch the lesson data, return the lesson data
        return lesson, 200
    return render_template('lesson.html', session=lesson) # render the lesson.html template with the lesson data

@app.route('/create', methods=['POST']) # create a new class or lesson
def create():
    data = request.get_json() # get the JSON data from the request
    token = request.cookies['token'] # get the session ID from the cookie

    if not data['type'] in errors.keys(): # if the type of the thing the user wants to create is not valid, return an error
        return "Invalid type.", 400
    
    for key in errors[data['type']].keys(): # check if all the required keys are provided
        if not key in data.keys():
            print(key)
            return errors[data['type']][key], 400
        
    match data['type']: # check the type of the thing the user wants to create

        case "class": # if the user wants to create a class
            new_class = Class(teacher=token, name=data['name']) # create a new class object with the teacher and class name
            return new_class.to_dict(), 200 # return the class data as a JSON object to the client
        
        case "lesson": # if the user wants to create a lesson
            _class = Class(teacher=token, id=data['class']) # create a new class object with the teacher and class ID
            return str(_class.create_lesson(name=data['name'], description=data['description'], content=data['questions'])), 200 # create a new lesson in the class and return the lesson data as a string to the client to be parsed clientside
        

if __name__ == '__main__':
    app.run(port=5500, debug=True)
