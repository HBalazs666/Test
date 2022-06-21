import json
import orm
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base, relationship
import pytest


# def test_get_pet():
#     url = '/pets'
#     client = application.test_client()
#     resp = client.get(url)
#     print(resp.text)
#     assert resp.status_code == 200



@pytest.fixture(scope="session")
def connection():
    engine = create_engine('sqlite:///test.db')
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    orm.Base.metadata.bind = connection
    orm.Base.metadata.create_all()

    yield

    orm.Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()


def test_user_created(db_session):
    db_session.add(orm.Person(first_name="Proba", email = 'proba@email'))
    db_session.commit()
    assert len(db_session.query(orm.Person).all()) == 1
