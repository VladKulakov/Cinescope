import time, pytest, allure
from playwright.sync_api import Page
from models.ui_page_object.сinescop_review_page import CinescopReviewPage
from pytest_check import check

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Movie")
@pytest.mark.ui
class TestFeedbackPage:
    @allure.title("Оставляем отзыв под фильмом")
    def test_feedback_page(self, page: Page, registered_user):
        page = CinescopReviewPage(page)
        with check:
            page.open_via_auth(registered_user.email, registered_user.password)
        with check:
            page.all_elements_visibility_check_auth()
        with check:
            page.fill_review('Отличный фильм на вечер')
        with check:
            page.check_pop_up_message()
        time.sleep(5)

    @allure.title("Проверяем, что без авторизации, не можем оставить отзыв под фильмом")
    def test_feedback_page_not_auth(self, page: Page):
        page = CinescopReviewPage(page)
        with check:
            page.open()
        with check:
            page.all_elements_visibility_check_not_auth()
        time.sleep(5)