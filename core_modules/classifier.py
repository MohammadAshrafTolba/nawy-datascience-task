import pickle
import pathlib
import os
from core_modules.data_processor import DataProcessor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split
import pandas as pd


base_path = os.path.dirname(__file__)

class Classifier:

    def __init__(self) -> None:
        self.model_path = os.path.join(base_path, 'classifier.pkl')

    def save_model(self, classifier):
        """
        pickle classifier
        """
        with open(self.model_path, 'wb') as f:
            pickle.dump(classifier, f)

    def load_model(self):
        """
        load pickled classifier
        """
        classifier = None
        with open(self.model_path, 'rb') as f:
            classifier = pickle.load(f)        
        return classifier

    def save_test_results(self, score_message, y_pred, y_test):
        pd.DataFrame({
            'predicted': y_pred,
            'actual': y_test
        }).to_csv('test_output.csv', header=True, index=False)

        with open(os.path.join(base_path, 'classifier_final_score.txt'), 'w') as f:
            f.write(score_message)

    def test_classifier(self, classifier, X_test, y_test):
        y_pred = classifier.predict(X_test)
        score = recall_score(y_test, y_pred)
        score_message = f'Recall score: {score}'
        print(score_message)
        self.save_test_results(score_message, y_pred, y_test)

    def train_classifer(self, df):

        data_processor = DataProcessor(df=df)
        df = data_processor.prepare_data()

        y = df['low_qualified']
        # print(y)
        x_cols = list(df.columns)
        
        x_cols.remove('low_qualified')
        X = df[x_cols]

        # print('x cols')
        # print(x_cols)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        classifier = RandomForestClassifier(max_depth=None, random_state=0)
        classifier.fit(X_train, y_train)
        self.test_classifier(classifier, X_test, y_test)
        self.save_model(classifier)
        print('Saved classifier')

        return x_cols, classifier

    def classify_instance(self, instance_info_dict):

        df = pd.DataFrame(instance_info_dict, index=[0])
        data_processor = DataProcessor(df=df)
        df = data_processor.prepare_data()
        # y = df['low_qualified']
        x_cols = list(df.columns)
        if 'low_qualified' in x_cols:
            x_cols.remove('low_qualified')
            df.drop(columns=['low_qualified'], inplace=True)
        
        clf = self.load_model()
        prediction = clf.predict(df)
        return instance_info_dict, prediction

