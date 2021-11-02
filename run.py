# load libaries
from flask import Flask
from blueprint_model import blueprint_model


# init Flask app
app = Flask(__name__)
app.register_blueprint(blueprint_model, url_prefix="/api/mymodel")
