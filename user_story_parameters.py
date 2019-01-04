from flask_restful import reqparse

class UserStoryParameters():
    _USERNAME = 'username'
    _PASSWORD = 'password'
    _NUMBER = 'number'

    def __init__(self):
        self._parser = reqparse.RequestParser()
        self._parser.add_argument(UserStoryParameters._USERNAME)
        self._parser.add_argument(UserStoryParameters._PASSWORD)
        self._parser.add_argument(UserStoryParameters._NUMBER)

    @property
    def UserName(self):
        arguments = self._parser.parse_args()
        return arguments[UserStoryParameters._USERNAME]

    @property
    def Password(self):
        arguments = self._parser.parse_args()
        return arguments[UserStoryParameters._PASSWORD]

    @property
    def Number(self):
        arguments = self._parser.parse_args()
        return arguments[UserStoryParameters._NUMBER]