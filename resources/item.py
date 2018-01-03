# from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,  # noqa
        required=True,  # noqa
        help="Cannot be left blank"  # noqa
    )  # noqa
    parser = reqparse.RequestParser()
    parser.add_argument('store_id',
        type=int,  # noqa
        required=True,  # noqa
        help="Every item needs a store id"  # noqa
    )  # noqa

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            # status code 400 bad request
            return {'message': "Item with name '{}' exists".format(name)}, 400
        # data = request.get_json(silent=True)  # Silent in case of wrong format  # noqa
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:  # noqa
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201  # created status code 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
