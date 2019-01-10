from flask_restful import Resource
from user_story_parameters import UserStoryParameters
import os.path
from user_story_train import get_story_points_data, file_name, sheetname, save_trained_models, load_trained_model
from user_story_predict import predict_points, define_input
import pandas as pd
import json
from jira import JIRAError

parameters = UserStoryParameters();

class UserStory(Resource):

    def get(self):
        return "GET: User Story Operation!"

    def post(self):
        return "POST: User Story Operation!"

    class Prediction(Resource):

        def get(self):
            return "GET: User Story Prediction!"

        def post(self):
            return "POST: User Story Prediction!"

        class Train(Resource):
            def get(self):
                result = self.train_model(parameters.UserName, parameters.Password)
                return result

            def post(self):
                result = self.train_model(parameters.UserName, parameters.Password)
                return result

            def train_model(self, username, password):
                jiraFileExist = os.path.exists(file_name)

                if not jiraFileExist:
                    df = get_story_points_data(username, password)
                else:
                    print("Data loaded from file:", file_name)
                    df = pd.read_excel(file_name, sheetname)
                data_shape = json.dumps(df.shape, default=lambda o: o.__dict__)

                save_trained_models(df)
                return data_shape

        class Predict(Resource):
            def get(self):
                result = self.predict_points(parameters.UserName, parameters.Password, parameters.Number)
                return result;

            def post(self):
                result = self.predict_points(parameters.UserName, parameters.Password, parameters.Number)
                return result;

            def predict_points(self, username, password, number):
                print('------------< Predict >------------------')

                load_trained_model(self)

                status = "";
                logistic = "";
                svc = "";
                linearSVC = "";
                adaBoost = "";
                try:
                    prediction_df = define_input(self.model, username, password, number)
                    print("\r\n\r\nFeatures: " + str(prediction_df.columns) + "\r\n\r\n")
                    print("\r\n\r\nTotal Features: " + str(len(prediction_df.columns)) + "\r\n\r\n")

                    logistic = predict_points(self.logistic_classifier, prediction_df)
                    svc = predict_points(self.svc_classifier, prediction_df)
                    linearSVC = predict_points(self.linearSVC_classifier, prediction_df)
                    adaBoost = predict_points(self.adaBoost_classifier, prediction_df)
                except JIRAError as e:
                    status = "Jira error: " + str(e)

                #classifiers = {"status":status, "logistic":logistic, "svc": svc, "linearSVC": linearSVC, "adaBoost": adaBoost};
                #result = json.dumps(classifiers, default=lambda o: o.__dict__)
                classifiers = {}
                classifiers['status'] = status
                classifiers['logistic'] = logistic
                classifiers['svc'] = svc
                classifiers['linearSVC'] = linearSVC
                classifiers['adaBoost'] = adaBoost
                result = json.dumps(classifiers)
                return result;
