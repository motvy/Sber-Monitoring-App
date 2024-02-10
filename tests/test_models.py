import time

from app.models import Domain


def test_new_domain(session):
    current_time = int(time.time())
    domain = Domain(link="https://ya.ru/", datetime=current_time)

    session.add(domain)
    session.commit()

    assert domain.id > 0
    assert domain.link == "https://ya.ru/"
    assert domain.datetime == current_time
    assert str(domain) == "https://ya.ru/"
