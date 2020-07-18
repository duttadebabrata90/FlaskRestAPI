from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

from SourceCode.FlaskSQLAlchemy.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True)
    parser.add_argument('store_id',
                        type=int,
                        required=True)

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
            item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()
            return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item {} deleted'.format(name)}, 200
        return {'message': 'Item not found'.format(name)}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return {'message': 'Item {} updated with price {}'.format(name, item.price)}


class ItemList(Resource):
    def get(self):
        return {'item': [item.json() for item in ItemModel.query.all()]}
