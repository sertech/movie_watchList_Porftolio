import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

from movie_library.routes import pages

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "0A_c-ekmVQ1X1pcL_3_yXprXWiOSzlCXk8r0a7av9Ns"
    )
    app.db = MongoClient(app.config["MONGODB_URI"]).get_default_database()

    app.register_blueprint(pages)
    return app

# for heroku we have to check environment variables here we have MONGODB_URI which needs to be in heroku variables