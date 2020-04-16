import os  # for reading heroku DATABASE_URL

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
# from flask_jwt import JWT
# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.secret_key = "rudimar"  # if publishing, do not want this key to be visible
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # the sqlAlchemy modification tracker does the job
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ugykgauycmywxv:701bf83f2c3578d738436980432836bcfed076dbedbe70f29aacef014dbfab16@ec2-18-233-137-77.compute-1.amazonaws.com:5432/derqg7tdiv2err'
# second is the default value
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTION'] = True

db.init_app(app)


@app.before_first_request
def create_tables():
    # Create all the tables unless they exist
    db.create_all()


# creates the endpoint /auth
# gets the username and password and sends to the authenticate function
# calls the 'identity' when receives the jwt token to get the user
# jwt = JWT(app, authenticate, identity)

jwt = JWTManager(app)  # not creating the /auth


@jwt.user_claims_loader  # runs whenever we create an acess token
def add_claims_to_jwt(identity):  # identity is what we pass when creating the token, in this case user.id
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == "__main__":
    print("oi")
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=True)
