from data import db_session
from data.users import User
from sqlalchemy.exc import IntegrityError


def add_admin():
    user = User()
    user.name = "Пользователь 1"
    user.about = "биография пользователя 1"
    user.email = "email@email.ru"
    session = db_session.create_session()
    session.add(user)
    session.commit()
    session.close()


def add_test_users():
    session = db_session.create_session()
    for i in range(2, 5):
        user = User()
        user.name = f"Пользователь {i}"
        user.about = f"биография пользователя {i}"
        user.email = f"email_{i}@email.ru"
        session.add(user)
    session.commit()


db_session.global_init("db/test.sqlite")
session = db_session.create_session()
try:
    add_admin()
except IntegrityError as e:
    print(f"WARNING: {e} {e.__class__.__name__}")
try:
    add_test_users()
except IntegrityError as e:
    print(f"WARNING: {e} {e.__class__.__name__}")

session.close()
