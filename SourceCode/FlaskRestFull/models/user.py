from SourceCode.FlaskRestFull.db import get_connection


class UserModel:

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conn = get_connection()
        cursor = conn.cursor()
        get_user_sql = "select * from test.user where  username=%s"
        cursor.execute(get_user_sql, params=(username,))
        data = cursor.fetchone()
        if data:
            user = cls(*data)
        else:
            user = None
        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conn = get_connection()
        cursor = conn.cursor()
        get_user_sql = 'select * from user where  id = %s;'
        cursor.execute(get_user_sql, params=(_id,))
        data = cursor.fetchone()
        if data:
            user = cls(*data)
        else:
            user = None
        conn.close()
        return user
