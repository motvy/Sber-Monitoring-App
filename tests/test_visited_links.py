from app.models import Domain


def test_without_param(session, test_client):
    response = test_client.post("/visited_links", json={})

    assert response.status_code == 400
    assert "status" in response.json
    assert response.json.get("status") == "The links parameter is not specified"

    links = [d.link for d in Domain.query.all()]
    assert links == []


def test_incorrect_param(session, test_client):
    response = test_client.post("/visited_links", json={"links": "https://google.com/"})

    assert response.status_code == 400
    assert "status" in response.json
    assert (
        response.json.get("status")
        == "Parameter links is not list: https://google.com/"
    )

    links = [d.link for d in Domain.query.all()]
    assert links == []


def test_correct_param_full(session, test_client):
    test_data = {
        "links": [
            "https://google.com/",
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "http://sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is",
        ]
    }

    response = test_client.post("/visited_links", json=test_data)

    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"

    links = []
    datetimes = []
    for d in Domain.query.all():
        links.append(d.link)
        datetimes.append(d.datetime)

    assert links == test_data["links"]
    assert len(set(datetimes)) == 1


def test_correct_param_part(session, test_client):
    test_data = {
        "links": [
            "google.com/profile",
            "http://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "sber.ru",
            "https://stackoverflow.com/questions/65724760/how-it-is",
        ]
    }

    response = test_client.post("/visited_links", json=test_data)

    assert response.status_code == 207
    assert "status" in response.json
    assert (
        response.json.get("status")
        == "Incorrect links were ignored in the request: google.com/profile, sber.ru"
    )

    links = []
    datetimes = []
    for d in Domain.query.all():
        links.append(d.link)
        datetimes.append(d.datetime)

    assert links == [
        "http://ya.ru/",
        "https://ya.ru/search/?text=мемы+с+котиками",
        "https://stackoverflow.com/questions/65724760/how-it-is",
    ]

    assert len(set(datetimes)) == 1


def test_correct_param_empty(session, test_client):
    test_data = {
        "links": [
            "google.com/profile",
            "htt://ya.ru/search/?text=мемы+с+котиками",
            "sber.ru",
        ]
    }

    response = test_client.post("/visited_links", json=test_data)
    assert response.status_code == 400
    assert "status" in response.json
    assert (
        response.json.get("status")
        == "Incorrect links were ignored in the request: google.com/profile, htt://ya.ru/search/?text=мемы+с+котиками, sber.ru"
    )

    links = [d.link for d in Domain.query.all()]
    assert links == []
