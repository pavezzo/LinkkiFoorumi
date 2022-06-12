from flask import Flask
from os import getenv
from utils import timeSince

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")

@app.context_processor
def utility_processor():
    return dict(timeSince=timeSince)

import routes
