import os # for reading heroku DATABASE_URL

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.secret_key = "rudimar"  # if publishing, do not want this key to be visible
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # the sqlAlchemy modification tracker does the job
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  # second is the default value

db.init_app(app)

@app.before_first_request
def create_tables():
    #Create all the tables unless they exist
    db.create_all()

# creates the endpoint /auth
# gets the username and password and sends to the authenticate function
# calls the 'identity' when receives the jwt token to get the user
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == "__main__":
    print("oi")
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=True)
