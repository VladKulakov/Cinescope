from pytest_check import check
import allure
from playwright.sync_api import Page, expect


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        with check:
            self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        with check:
            self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        with check:
            self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        with check:
            self.page.wait_for_url(url)

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        with check:
            return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible"):
        with check:
            self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        self.page.screenshot(path=screenshot_path, full_page=True)  # full_page=True для скриншота всей страницы
        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str):
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            with check:
                notification_locator.wait_for(state="visible")
        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            with check:
                notification_locator.wait_for(state="hidden")

    @allure.step("Проверка видимости элемента {locator} на странице")
    def visibility_check(self, locator: str):
        with check:
            expect(self.page.locator(locator).first).to_be_visible()

    @allure.step("Проверка disabled элемента {locator} на странице")
    def not_visible_check(self, locator: str):
        with check:
            expect(self.page.locator(locator).first).to_be_hidden()
