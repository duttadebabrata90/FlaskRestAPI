from flask import Flask, jsonify
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from flask_restful import Api

from SourceCode.FlaskSQLAlchemy.blacklist import BLACKLIST
from SourceCode.FlaskSQLAlchemy.resources.item import Item, ItemList
from SourceCode.FlaskSQLAlchemy.resources.store import Store, StoreList
# from SourceCode.FlaskSQLAlchemy.security import user_validation, identity
from SourceCode.FlaskSQLAlchemy.resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout

app = Flask(__name__)
app.secret_key = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='db2inst1', server='localhost', database='test')
app.config['SQLALCHEMY_TRACK_MODIFICATIOS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)

# jwt = JWT(app, user_validation, identity)  # will create new endpoint for authenticate /auth
jwt = JWTManager(app)


@jwt.user_claims_loader              # jwt -----> name of the JWTManager object
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    else:
        return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {'description': 'The token has been expired .....',
         'error': 'token_expired'}
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(
        {'description': 'Signature verification failed .....',
         'error': 'token_expired'}
    ), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(
        {'description': 'Request done not contain a access token .....',
         'error': 'authorization_required'}
    ), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify(
        {'description': 'The token is not fresh .....',
         'error': 'fresh_token_required'}
    ), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')  # we cn use any uri
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from SourceCode.FlaskSQLAlchemy.database import db
    db.init_app(app)
    app.run(port=5000, debug=True)
