import logging, coloredlogs

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
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

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'

login_manager.init_app(app)


def create_logger():
    # create logger.
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    coloredlogs.install(level='DEBUG', logger=logger)

    # create console handler and set level to debug.
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create file handler.
    file_log = logging.FileHandler(filename="app.log")
    file_log.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    file_log.setFormatter(formatter)

    # add ch and file_log to logger
    logger.addHandler(ch)
    logger.addHandler(file_log)

    return logger


app_logger = create_logger()
app_logger.info("Webservice started.")

# this must be imported only after flask configuration.
from flaskapp.api import api as api_blueprint
from flaskapp.api import users as users_blueprint

# register new APIs here.
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(users_blueprint, url_prefix='/api/user')

