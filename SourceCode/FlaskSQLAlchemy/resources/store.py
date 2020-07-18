from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

from SourceCode.FlaskSQLAlchemy.models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.json(), 202
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_store_by_name(name):
            return {'message': 'Store with name {} already exist'.format(name)}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {'message': 'An error occurred while inserting item'}, 500
            return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store {} deleted'.format(name)}, 200
        return {'message': 'Store not found'.format(name)}, 400


class StoreList(Resource):
    def get(self):
        return {'store': [store.json() for store in StoreModel.query.all()]}