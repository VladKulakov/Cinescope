import allure
from playwright.sync_api import expect, Page
from models.page_object_models import BasePage
from pytest_check import check

class CinescopReviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_login_button = "button[type='button']:has-text('Войти')" #Войти через хедар
        self.movie_button = "button:has-text('Подробнее')" #Подробней о фильме
        self.title = "h2.text-6xl" #Заголовок
        self.description = "p.mt-10.text-lg" #Описание фильма
        self.genre = "p:has-text('Жанр:')"  # Жанр фильма
        self.rating = "div.w-\[500px\] h3:has-text('Рейтинг:')"  # Блок с рейтингом фильма
        self.rating_value = "div.w-\[500px\] span.underline"  # Значение рейтинга (3.8/5)
        self.poster = "img[width='500'][height='500']"  # Постер фильма
        self.buy_button = "div.bg-blue-500"  # Кнопка "Купить билет"
        self.cart_icon = "svg.lucide-shopping-cart"  # Иконка корзины
        self.price = "div.bg-blue-500 p"  # Цена билета (236 руб.)
        self.user_icon = "div.rounded-full p"  # Иконка пользователя (буква "Ж")
        self.profile_button = "a[href='/profile'] button"  # Кнопка "Профиль"
        self.reviews_section = "h2:has-text('Отзывы')"  # Заголовок секции отзывов
        self.review_author = "h4"  # Имя автора отзыва
        self.review_text = "li p"  # Текст отзыва
        self.review_rating = "li h3:has-text('Рейтинг:')"  # Рейтинг в отзыве
        self.review_textarea_placeholder = "textarea[placeholder='Написать отзыв']"  # Поле по placeholder
        self.review_submit_button = "button[type='submit']"  # Кнопка отправки отзыва
        self.review_rating_select = "select[name='rating']"  # Выбор оценки (звезды/select)

    @allure.step("Открытие страницы Фильм с Авторизацией")
    def open_via_auth(self, email, password):
        self.open_url(self.home_url)
        self.click_element(self.home_login_button)
        self.enter_text_to_element(self.login_email_input, email)
        self.enter_text_to_element(self.login_password_input, password)
        self.click_element(self.login_button)
        self.click_element(self.movie_button)

    @allure.step("Открытие страницы Фильм без Авторизации")
    def open(self):
        self.open_url(self.home_url)
        self.click_element(self.movie_button)


    @allure.step("Проверка видимости всех элементов страницы фильма без Авторизацией")
    def all_elements_visibility_check_not_auth(self):
        self.visibility_check(self.home_button)
        self.visibility_check(self.all_movies_button)
        self.not_visible_check(self.user_icon)
        self.visibility_check(self.title)
        self.visibility_check(self.description)
        self.visibility_check(self.genre)
        expect(self.page.locator(self.rating).first).to_be_visible()
        expect(self.page.locator(self.rating_value).first).to_be_visible()
        self.visibility_check(self.poster)
        self.visibility_check(self.buy_button)
        self.visibility_check(self.cart_icon)
        self.visibility_check(self.price)
        self.visibility_check(self.reviews_section)
        self.visibility_check(self.review_author)
        self.visibility_check(self.review_text)
        self.visibility_check(self.review_rating)
        self.not_visible_check(self.review_textarea_placeholder)
        self.not_visible_check(self.review_submit_button)

    @allure.step("Проверка видимости всех элементов страницы фильма с Авторизацией")
    def all_elements_visibility_check_auth(self):
        self.visibility_check(self.home_button)
        self.visibility_check(self.all_movies_button)
        self.visibility_check(self.user_icon)
        self.visibility_check(self.profile_button)
        self.visibility_check(self.title)
        self.visibility_check(self.description)
        self.visibility_check(self.genre)
        expect(self.page.locator(self.rating).first).to_be_visible()
        expect(self.page.locator(self.rating_value).first).to_be_visible()
        self.visibility_check(self.poster)
        self.visibility_check(self.buy_button)
        self.visibility_check(self.cart_icon)
        self.visibility_check(self.price)
        self.visibility_check(self.reviews_section)
        self.visibility_check(self.review_author)
        self.visibility_check(self.review_text)
        self.visibility_check(self.review_rating)
        self.visibility_check(self.review_textarea_placeholder)
        self.visibility_check(self.review_submit_button)

    @allure.step("Добавляем и отправляем отзыв")
    def fill_review(self, text):
        self.enter_text_to_element(self.review_textarea_placeholder, text)
        self.click_element(self.review_submit_button)

    @allure.step("Проверяем всплывающие окно")
    def check_pop_up_message(self):
        self.check_pop_up_element_with_text("Отзыв успешно создан")