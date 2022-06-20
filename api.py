from connexion.problem import problem
from orm import Person
from orm import Pet
from orm import Workplace
from connexion import NoContent
import json

def add_workplace(personId, workplaceId):
    from main import db_session
    person = db_session.query(Person).filter(Person.id == personId).one_or_none()
    workplace = db_session.query(Workplace).filter(Workplace.id == workplaceId).one_or_none()
    person.workplaces.append(workplace)
    db_session.commit()


def add_person(personId, workplaceId):
    from main import db_session
    person = db_session.query(Person).filter(Person.id == personId).one_or_none()
    workplace = db_session.query(Workplace).filter(Workplace.id == workplaceId).one_or_none()
    workplace.workers.append(person)
    db_session.commit()

def get_workplace_list():
    from main import db_session
    workplaces = db_session.query(Workplace).all()
    lst = [p.dump() for p in workplaces]
    return lst, 200


def workplace_delete(workplaceId):
    from main import db_session
    workplace = db_session.query(Workplace).filter(Workplace.id == workplaceId).one_or_none()
    if workplace is not None:
        db_session.delete(workplace)
        db_session.commit()
        return NoContent, 204
    else:
        return problem(404, 'Not found',
                       'Workplace does not exist.')


def create_workplace(body):
    from main import db_session
    city = body['city']
    title = body['title']
    company = body['company']
    w = Workplace(
        company=company,
        title=title,
        city=city,
    )
    db_session.add(w)
    db_session.commit()
    return w.dump(), 201


def get_workplace(workplaceId):
    from main import db_session
    workplace = db_session.query(Workplace).filter_by(id=workplaceId).one_or_none()
    if workplace is None:
        return problem(404, 'Not found',
                       'Workplace does not exist.')
    lst = workplace.dump()
    return lst, 200


def get_people_list():
    from main import db_session
    query = db_session.query(Person).all()
    lst = [p.dump() for p in query]
    print(lst)
    print(type(lst))
    return lst, 200


def create_person(body):
    from main import db_session
    first_name = body.get('first_name')
    last_name = body.get('last_name')
    email = body['email']
    p2 = db_session.query(Person).filter_by(email=email).one_or_none()
    if p2 is not None:
        return problem(409, 'Conflict',
                       'Person with this email already exists.')
    p = Person(
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    db_session.add(p)
    db_session.commit()
    return p.dump(), 201

def create_pet(body):
    from main import db_session
    name = body.get('name')
    owner = body['owner']
    p = Pet(
        name = name,
        owner_id = owner
    )
    db_session.add(p)
    db_session.commit()
    return p.dump(), 201

def get_pet_list():
    from main import db_session
    pets = db_session.query(Pet)
    # if pets is None:
    #     return problem(404, 'Not found',
    #                    'List of pets is empty.')
    return [pet.dump() for pet in pets], 200

def get_pet(petId):
    from main import db_session
    pet = db_session.query(Pet).filter_by(id=petId).one_or_none()
    if pet is None:
        return problem(404, 'Not found',
                       'Pet does not exist.')
    lst = pet.dump()
    return lst, 200

def pet_delete(petId):
    from main import db_session
    pet = db_session.query(Pet).filter(Pet.id == petId).one_or_none()
    if pet is not None:
        #logging.info('Deleting pet %s..', pet_id)
        # db_session.query(Pet).filter(Pet.id == petId).delete()
        db_session.delete(pet)
        db_session.commit()
        return NoContent, 204
    else:
        return problem(404, 'Not found',
                       'Pet does not exist.')


def get_person(personId):
    from main import db_session
    person = db_session.query(Person).filter_by(id=personId).one_or_none()
    lst = person.dump()
    return lst, 200


def get_persons_pets(personId):
    from main import db_session
    pets = db_session.query(Pet).filter_by(owner_id=personId).all()
    lst = [pet.dump() for pet in pets]
    return lst, 200
