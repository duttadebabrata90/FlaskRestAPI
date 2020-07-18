from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from SourceCode.FlaskSQLAlchemy.security import user_validation, identity
from SourceCode.FlaskSQLAlchemy.resources.user import UserRegister
from SourceCode.FlaskSQLAlchemy.resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'test'
api = Api(app)

jwt = JWT(app, user_validation, identity)  # will create new endpoint for authenticate /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
