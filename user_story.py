from flask_restful import Resource
from user_story_parameters import UserStoryParameters

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
                return "GET: Train for username: " + parameters.UserName + ", password: " + parameters.Password

            def post(self):
                return "POST: Train for username: " + parameters.UserName + ", password: " +parameters.Password

        class Predict(Resource):
            def get(self):
                return "GET: Predict US#" + parameters.Number;

            def post(self):
                return "POST: Predict US#" + parameters.Number;
