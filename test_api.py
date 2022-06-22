import json
import orm
import connexion
# from main import application
from orm import Person, Pet, Workplace
from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base, relationship
import pytest

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('openapi.yaml')

# def test_get_pet():
#     url = '/pets'
#     client = application.test_client()
#     resp = client.get(url)
#     print(resp.text)
#     assert resp.status_code == 200

@pytest.fixture(scope='function')
def client():
    with flask_app.app.test_client() as c:
        yield c


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


def create_person(db_session):
    db_session.add(Person(first_name="Proba", email = 'proba@email'))
    db_session.commit()
    assert len(db_session.query(Person).all()) == 1

def test_add_workplace(db_session):
    db_session.add(Person(first_name="Proba", email='proba@email'))
    db_session.add(Workplace(city="Budapest", title='Intern', company='Ericsson'))
    db_session.commit()
    person = db_session.query(Person).filter(Person.email == 'proba@email').one_or_none()
    workplace = db_session.query(Workplace).filter(Workplace.company == 'Ericsson').one_or_none()
    person.workplaces.append(workplace)
    db_session.commit()
    assert len(person.workplaces) == 1


def test_add_person(db_session):
    db_session.add(Person(first_name="Proba", email='proba@email'))
    db_session.add(Workplace(city="Budapest", title='Intern', company='Ericsson'))
    db_session.commit()
    person = db_session.query(Person).filter(Person.email == 'proba@email').one_or_none()
    workplace = db_session.query(Workplace).filter(Workplace.company == 'Ericsson').one_or_none()
    workplace.workers.append(person)
    db_session.commit()
    assert len(workplace.workers) == 1


def test_get_workplace_list(db_session):
    db_session.add(Workplace(city="Budapest", title='Intern', company='Ericsson'))
    db_session.add(Workplace(city="Rosenheim", title='Intern', company='Ericsson'))
    db_session.commit()
    workplaces = db_session.query(Workplace).all()
    assert len(workplaces) == 2


def test_workplace_delete(db_session):
    db_session.add(Workplace(city="Budapest", title='Intern', company='Ericsson'))
    db_session.add(Workplace(city="Rosenheim", title='Intern', company='Ericsson'))
    db_session.commit()
    delete_workplace = db_session.query(Workplace).filter(Workplace.city == 'Rosenheim').one_or_none()
    db_session.delete(delete_workplace)
    db_session.commit()
    workplaces = db_session.query(Workplace).all()
    assert len(workplaces) == 1

def test_create_workplace(db_session):
    db_session.add(Workplace(city="Budapest", company = 'Ericsson', title = 'Intern'))
    db_session.commit()
    assert len(db_session.query(Workplace).all()) == 1


def test_get_workplace(db_session):
    db_session.add(Workplace(city="Budapest", company = 'Ericsson', title = 'Intern'))
    db_session.commit()
    workplace = db_session.query(Workplace).filter_by(company = 'Ericsson').all()
    assert len(workplace) == 1


def test_get_people_list(db_session):
    db_session.add(Person(email='example.email1'))
    db_session.add(Person(email='example.email2'))
    db_session.commit()
    people = db_session.query(Person).all()
    assert len(people) == 2


def test_create_pet(db_session):
    db_session.add(Pet(name='proba', owner_id='probaowner'))
    db_session.commit()
    assert len(db_session.query(Pet).all()) == 1


def test_get_pet_list(db_session):
    db_session.add(Pet(name='proba1', owner_id=1))
    db_session.add(Pet(name='proba2', owner_id=2))
    db_session.commit()
    people = db_session.query(Pet).all()
    assert len(people) == 2


def test_get_pet(client, db_session):
    db_session.add(Pet(name='proba1', owner_id=2))
    db_session.commit()
    url = '/pets'
    resp = client.get(url)
    print(resp.text)
    assert resp.status_code == 200
    # pet = db_session.query(Pet).filter_by(owner_id = 2).all()
    assert resp.json[0]['name'] == 'proba1'


def test_pet_delete(db_session):
    db_session.add(Pet(name='proba1', owner_id=1))
    db_session.add(Pet(name='proba2', owner_id=2))
    db_session.commit()
    assert len(db_session.query(Pet).all()) == 2
    delete_pet = db_session.query(Pet).filter_by(owner_id = 1).one_or_none()
    db_session.delete(delete_pet)
    db_session.commit()
    pets = db_session.query(Pet).all()
    assert len(pets) == 1


def test_get_person(db_session):
    db_session.add(Person(email='example@email1.com'))
    db_session.add(Person(email='example@email2.com'))
    db_session.add(Person(email='example@email3.com'))
    db_session.commit()
    person = db_session.query(Person).filter_by(id = 1).all()
    assert len(person) == 1


def test_get_persons_pets(db_session):
    db_session.add(Person(email='example@email1.com'))
    db_session.add(Person(email='example@email2.com'))
    db_session.add(Pet(name='proba1', owner_id=1))
    db_session.add(Pet(name='proba3', owner_id=1))
    db_session.add(Pet(name='proba2', owner_id=2))
    db_session.commit()
    person = db_session.query(Person).filter_by(id = 1).all()
    assert len(person[0].pets) == 2
