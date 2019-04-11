
def database_config():
    # Database configuration.
    db_url = "localhost:5432"
    db_name = "app"
    db_user = "app"
    db_password = "app"
    sqlalchemy_database_url = "postgresql://{db_user}:{db_password}@{db_url}/{db_name}". \
        format(db_user=db_user, db_password=db_password, db_url=db_url, db_name=db_name)

    return sqlalchemy_database_url


class Config:
    SQLALCHEMY_DATABASE_URI = database_config()
    SECRET_KEY = '5780628bb0b13ce0c676dfde280ba187'


