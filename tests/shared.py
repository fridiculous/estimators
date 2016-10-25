from estimators import DataBase
import factory.alchemy


def create_session():
    db = DataBase(url='sqlite://')
    db.initialize_database()
    return db.Session

db_session = create_session()


class SessionFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db_session
