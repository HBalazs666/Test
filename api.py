from connexion.problem import problem
from main import db
from orm import Person
from orm import Pet
from orm import Workplace
from connexion import NoContent


def add_workplace(personId, workplaceId):
    person = db.session.query(Person).filter(Person.id == personId).one_or_none()
    workplace = db.session.query(Workplace).filter(Workplace.id == workplaceId).one_or_none()
    person.workplaces.append(workplace)
    db.session.commit()


def add_person(personId, workplaceId):
    person = db.session.query(Person).filter(Person.id == personId).one_or_none()
    workplace = db.session.query(Workplace).filter(Workplace.id == workplaceId).one_or_none()
    workplace.workers.append(person)
    db.session.commit()


def get_workplace_list():
    workplaces = db.session.query(Workplace).all()
    lst = [p.dump() for p in workplaces]
    return lst, 200


def workplace_delete(workplaceId):
    workplace = db.session.query(Workplace).filter(Workplace.id == workplaceId).one_or_none()
    if workplace is not None:
        db.session.delete(workplace)
        db.session.commit()
        return NoContent, 204
    else:
        return problem(404, 'Not found',
                       'Workplace does not exist.')


def create_workplace(body):
    city = body['city']
    title = body['title']
    company = body['company']
    w = Workplace(
        company=company,
        title=title,
        city=city,
    )
    db.session.add(w)
    db.session.commit()
    return w.dump(), 201


def get_workplace(workplaceId):
    workplace = db.session.query(Workplace).filter_by(id=workplaceId).one_or_none()
    if workplace is None:
        return problem(404, 'Not found',
                       'Workplace does not exist.')
    lst = workplace.dump()
    return lst, 200


def get_people_list():
    query = db.session.query(Person).all()
    lst = [p.dump() for p in query]
    return lst, 200


def create_person(body):
    first_name = body.get('first_name')
    last_name = body.get('last_name')
    email = body['email']
    p2 = db.session.query(Person).filter_by(email=email).one_or_none()
    if p2 is not None:
        return problem(409, 'Conflict',
                       'Person with this email already exists.')
    p = Person(
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    db.session.add(p)
    db.session.commit()
    return p.dump(), 201


def create_pet(body):
    name = body.get('name')
    owner = body['owner']
    p = Pet(
        name = name,
        owner_id = owner
    )
    db.session.add(p)
    db.session.commit()
    return p.dump(), 201

def get_pet_list():
    pets = db.session.query(Pet)
    # if pets is None:
    #     return problem(404, 'Not found',
    #                    'List of pets is empty.')
    return [pet.dump() for pet in pets], 200

def get_pet(petId):
    pet = db.session.query(Pet).filter_by(id=petId).one_or_none()
    if pet is None:
        return problem(404, 'Not found',
                       'Pet does not exist.')
    lst = pet.dump()
    return lst, 200

def pet_delete(petId):
    pet = db.session.query(Pet).filter(Pet.id == petId).one_or_none()
    if pet is not None:
        #logging.info('Deleting pet %s..', pet_id)
        # db.session.query(Pet).filter(Pet.id == petId).delete()
        db.session.delete(pet)
        db.session.commit()
        return NoContent, 204
    else:
        return problem(404, 'Not found',
                       'Pet does not exist.')


def get_person(personId):
    person = db.session.query(Person).filter_by(id=personId).one_or_none()
    lst = person.dump()
    return lst, 200


def get_persons_pets(personId):
    pets = db.session.query(Pet).filter_by(owner_id=personId).all()
    lst = [pet.dump() for pet in pets]
    return lst, 200
