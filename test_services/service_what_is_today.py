import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()


class DateTimeRequest(BaseModel):
    currentDateTime: str  # Формат: "2025-02-13T21:43Z"
# Список праздников в России (пример)
russian_holidays = {
    "01-01": "Новый год",
    "01-07": "Рождество Христово",
    "02-23": "День защитника Отечества",
    "03-08": "Международный женский день",
    "05-01": "Праздник Весны и Труда",
    "05-09": "День Победы",
    "06-12": "День России",
    "11-04": "День народного единства",
    "12-31": "Канун Нового года"
}
@app.post("/what_is_today")
def what_is_today(request: DateTimeRequest):
    try:
        # Парсим дату из входного JSON
        date_str = request.currentDateTime
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%MZ")
        # Получаем месяц и день в формате "MM-DD"
        month_day = date_obj.strftime("%m-%d")
        # Проверяем, есть ли праздник на эту дату
        holiday = russian_holidays.get(month_day, "Сегодня нет праздников в России.")
        return {"message": holiday}

    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный формат даты. Используйте формат 'YYYY-MM-DDTHH:MMZ'.")

@app.get("/ping")
def ping():
    return "PONG!"

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=16002)



# import datetime
# from datetime import datetime
# from unittest.mock import Mock
#
# import pytz
# import requests
# from pydantic import BaseModel, Field


