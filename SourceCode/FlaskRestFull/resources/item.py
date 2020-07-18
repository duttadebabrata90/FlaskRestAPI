from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

from SourceCode.FlaskRestFull.db import get_connection
from SourceCode.FlaskRestFull.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True)\


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json(), 202
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': 'Item with name {} already exist'.format(name)}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name, data['price'])
            try:
                item.insert_item()
            except:
                return {'message': 'An error occurred while inserting item'}, 500
            return item.json(), 201

    def delete(self, name):
        if ItemModel.find_item_by_name(name):
            conn = get_connection()
            cursor = conn.cursor()
            delete_item_sql = "DELETE FROM items WHERE name = %s"
            cursor.execute(delete_item_sql, params=(name,))
            conn.commit()
            conn.close()
            return {'message': 'Item {} deleted'.format(name)}, 200
        return {'message': 'Item not found'.format(name)}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        updated_item = ItemModel(name, data['price'])
        item = ItemModel.find_item_by_name(name)
        if item:
            try:
                updated_item.update_item()
            except:
                return {'message': 'An error occurred while inserting item'}, 500
        else:
            try:
                updated_item.insert_item()
            except:
                return {'message': 'An error occurred while updating item'}, 500
        return {'message': 'Item {} updated with price {}'.format(name, updated_item.price)}


class ItemList(Resource):
    def get(self):
        return {'item': self.get_items()}

    @classmethod
    def get_items(cls):
        conn = get_connection()
        cursor = conn.cursor()
        get_item_sql = "SELECT * FROM items"
        cursor.execute(get_item_sql)
        data = cursor.fetchall()
        conn.close()
        items = []
        if data:
            for item in data:
                items.append({'name': item[0], 'price': item[1]})
        return items
