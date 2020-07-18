from flask_restful import Resource, reqparse

from SourceCode.FlaskRestFull.models.user import UserModel
from SourceCode.FlaskRestFull.db import get_connection


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type = str,
                        required = True)
    parser.add_argument('password',
                        type=str,
                        required=True)

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User Exist'}, 400

        con = get_connection()
        cursor = con.cursor()
        insert_user_sql = "INSERT INTO user VALUES (NULL,%s,%s)"
        cursor.execute(insert_user_sql, params=(data['username'], data['password']))
        con.commit()
        con.close()
        return {'message': 'User created Successfully'}, 200
