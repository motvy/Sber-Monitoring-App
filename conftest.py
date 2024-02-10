import pytest

import config
from app import create_app
from app import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app(config=config.TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def test_client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app, request):
    def teardown():
        _db.drop_all()

    _db.app = app

    _db.create_all()
    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="function")
def session(db, request):
    db.session.begin_nested()

    def commit():
        db.session.flush()

    old_commit = db.session.commit
    db.session.commit = commit

    def teardown():
        db.session.rollback()
        db.session.close()
        db.session.commit = old_commit

    request.addfinalizer(teardown)
    return db.session
