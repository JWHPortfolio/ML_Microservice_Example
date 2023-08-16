from flask import Flask
from flask import request
import os
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score

app = Flask(__name__)

#http://localhost:8786/infer?age=28&salary=40000

global ml_learn
ml_learn = False

@app.route('/stats', methods=['GET'])
def getStats():
    global ml_learn
    if(ml_learn == False):
        #must learn first
        ml_learn = model_learn()
    return model_stats()

@app.route('/infer', methods=['GET'])
def getInfer():
    global ml_learn
    if(ml_learn == False):
        #must learn first
        ml_learn = model_learn()
    args = request.args
    age = int(args.get('age'))
    salary = int(args.get('salary'))
    return model_infer(age,salary)

@app.route('/post', methods=['POST'])
def hellopost():
    args = request.args
    name = args.get('name')
    location = args.get('location')
    image = args.get('image')
    print("Name: ", name, " Location: ", location)
    print("Image: ", image)
    return 'Hello, Post!'

def model_learn():
    print('Model Learning')
    # Importing the dataset
    dataset = pd.read_csv('Social_Network_Ads.csv')
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
    
    
    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
    
    global sc
    
    # Feature Scaling
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    
    global classifier
    
    # Training the Random Forest Classification model on the Training set
    from sklearn.ensemble import RandomForestClassifier
    classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
    classifier.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = classifier.predict(X_test)

    global stats 
    stats = str(accuracy_score(y_test, y_pred))

    return True

def model_infer(age,salary):
    if( classifier.predict(sc.transform([[age,salary]]))[0] == 1):
        determination = 'Yes, A good Candidate'
    else:
        determination = 'No, a Bad Candidate'
    return determination

def model_stats():
    return stats


if __name__ == "__main__":
    flaskPort = 8786
    print('starting server...')
    app.run(host = '0.0.0.0', port = flaskPort)
    