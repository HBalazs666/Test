from orm import Person
from orm import Pet
from orm import Workplace
import json


def test_add_person(db_session, client):

    db_session.add(Person(first_name="Proba1",
                          last_name="valami",
                          email='proba@email'))

    db_session.add(Person(first_name="Proba2",
                          last_name="valami",
                          email='proba@emai2'))

    db_session.add(Workplace(city="Budapest",
                             title='Intern',
                             company='Ericsson'))
    db_session.commit()

    person = db_session.query(Person).filter(Person.id == 1).one_or_none()
    workplace = db_session.query(Workplace).filter(Workplace.id
                                                   == 1).one_or_none()
    workplace.workers.append(person)
    assert len(workplace.workers) == 1

    client.post("/workplace/add-workplace?personId=2&workplaceId=1")
    assert len(workplace.workers) == 2


def test_add_workplace(db_session, client):
    db_session.add(Person(first_name="Proba",
                          last_name="valami",
                          email='proba@email'))

    db_session.add(Workplace(city="Budapest",
                             title='Intern',
                             company='Ericsson'))

    db_session.add(Workplace(city="Rosenheim",
                             title='Intern',
                             company='Ericsson'))
    db_session.commit()

    person = db_session.query(Person).filter(Person.id == 1).one_or_none()
    workplace = db_session.query(Workplace).filter(Workplace.id
                                                   == 1).one_or_none()

    person.workplaces.append(workplace)
    assert len(person.workplaces) == 1

    client.post("/people/add-workplace?personId=1&workplaceId=2")
    assert len(person.workplaces) == 2


def test_create_person(db_session, client):
    db_session.add(Person(first_name="Proba",
                          last_name="valami",
                          email='proba@email',
                          workplaces=[]))

    db_session.commit()
    person = db_session.query(Person).filter_by(
                                            email='proba@email').one_or_none()
    person.dump()
    print(person.dump())
    assert len(db_session.query(Person).all()) == 1

    data = {
                "email": "created@email.com"
            }
    url = '/people'
    resp = client.post(url, json=data)
    assert resp.status_code == 201
    data2 = json.loads(resp.data)
    assert data2['email'] == "created@email.com"

    resp = client.post(url, json=data)
    assert resp.status_code == 409


def test_get_workplace_list(db_session, client):

    db_session.add(Workplace(city="Budapest",
                             title='Intern',
                             company='Ericsson'))

    db_session.add(Workplace(city="Rosenheim",
                             title='Intern',
                             company='Ericsson'))
    db_session.commit()
    workplaces = db_session.query(Workplace).all()
    assert len(workplaces) == 2

    resp = client.get('/workplace')
    assert resp.status_code == 200


def test_workplace_delete(db_session, client):

    db_session.add(Workplace(city="Budapest",
                             title='Intern',
                             company='Ericsson'))

    db_session.add(Workplace(city="Rosenheim",
                             title='Intern',
                             company='Ericsson'))
    db_session.commit()

    delete_workplace = db_session.query(Workplace).filter(
        Workplace.city == 'Rosenheim').one_or_none()

    db_session.delete(delete_workplace)
    db_session.commit()

    workplaces = db_session.query(Workplace).all()
    assert len(workplaces) == 1

    url = '/workplace/1'
    resp = client.delete(url)
    assert resp.status_code == 204

    resp = client.delete(url)
    assert resp.status_code == 404


def test_create_workplace(db_session, client):
    db_session.add(Workplace(city="Budapest",
                             company='Ericsson',
                             title='Intern'))
    db_session.commit()

    assert len(db_session.query(Workplace).all()) == 1

    data = {
                "city": "Budapest",
                "company": "Ericsson",
                "title": "Intern"
            }
    url = '/workplace'
    resp = client.post(url, json=data)
    assert resp.status_code == 201


def test_get_workplace(db_session, client):
    db_session.add(Workplace(city="Budapest",
                             company='Ericsson',
                             title='Intern'))
    db_session.commit()

    workplace = db_session.query(Workplace).filter_by(
        company='Ericsson').all()
    assert len(workplace) == 1

    resp = client.get('/workplace/1')
    assert resp.status_code == 200
    # print(resp.text)
    lst = resp.json
    assert lst['city'] == 'Budapest'

    resp = client.get('/workplace/100')
    assert resp.status_code == 404


