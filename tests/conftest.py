import pytest
from connexion import FlaskApp
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope='session')
def app():
    connexion_app = FlaskApp(__name__)
    connexion_app.add_api('../openapi.yaml')
    app = connexion_app.app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db_test.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app


@pytest.fixture(scope='session')
def _db(app):
    from orm import Base
    db = SQLAlchemy(app=app)
    Base.metadata.create_all(db.engine)
    yield db
    Base.metadata.drop_all(db.engine)


@pytest.fixture()
def client(app):
    with app.test_client() as c:
        yield c
