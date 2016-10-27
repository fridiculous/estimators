from estimators import DataBase


def create_db():
    db = DataBase(url='sqlite://')
    db.initialize_database()
    return db

db = create_db()
