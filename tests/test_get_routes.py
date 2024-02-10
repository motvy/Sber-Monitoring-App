def test_not_found(test_client, session):
    response = test_client.get("/visited_domain")

    assert response.status_code == 404
    assert "status" in response.json
    assert response.json.get("status") == "No matching route for request"


def test_withot_params(test_client, session):
    response = test_client.get("/visited_domains")

    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json


def test_incorrect_interval(test_client, session):
    response = test_client.get("visited_domains?from=1645221231&to=1545217638")

    assert response.status_code == 400
    assert "status" in response.json
    assert (
        response.json.get("status")
        == "Parameter from cannot be greater than parameter to: 1645221231 > 1545217638"
    )
    assert "domains" not in response.json


def test_incorrect_format_to(test_client, session):
    response = test_client.get("visited_domains?from=1645221231&to=qqq")

    assert response.status_code == 400
    assert "status" in response.json
    assert response.json.get("status") == "Parameter to is not digit: qqq"
    assert "domains" not in response.json


def test_incorrect_format_from(test_client, session):
    response = test_client.get("visited_domains?from=[123, 456]&to=1645221231")

    assert response.status_code == 400
    assert "status" in response.json
    assert response.json.get("status") == "Parameter from is not digit: [123, 456]"
    assert "domains" not in response.json


def test_incorrect_size_to(test_client, session):
    response = test_client.get(
        "visited_domains?from=1645221231&to=100000000000000000000000000000000000"
    )

    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json


def test_incorrect_size_from(test_client, session):
    response = test_client.get(
        "visited_domains?from=100000000000000000000000000000000000"
    )

    assert response.status_code == 200
    assert "status" in response.json
    assert response.json.get("status") == "ok"
    assert "domains" in response.json