# Модель Pydantic для ответа сервера worldclockapi
# class WorldClockResponse(BaseModel):
#     id: str = Field(alias="$id")  # Используем алиас для поля "$id"
#     currentDateTime: str
#     utcOffset: str
#     isDayLightSavingsTime: bool
#     dayOfTheWeek: str
#     timeZoneName: str
#     currentFileTime: int
#     ordinalDate: str
#     serviceResponse: None
#
#     class Config:
#         # Разрешаем использование алиасов при парсинге JSON
#         allow_population_by_field_name = True
#
#
# # Модель для запроса к сервису TodayIsHoliday
# class DateTimeRequest(BaseModel):
#     currentDateTime: str  # Формат: "2025-02-13T21:43Z"
#
#
# # Модель для ответа от сервиса TodayIsHoliday
# class WhatIsTodayResponse(BaseModel):
#     message: str
#
#
# # Функция выолняющая запрос в сервис worldclockapi для получения текущей даты
# def get_worldclockap_time() -> WorldClockResponse:
#     # Выполняем GET-запрос
#     response = requests.get("https://worldclockapi.com/api/json/utc/now",
#                             verify=False)  # Запрос в реальный сервис
#     # Проверяем статус ответа
#     assert response.status_code == 200, "Удаленный сервис недоступен"
#     # Парсим JSON-ответ с использованием Pydantic модели
#     return WorldClockResponse(**response.json())
#
#
# class TestTodayIsHolidayServiceAPI:
#     # worldclockap
#     def test_worldclockap(self):  # проверка работоспособности сервиса worldclockap
#         world_clock_response = get_worldclockap_time()
#         # Выводим текущую дату и время
#         current_date_time = world_clock_response.currentDateTime
#         print(f"Текущая дата и время: {current_date_time=}")
#
#         assert current_date_time == datetime.now(pytz.utc).strftime("%Y-%m-%dT%H:%MZ"), "Дата не совпадает"
#
#     def test_what_is_today(self):  # проверка работоспособности Fake сервиса what_is_today
#         # Запрашиваем текущее время у сервиса worldclockap
#         world_clock_response = get_worldclockap_time()
#
#         what_is_today_response = requests.post("http://127.0.0.1:16002/what_is_today",
#                                                data=DateTimeRequest(
#                                                    currentDateTime=world_clock_response.currentDateTime).model_dump_json()
#                                                )
#
#         # Проверяем статус ответа от тестируемогосервиса
#         assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
#         # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
#         what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
#         # Проводим валидацию ответа тестируемого сервиса
#         assert what_is_today_data.message == "Сегодня нет праздников в России.", "Сегодня нет праздника!"
#
#     def test_what_is_today_by_mock(self, mocker):
#         # 1. Мокаем внешний сервис worldclockapi
#         mock_worldclock_response = Mock()
#         mock_worldclock_response.currentDateTime = "2025-01-01T00:00Z"
#
#         mocker.patch(
#             "service_what_is_today.get_worldclockap_time",
#             return_value=mock_worldclock_response
#         )
#
#         # 2. Мокаем POST-запрос к вашему тестируемому сервису
#         mock_post_response = Mock()
#         mock_post_response.status_code = 200
#         mock_post_response.json.return_value = {
#             "message": "Новый год"  # Ожидаемый ответ от сервиса для 1 января
#         }
#
#         mocker.patch("requests.post", return_value=mock_post_response)
#
#         # Выполняем тест
#         world_clock_response = get_worldclockap_time()
#
#         what_is_today_response = requests.post(
#             "http://127.0.0.1:16002/what_is_today",
#             data=DateTimeRequest(
#                 currentDateTime=world_clock_response.currentDateTime
#             ).model_dump_json()
#         )
#
#         # Проверки
#         assert what_is_today_response.status_code == 200
#         what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
#         assert what_is_today_data.message == "Новый год", "ДОЛЖЕН БЫТЬ НОВЫЙ ГОД!"
#
#
#     def run_wiremock_what_is_today(self):
#         """Настройка WireMock для эмуляции what_is_today сервиса"""
#         wiremock_url = "http://localhost:8080/__admin/mappings"
#
#         mapping = {
#             "request": {
#                 "method": "POST",
#                 "url": "/what_is_today"
#             },
#             "response": {
#                 "status": 200,
#                 "jsonBody": {
#                     "message": "Международный женский день"
#                 }
#             }
#         }
#         response = requests.post(wiremock_url, json=mapping)
#         assert response.status_code == 201, "Не удалось настроить WireMock для what_is_today"
#
#
#     def run_wiremock_worldclockap_time(self):
#     # Запуск WireMock сервера (если используется standalone, этот шаг можно пропустить)
#         wiremock_url = "http://localhost:8080/__admin/mappings"
#
#
#         mapping = {
#             "request": {
#                 "method": "GET",
#                 "url": "/api/json/utc/now"  # Путь как у реального API
#             },
#             "response": {
#                 "status": 200,
#                 "jsonBody": {
#                     "$id": "1",
#                     "currentDateTime": "2025-03-08T00:00Z",  # 8 марта
#                     "utcOffset": "+00:00",
#                     "isDayLightSavingsTime": False,
#                     "dayOfTheWeek": "Saturday",
#                     "timeZoneName": "UTC",
#                     "currentFileTime": 1324567890123,
#                     "ordinalDate": "2025-03-08",
#                     "serviceResponse": None
#                 },
#                 "headers": {
#                     "Content-Type": "application/json"
#                 }
#             }
#         }
#         response = requests.post(wiremock_url, json=mapping)
#         assert response.status_code == 201, "Не удалось настроить WireMock"
#
#     def test_what_is_today_by_wiremock(self):  # Данный тест максимально похож на базовый
#         # запускаем наши мок серверы
#         self.run_wiremock_worldclockap_time()
#         self.run_wiremock_what_is_today()  # ← ДОБАВИТЬ ЭТУ СТРОКУ
#
#         # Выполняем запрос к WireMock (имитация worldclockapi)
#         world_clock_response = requests.get("http://localhost:8080/api/json/utc/now")
#         assert world_clock_response.status_code == 200, "Удаленный сервис недоступен"
#         # Парсим JSON-ответ с использованием Pydantic модели
#         current_date_time = WorldClockResponse(**world_clock_response.json()).currentDateTime
#
#         # Выполняем запрос к WireMock (имитация what_is_today)
#         what_is_today_response = requests.post(
#             "http://127.0.0.1:8080/what_is_today",  # порт 8080 (WireMock)
#             data=DateTimeRequest(currentDateTime=current_date_time).model_dump_json()
#         )
#
#         # Проверяем статус ответа от тестируемого сервиса
#         assert what_is_today_response.status_code == 200, "Удаленный сервис недоступен"
#         # Парсим JSON-ответ от тестируемого сервиса с использованием Pydantic модели
#         what_is_today_data = WhatIsTodayResponse(**what_is_today_response.json())
#         # Проверяем, что ответ соответствует ожидаемому
#         assert what_is_today_data.message == "Международный женский день", "8 марта же?"
# import allure  # Импортируем пакет allure
# import pytest
#
#
# @allure.title("Проверка сложения двух чисел")
# @allure.description("Тест проверяет, что сумма двух чисел вычисляется корректно")
# def test_addition():
#     with allure.step("Проверка суммы 2 + 2"):
#         assert 2 + 2 == 4
#
#     with allure.step("Проверка суммы 3 + 2"):
#         assert 3 + 2 == 5










