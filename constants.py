from enum import Enum

AUTH_DEV_URL = "https://auth.dev-cinescope.coconutqa.ru"
API_DEV_URl = "https://api.dev-cinescope.coconutqa.ru"
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
MOVIES_ENDPOINT = "/movies"
USER_ENDPOINT = "/user"



class Roles(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

"""
Этот файл содержит все базовые константы проекта, такие как базовый URL, заголовки для
запросов и пути эндпоинтов. Это позволяет централизовать управление изменениями, чтобы
избежать ошибок, связанных с дублированием.

**Зачем это нужно?**

- Упрощает управление конфигурацией.
- Снижает вероятность ошибок при изменении базового URL или эндпоинтов.
"""