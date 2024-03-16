def test__returns_ok_status__when_api_is_working_correctly(client):
    response = client.get("/health_check/")

    response_content = response.json()
    assert response.status_code == 200
    assert response_content["status"] == "OK"
