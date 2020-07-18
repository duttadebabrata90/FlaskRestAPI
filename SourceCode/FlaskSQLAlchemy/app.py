from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from SourceCode.FlaskSQLAlchemy.security import user_validation, identity
from SourceCode.FlaskSQLAlchemy.resources.user import UserRegister
from SourceCode.FlaskSQLAlchemy.resources.item import Item, ItemList
from SourceCode.FlaskSQLAlchemy.resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='db2inst1', server='localhost', database='test')
app.config['SQLALCHEMY_TRACK_MODIFICATIOS'] = False
api = Api(app)

jwt = JWT(app, user_validation, identity)  # will create new endpoint for authenticate /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    from SourceCode.FlaskSQLAlchemy.database import db
    db.init_app(app)
    app.run(port=5000, debug=True)
