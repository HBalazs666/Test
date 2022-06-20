from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship
# from main import db_session


Base = declarative_base()

association_table=Table(
    'association',
    Base.metadata,
    Column('person_id', ForeignKey('person.id')),
    Column('workplace_id', ForeignKey('workplace.id'))
    )


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(254))
    last_name = Column(String(254))
    email = Column(String(254), nullable=False)
    pets = relationship("Pet", back_populates='owner',
                            cascade='all, delete-orphan')
    workplaces = relationship('Workplace', secondary=association_table,
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
        print(type(ret))
        return ret

    def __str__(self):
        return self.email

    # def pets(self):
    #    q = db_session.query(Pet).filter_by(id=self.owner_id).all()
    #    lst = [x.dump() for x in q]
    #    return lst

class Pet(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    name = Column(String(254))
    owner_id = Column(Integer, ForeignKey("person.id"))
    owner = relationship("Person", back_populates='pets')


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
    id = Column(Integer, primary_key=True)
    city = Column(String(254))
    company = Column(String(254))
    title = Column(String(254))
    workers = relationship('Person', secondary=association_table,
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



def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
