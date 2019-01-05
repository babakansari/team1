from flask_restful import Resource
from user_story_parameters import UserStoryParameters
import os.path
from user_story_train import get_story_points_data, file_name, sheetname
import pandas as pd
import json

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
                return json.dumps(df.shape, default=lambda o: o.__dict__)

        class Predict(Resource):
            def get(self):
                return "GET: Predict US#" + parameters.Number;

            def post(self):
                return "POST: Predict US#" + parameters.Number;
