import allure
from playwright.sync_api import Page
from models.ui_page_object.page_object_action import PageAction


class BasePage(PageAction): #Базовая логика доспустимая для всех страниц на сайте
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"
        self.login_email_input = "input[name='email']"
        self.login_password_input = "input[name='password']"
        self.login_button = 'button[type="submit"]:has-text("Войти")'

        # Общие локаторы для всех страниц на сайте
        self.home_button = "a[href='/']:has-text('Cinescope')"
        self.all_movies_button = "a[href='/movies']:has-text('Все фильмы')"
        self.header_login_button = "header button:has-text('Войти')"  # Кнопка "Войти"
        self.user_icon = "div.rounded-full" # Круглая иконка пользователя
        self.profile_button = "button:has-text('Профиль')"  # Кнопка "Профиль"

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies(self):
        self.click_element(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")