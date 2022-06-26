from main import db


class Base(db.Model):
    __abstract__ = True


association_table = db.Table(
    'association',
    Base.metadata,
    db.Column('person_id', db.ForeignKey('person.id')),
    db.Column('workplace_id', db.ForeignKey('workplace.id'))
    )


class Person(Base):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(254))
    last_name = db.Column(db.String(254))
    email = db.Column(db.String(254), nullable=False)
    pets = db.relationship("Pet", back_populates='owner',
                            cascade='all, delete-orphan')
    workplaces = db.relationship('Workplace', secondary=association_table,
                                back_populates='workers')


    def dump(self):
        ret = {
            'id': self.id,
            'email': self.email,
        }

        if self.first_name is not None:
            ret['first_name'] = self.first_name
        if self.last_name is not None:
            ret['last_name'] = self.last_name

        if self.workplaces is not None:
            ret['workplaces'] = [workspace.dump() for workspace in self.workplaces]
        else:
            ret['workplaces'] = []
        return ret

    def __str__(self):
        return self.email

    # def pets(self):
    #    q = db_session.query(Pet).filter_by(id=self.owner_id).all()
    #    lst = [x.dump() for x in q]
    #    return lst

class Pet(Base):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254))
    owner_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    owner = db.relationship("Person", back_populates='pets')


    def dump(self):
        ret = {
            'id': self.id,
            'name': self.name,
        }
        if self.name is not None:
            ret['name'] = self.name
        return ret

    # def owner():
    #    q = db_session.query(Person).filter_by(owner_id=id).one_or_none()
    #    return q.dump()

class Workplace(Base):
    __tablename__ = 'workplace'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(254))
    company = db.Column(db.String(254))
    title = db.Column(db.String(254))
    workers = db.relationship('Person', secondary=association_table,
                                back_populates='workplaces')

    def dump(self):
        ret = {
            'id': self.id,
            'city': self.city,
            'company': self.company,
            'title': self.title
        }
        # if self.workers is not None:
        #     ret['workers'] = self.workers
        return ret
