import pytest

from rating_app.app import create_app
from rating_app.extensions import db as _db
from rating_app.models import User


@pytest.fixture
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username='admin',
        email='admin@admin.com',
    )

    db.session.add(user)
    db.session.commit()

    return user
