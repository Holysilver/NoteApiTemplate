import os
from pathlib import Path

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

 # TODO ПЕРЕПИСАТЬ НА Pathlib

BASE_DIR = Path(__file__).parent
security_definitions = {
    "basicAuth": {
        "type": "basic"
    }
}

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASE_DIR, 'base.db')
    TEST_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    SQLALCHEMY_ECHO = True      # Добавление показа в терминале всего SQL кода.
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "My secret key =)"
    RESTFUL_JSON = {
        'ensure_ascii': False,
    }
    security_definitions = {
        "basicAuth": {
            "type": "basic"
        }
    }
    APISPEC_SPEC = APISpec(
        title='Notes Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        securityDefinitions=security_definitions,
        openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_URL = '/swagger'  # URI API Doc JSON
    APISPEC_SWAGGER_UI_URL = '/swagger-ui'  # URI UI of API Doc

    LANGUAGES = ['en', 'ru']
