from SourceCode.FlaskRestFull.db import get_connection


class ItemModel:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_item_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        get_item_sql = "SELECT * FROM items where name = %s"
        cursor.execute(get_item_sql, params=(name,))
        data = cursor.fetchone()
        conn.close()
        if data:
            return cls(*data)

    def insert_item(self):
        conn = get_connection()
        cursor = conn.cursor()
        insert_item_sql = "INSERT INTO items VALUES (%s,%s)"
        cursor.execute(insert_item_sql, params=(self.name, self.price))
        conn.commit()
        conn.close()

    def update_item(self):
        conn = get_connection()
        cursor = conn.cursor()
        update_item_sql = "UPDATE items SET price = %s WHERE name = %s"
        cursor.execute(update_item_sql, params=(self.price, self.name))
        conn.commit()
        conn.close()