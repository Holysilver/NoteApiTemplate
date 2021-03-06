from flask_babel import Babel
from config import Config
from flask import Flask, g
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from flask_apispec.extension import FlaskApiSpec
from flask_restful import reqparse, request

# # Общие настройки логгера
# logging.basicConfig(filename='record.log',
#                     level=logging.INFO,
#                     format=f'%(asctime)s %(levelname)s %(name)s : %(message)s')

app = Flask(__name__)
app.config.from_object(Config)
# app.config.update()

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
auth = HTTPBasicAuth()
# swagger = Swagger(app)
docs = FlaskApiSpec(app)
babel = Babel(app)

with app.app_context():
    from commands import *


@auth.verify_password
def verify_password(username_or_token, password):
    from api.models.user import UserModel
    # сначала проверяем authentication token
    # print("username_or_token = ", username_or_token)
    # print("password = ", password)
    user = UserModel.verify_auth_token(username_or_token)
    if not user:
        # потом авторизация
        user = UserModel.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@auth.get_user_roles
def get_user_roles(user):
    return g.user.get_roles()


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
