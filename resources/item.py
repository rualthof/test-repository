from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
# from flask_jwt import jwt_required
from models.item import ItemModel


# the api works with resources and every resource has to be a class
class Item(Resource):
    # Pertains to the class, call as Item.parser..
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    # @jwt_required()
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found '}, 404

    def post(self, name):
        # checking for unique name
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name {name} already exists."}, 400  # Bad request

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)  # data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"}, 500  # Internal server error

        return item.json(), 201  # 201 - created

    @jwt_required
    def delete(self, name):

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):

        # data = request.get_json()
        # print(data)
        data = Item.parser.parse_args()  # drops any arguments that weren't added

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)  # data['price'], data['store_id']
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()  # if none, user not logged in or didnt send the auth token
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            return {'items': items}
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in'
        }
