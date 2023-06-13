from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from application.keys import SECRET_KEY
# from application.workers import celery
from application.celery_file import make_celery
from flask_caching import Cache

# Flask App
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config["CELERY_BACKEND"] = "redis://localhost:6379/2"

celery = make_celery(app)
db = SQLAlchemy(app)
cache = Cache(config={"CACHE_TYPE": "RedisCache",
                      "CACHE_REDIS_HOST": "127.0.0.1",
                      "CACHE_REDIS_PORT": 6379})
cache.init_app(app)
app.app_context().push()

from application.controller import *
from application.api import *
from application.tasks import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)


