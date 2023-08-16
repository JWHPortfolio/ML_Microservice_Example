import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score


class randomforest:
    def model_learn(self):
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

    def model_infer(self, age,salary):
        if( classifier.predict(sc.transform([[age,salary]]))[0] == 1):
            determination = 'Yes, A good Candidate'
        else:
            determination = 'No, a Bad Candidate'
        return determination

    def model_stats(self):
        return stats
