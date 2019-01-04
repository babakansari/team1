# python.exe D:/Intelex/AI/StorySize/UserStory.py
# POST
#       username:Babak
#       password:Ansari
#       number:36
# http://127.0.0.1:5000/UserStory/Prediction/Train
# http://127.0.0.1:5000/UserStory/Prediction/Predict

from flask import Flask
from flask_restful import Api
from user_story import UserStory


#################### INITIAL VARIABELS ################
app = Flask(__name__)
api = Api(app)

################# DEFINE ROUTINGS ###################
api.add_resource(UserStory, "/UserStory")
api.add_resource(UserStory.Prediction, "/UserStory/Prediction")
api.add_resource(UserStory.Prediction.Train, "/UserStory/Prediction/Train")
api.add_resource(UserStory.Prediction.Predict, "/UserStory/Prediction/Predict")

################ RUN SERVICE #################
app.run(debug = True, host= '0.0.0.0')