def test_get_people_list(db_session, client):
    db_session.add(Person(email='example.email1'))
    db_session.add(Person(email='example.email2'))
    db_session.commit()
    people = db_session.query(Person).all()
    assert len(people) == 2

    resp = client.get('/people')
    assert resp.status_code == 200


def test_create_pet(db_session, client):
    p = Person(email='proba')
    db_session.add(p)
    db_session.add(Pet(name='proba', owner=p))
    db_session.commit()
    assert len(db_session.query(Pet).all()) == 1

    data = {
                "name": "probacreate",
                "owner_id": p.id
            }
    url = '/pets'
    resp = client.post(url, json=data)
    assert resp.status_code == 201


def test_get_pet_list(db_session, client):
    db_session.add(Pet(name='proba1', owner_id=1))
    db_session.add(Pet(name='proba2', owner_id=2))
    db_session.commit()
    people = db_session.query(Pet).all()

    assert len(people) == 2
    url = '/pets'
    resp = client.get(url)
    assert resp.status_code == 200
    lst = resp.json
    assert len(lst) == 2
    assert lst[0]['name'] == 'proba1'


def test_get_pet(client, db_session):
    db_session.add(Pet(name='proba1'))
    db_session.commit()

    url = '/pets/1'
    resp = client.get(url)
    assert resp.status_code == 200
    lst = resp.json
    assert lst['name'] == 'proba1'

    resp = client.get("/pets/100")
    assert resp.status_code == 404


def test_pet_delete(db_session, client):
    db_session.add(Pet(name='proba1', owner_id=1))
    db_session.add(Pet(name='proba2', owner_id=2))
    db_session.commit()
    assert len(db_session.query(Pet).all()) == 2
    delete_pet = db_session.query(Pet).filter_by(owner_id=1).one_or_none()
    db_session.delete(delete_pet)
    db_session.commit()
    pets = db_session.query(Pet).all()
    assert len(pets) == 1

    url = '/pets/2'
    resp = client.delete(url)
    assert resp.status_code == 204

    resp = client.delete("/pets/100")
    assert resp.status_code == 404


def test_get_person(db_session, client):
    db_session.add(Person(email='example@email1.com'))
    db_session.add(Person(email='example@email2.com'))
    db_session.add(Person(email='example@email3.com'))
    db_session.commit()
    person = db_session.query(Person).filter_by(id=1).all()
    assert len(person) == 1

    url = '/people/1'
    resp = client.get(url)
    assert resp.status_code == 200
    lst = resp.json
    assert lst['email'] == 'example@email1.com'


def test_get_persons_pets(db_session, client):
    db_session.add(Person(email='example@email1.com'))
    db_session.add(Person(email='example@email2.com'))
    db_session.add(Pet(name='proba1', owner_id=1))
    db_session.add(Pet(name='proba3', owner_id=1))
    db_session.add(Pet(name='proba2', owner_id=2))
    db_session.commit()
    person = db_session.query(Person).filter_by(id=1).all()
    assert len(person[0].pets) == 2

    url = '/people/1/pets'
    resp = client.get(url)
    assert resp.status_code == 200
    lst = resp.json
    assert len(lst) == 2


def test_person_dump(db_session):

    db_session.add(Workplace(city="Budapest",
                             title='Intern',
                             company='Ericsson'))

    db_session.add(Person(first_name="Proba1",
                          last_name="valami1",
                          email='proba@email1',
                          workplaces=[]))

    db_session.add(Person(first_name="Proba2",
                          last_name="valami2",
                          email='proba@email2',
                          workplaces=[]))

    person = db_session.query(Person).filter_by(id=2).one_or_none()
    workplace = db_session.query(Workplace).filter_by(id=1).one_or_none()
    person.workplaces.append(workplace)

    res = person.dump()
    assert len(res['workplaces']) == 1

    person = db_session.query(Person).filter_by(id=1).one_or_none()
    res = person.dump()
    assert res["workplaces"] == []


def test_person_str():

    p = Person(email='xyz@example.com')
    assert str(p) == 'xyz@example.com'
