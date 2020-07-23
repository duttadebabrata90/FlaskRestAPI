from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from flask_restful import reqparse, Resource

from SourceCode.FlaskSQLAlchemy.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True)
    parser.add_argument('store_id',
                        type=int,
                        required=True)

    @jwt_required
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json(), 202
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': 'Item with name {} already exist'.format(name)}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name, **data)
            item.save_to_db()
            return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Need admin privilege to delete'}, 401
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
            item = ItemModel(name, **data)
        item.save_to_db()
        return {'message': 'Item {} updated with price {}'.format(name, item.price)}


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'item': items}, 200
        return {'item': [item['name'] for item in items],
                'message': 'More data available if you log in'}
