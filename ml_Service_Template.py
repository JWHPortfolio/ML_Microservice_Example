from flask import Flask
from flask import request
import os

from randomforest import randomforest

app = Flask(__name__)

#http://localhost:8786/infer?age=28&salary=40000

global rf
global ml_learn
ml_learn = False

@app.route('/stats', methods=['GET'])
def getStats():
    global ml_learn
    if(ml_learn == False):
        #must learn first
        ml_learn = rf.model_learn()
    return rf.model_stats()

@app.route('/infer', methods=['GET'])
def getInfer():
    global ml_learn
    if(ml_learn == False):
        #must learn first
        ml_learn = rf.model_learn()
    args = request.args
    age = int(args.get('age'))
    salary = int(args.get('salary'))
    return rf.model_infer(age,salary)

@app.route('/post', methods=['POST'])
def hellopost():
    args = request.args
    name = args.get('name')
    location = args.get('location')
    image = args.get('image')
    print("Name: ", name, " Location: ", location)
    print("Image: ", image)
    return 'Hello, Post!'



if __name__ == "__main__":
    flaskPort = 8786
    rf = randomforest()
    print('starting server...')
    app.run(host = '0.0.0.0', port = flaskPort)
    