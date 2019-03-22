from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Database configuration.
db_url = "localhost:5432"
db_name = "app"
db_user = "app"
db_password = "app"
sqlalchemy_database_url = "postgresql://{db_user}:{db_password}@{db_url}/{db_name}".\
    format(db_user=db_user, db_password=db_password, db_url=db_url, db_name=db_name)


# App configuration.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_database_url
app.config['SECRET_KEY'] = '5780628bb0b13ce0c676dfde280ba187'

# start db.
db = SQLAlchemy(app)

# set CORS-filter
CORS(app)

# this must be imported only after flask configuration.
from flaskapp import api

