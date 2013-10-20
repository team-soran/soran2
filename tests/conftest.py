# -*- coding: utf-8 -*-
from pytest import fixture

from soran.web.app import app
from soran.db import get_session, Base
from soran.db import get_engine

@fixture
def f_session(request):
    with app.app_context():
        app.config['DATABASE_URL'] = 'sqlite:///'
        engine = get_engine(app)
        Base.metadata.create_all(engine)
        session = get_session(engine)
        def finish():
            session.remove()
            session.close()
            Base.metadata.drop_all(engine)
            engine.dispose()

        request.addfinalizer(finish)
        return session
