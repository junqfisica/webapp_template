from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = '5780628bb0b13ce0c676dfde280ba187'
CORS(app)

# this must be imported only after flask configuration.
from flaskapp import api

