import mysql.connector

conn = mysql.connector.connect(charset = 'utf8',
                               host="localhost",
                               user="root",
                               password="db2inst1",
                               database = 'test' )
cursor = conn.cursor()

create__user = 'CREATE TABLE IF NOT EXISTS user ' \
                '(id int NOT NULL AUTO_INCREMENT,' \
                'username VARCHAR(50) NOT NULL,' \
                'password VARCHAR(50) NULL,' \
                'PRIMARY KEY (id))'
create__items = 'CREATE TABLE IF NOT EXISTS items ' \
                '(id int NOT NULL AUTO_INCREMENT, '\
                'name VARCHAR(50) NOT NULL,' \
                'price float NOT NULL,' \
                'PRIMARY KEY (id))'

cursor.execute(create__user)
cursor.execute(create__items)

conn.commit()
conn.close()


def get_connection():
    conn = mysql.connector.connect(charset='utf8',
                                    host="localhost",
                                    user="root",
                                    password="db2inst1",
                                    database='test')
    return conn



