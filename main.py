import connexion
from orm import init_db
from orm import Person
from orm import Pet


SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'


# def create_person():
#     session = init_db(SQLALCHEMY_DATABASE_URI)
#     p = Person(first_name='Jakab', last_name='Gipsz',
#                email='gipsz.jakab@example.com')
#     session.add(p)
#     session.commit()

# def create_pet():
#     session = init_db(SQLALCHEMY_DATABASE_URI)
#     p = Pet(name='Marcang')
#     session.add(p)
#     session.commit()


db_session = init_db(SQLALCHEMY_DATABASE_URI)
app = connexion.FlaskApp(__name__)
app.add_api('openapi.yaml')

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run(host ='0.0.0.0', port=5000)
