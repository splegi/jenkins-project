from app import app


def test_index():
    # Создаем тестовый клиент Flask
    client = app.test_client()

    # Делаем GET-запрос к главной странице
    response = client.get("/")

    # Проверяем, что статус-код 200 OK
    assert response.status_code == 200

    # Декодируем байты в строку
    html = response.data.decode("utf-8")

    assert "Привет, Jenkins!" in html
    assert "Это простое Flask-приложение для тренировки " "CI/CD пайплайнов." in html
