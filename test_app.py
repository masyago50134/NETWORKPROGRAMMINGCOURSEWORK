import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Тест для кореневого шляху (ЛБ2)
def test_hello_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello World!" in response.data

# Тест аутентифікації (ЛБ3): Перевірка доступу без пароля
def test_items_unauthorized(client):
    response = client.get('/items')
    assert response.status_code == 401
    assert b"Unauthorized" in response.data

# Тест аутентифікації (ЛБ3): Перевірка доступу з правильним паролем
def test_items_authorized(client):
    import base64
    valid_auth = base64.b64encode(b"admin:1234").decode('utf-8')
    response = client.get('/items', headers={'Authorization': f'Basic {valid_auth}'})
    assert response.status_code == 200

# Тест логіки отримання валюти (ЛБ2)
def test_currency_route(client):
    response = client.get('/currency?date=today')
    assert response.status_code == 200
    assert b"USD rate" in response.data