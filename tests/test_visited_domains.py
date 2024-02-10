from app.models import Domain


def create_db(session):
    domains = [
        ("https://ya.ru/", 1545221231),
        ("https://ya.ru/search/?text=мемы+с+котиками", 1545221232),
        ("https://sber.ru", 1545224567),
        ("https://stackoverflow.com/questions/65724760/how-it-is", 1545224567),
    ]

    for d in domains:
        domain = Domain(link=d[0], datetime=d[1])
        session.add(domain)

    session.commit()


def test_withot_params(session, test_client):
    create_db(session)

    response = test_client.get("/visited_domains")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == ["ya.ru", "sber.ru", "stackoverflow.com"]


def test_with_both_params_full(session, test_client):
    create_db(session)

    response = test_client.get("/visited_domains?from=1545221231&to=1545224567")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == ["ya.ru", "sber.ru", "stackoverflow.com"]


def test_with_both_params_part(session, test_client):
    create_db(session)
    response = test_client.get("/visited_domains?from=1545224567&to=1545224567")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == ["sber.ru", "stackoverflow.com"]


def test_with_both_params_empty(session, test_client):
    create_db(session)
    response = test_client.get("/visited_domains?from=1545224568&to=1545225673")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == []


def test_with_only_from_full(session, test_client):
    create_db(session)

    response = test_client.get("/visited_domains?from=1545221231")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == ["ya.ru", "sber.ru", "stackoverflow.com"]


def test_with_only_from_part(session, test_client):
    create_db(session)
    response = test_client.get("/visited_domains?from=1545224567")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == ["sber.ru", "stackoverflow.com"]


def test_with_only_from_empty(session, test_client):
    create_db(session)
    response = test_client.get("/visited_domains?from=1545224568")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == []


def test_with_only_to_full(session, test_client):
    create_db(session)

    response = test_client.get("/visited_domains?to=1545224567")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == ["ya.ru", "sber.ru", "stackoverflow.com"]


def test_with_only_to_part(session, test_client):
    create_db(session)
    response = test_client.get("/visited_domains?to=1545221232")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == ["ya.ru"]


def test_with_only_to_empty(session, test_client):
    create_db(session)
    response = test_client.get("/visited_domains?to=1545221230")
    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
    assert response.json.get("domains") == []
