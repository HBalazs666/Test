from orm import Person
from orm import Pet
from orm import Workplace


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
    db_session.add(Pet(name='proba1'))
    db_session.commit()
    url = '/pets'
    resp = client.get(url)
    assert resp.status_code == 200
    lst = resp.json
    assert len(lst) == 1
    assert lst[0]['name'] == 'proba1'


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
