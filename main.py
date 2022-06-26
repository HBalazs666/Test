from connexion import FlaskApp
from flask_sqlalchemy import SQLAlchemy


connexion_app = FlaskApp(__name__)
app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


if __name__ == '__main__':
    from orm import Base
    Base.metadata.create_all(db.engine)
    connexion_app.add_api('openapi.yaml')
    connexion_app.run(host='0.0.0.0', port=5000)
