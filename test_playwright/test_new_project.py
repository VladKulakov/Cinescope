# from playwright.sync_api import sync_playwright
# import time
#
# # Создаем экземпляр Playwright и запускаем его
# playwright = sync_playwright().start()
#
# # Далее, используя объект playwright, можно запускать браузер и работать с ним
# browser = playwright.chromium.launch(headless=False)
# page = browser.new_page()
# page.goto('https://demoqa.com/')
# time.sleep(10)  # Сделаем sleep иначе браузер сразу закроектся перейдя к следующим строкам
#
# # После выполнения необходимых действий, следует явно закрыть браузер
# browser.close()
#
# # И остановить Playwright, чтобы освободить ресурсы
# playwright.stop()

# from playwright.sync_api import sync_playwright
# import time
#
#
# def test_multiple_browsers():
#     with sync_playwright() as p:
#         chromium_browser = p.chromium.launch(headless=False)
#         firefox_browser = p.firefox.launch(headless=False)
#
#         chromium_page = chromium_browser.new_page()
#         firefox_page = firefox_browser.new_page()
#
#         chromium_page.goto("https://demoqa.com")
#         firefox_page.goto("https://www.google.com")
#
#         time.sleep(10)
#
#         chromium_browser.close()
#         firefox_browser.close()









# from playwright.sync_api import sync_playwright
# import time
#
# def test_open_url():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context1 = browser.new_context()
#         context2 = browser.new_context()
#         page1 = context1.new_page()
#         page2 = context2.new_page()
#         page1.goto("https://www.google.com")
#         page2.goto("https://www.yandex.ru")
#         time.sleep(10)
#
#         page1.close()
#         page2.close()
#         context1.close()
#         context2.close()
#         browser.close()














# import time
#
# def test_example(page):  # page автоматически будет предоставлена фикстурой
#     start = time.time()
#     page.goto("https://www.yandex.ru")
#     time.sleep(10)
#     stop = time.time()
#     result = stop - start
#     print(result)
#
# def test_google(page):  # page автоматически будет предоставлена фикстурой
#     start = time.time()
#     page.goto("https://www.google.com")
#     time.sleep(10)
#     stop = time.time()
#     result = stop - start
#     print(result)












# from playwright.sync_api import Page
# import time
#
#
# def test_text_box(page: Page):
#     page.goto('https://demoqa.com/text-box')
#     page.fill(selector='#userName', value='testQa')
#     time.sleep(10)












# from playwright.sync_api import Page, expect
# import time
#
#
# def test_text_box(page: Page):
#     page.goto('https://demoqa.com/text-box')
#
#     username_locator = '#userName'
#     page.fill(username_locator, 'testQa')
#     page.fill('#userEmail', 'test@qa.com')
#     page.fill('#currentAddress', 'Phuket, Thalang 99')
#     page.fill('#permanentAddress', 'Moscow, Mashkova 1')
#
#     page.click('button#submit')
#     time.sleep(10)
#
#     expect(page.locator('#output #name')).to_have_text('Name:testQa')
#     expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
#     expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Phuket, Thalang 99')
#     expect(page.locator('#output #permanentAddress')).to_have_text('Permananet Address :Moscow, Mashkova 1')

#
# from playwright.sync_api import Page
# import time
# from random import randint
#
#
# def test_text_box(page: Page):
#     user_email = f"test_{randint(1, 9999)}@email.qa"
#     page.goto('https://dev-cinescope.coconutqa.ru/register')
#     page.fill(selector='[name="fullName"]', value='Жмышенко Валерий Альбертович')
#     page.fill(selector='[name="email"]', value=user_email)
#     page.fill(selector='[name="password"]', value='qwerty123Q')
#     page.fill(selector='[name="passwordRepeat"]', value='qwerty123Q')
#     time.sleep(10)










#
# from playwright.sync_api import Playwright, sync_playwright, expect
# import time

# def test_run(page):
#     page.pause()
#     page.goto("https://demoqa.com/")
#     page.get_by_role("link", name="Elements").click()
#     page.get_by_role("listitem").filter(has_text="Text Box").click()
#     page.get_by_role("textbox", name="Full Name").fill("Жмышенко Валерий Альбертович")
#     page.get_by_role("textbox", name="name@example.com").fill("Test12131331@email.qa")
#     page.get_by_role("textbox", name="Current Address").fill("qwerty123Q")
#
#     page.locator("#permanentAddress").fill("qwerty123Q")
#     page.get_by_role("button", name="Submit").click()
#     expect(page.locator("#name")).to_contain_text("Жмышенко Валерий Альбертович")
#     expect(page.locator("#email")).to_contain_text("Test12131331@email.qa")
#     expect(page.locator("#output")).to_contain_text("qwerty123Q")
#     expect(page.locator("#output")).to_contain_text("qwerty123Q")






# from playwright.sync_api import expect
# import time
# import re
#
# def test_web_table(page):
#     page.goto("https://demoqa.com/webtables")
#     page.get_by_role("button", name="Add").click()
#     expect(page.locator("div").filter(has_text="Registration Form").nth(3)).to_be_visible()
#     expect(page.locator("div").filter(has_text=re.compile(r"^First NameLast NameEmailAgeSalaryDepartmentSubmit$"))).to_be_visible()
#     page.get_by_placeholder("First Name").fill('Alex')
#     page.get_by_placeholder("Last Name").fill('Popov')
#     page.get_by_role("textbox", name="name@example.com").fill("vlad@gmail.com")
#     page.get_by_role("textbox", name="Age").fill("30")
#     page.get_by_role("textbox", name="Salary").fill("1000")
#     page.get_by_role("textbox", name="Department").fill("fa")
#     page.get_by_role("button", name="Submit").click()
#     time.sleep(5)








# from datetime import datetime
# from playwright.sync_api import expect, Page
# import time

# def test_web_table(page: Page):
#     page.goto("https://demoqa.com/automation-practice-form")
#     page.get_by_role('textbox', name="First Name").fill("Alex")
#     page.get_by_role('textbox', name="Last Name").type("Bobr", delay=100)
#     page.get_by_placeholder("name@example.com").type("bobr_kyrva@mail.ru", delay=100)
#     page.get_by_role("radio", name="Male", exact=True).check()
#     page.get_by_role("textbox", name="Mobile Number").fill("1234567890")
#     value = page.get_attribute("#dateOfBirthInput", 'value')
#     today_formatted = datetime.now().strftime("%d %B %Y")
#     assert value == today_formatted
#     value = page.get_by_text('© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED.', exact=True)
#     actual_text = value.text_content()
#     assert actual_text == '© 2013-2026 TOOLSQA.COM | ALL RIGHTS RESERVED.'
#     time.sleep(4)



#
# def test_radio_button(page: Page):
#     page.goto("https://demoqa.com/radio-button")
#     yes_enabled = page.get_by_role("radio", name="Yes").is_enabled()
#     assert yes_enabled,"Yes, не доступна"
#     impressive_enabled = page.get_by_role("radio", name="Impressive").is_enabled()
#     assert impressive_enabled, "Impressive, не доступна"
#     no_enabled = page.get_by_role("radio", name="No").is_enabled()
#     assert not no_enabled, "No, доступна"
#     expect(page.get_by_text("YesImpressiveNo")).to_be_visible()





#
# from datetime import datetime
# from playwright.sync_api import expect, Page
# import time
#
# def test_treeitem(page: Page):
#     page.goto("https://demoqa.com/checkbox")
#     expect(page.get_by_text("Home")).to_be_visible()
#     desktop = page.get_by_text("Desktop").is_visible()
#     assert not desktop
#     page.locator(".rc-tree-switcher").click()
#     desktop = page.get_by_text("Desktop").is_visible()
#     assert desktop



# from datetime import datetime
# from playwright.sync_api import expect, Page
# import time
#
# from pytest_check import check
#
#
# def test_viseble(page: Page):
#     page.goto('https://demoqa.com/dynamic-properties')
#     button_viseble = page.get_by_role("button", name="Visible After 5 Seconds").is_visible()
#     assert not button_viseble, "Button виден"
#     page.get_by_role("button", name="Visible After 5 Seconds").wait_for(timeout=10000, state="visible")
#     button_viseble = page.get_by_role("button", name="Visible After 5 Seconds").is_visible()
#     assert button_viseble, "Button2 не виден"
#
# # def test_viseble(page: Page):
# #     page.goto('https://demoqa.com/dynamic-properties')
# #     expect(page.get_by_text("Visible After 5 Seconds")).to_be_hidden()
# #     expect(page.get_by_text("Visible After 5 Seconds")).to_be_visible(timeout=10000)

from playwright.sync_api import Page, expect


def test_expect(page: Page):
    page.goto("https://demoqa.com/radio-button")
    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")
    expect(no_radio).to_be_disabled()  # проверяем, что не доступен
    expect(yes_radio).to_be_enabled()  # проверяем, что доступен
    expect(impressive_radio).to_be_enabled()  # проверяем, что доступен
    page.locator('[for="yesRadio"]').click()  # тут хитрый лейбл не позволяет кликнуть прямо на инпут, обращаемся по лейблу
    expect(yes_radio).to_be_checked()  # проверяем, что отмечен
    expect(impressive_radio).not_to_be_checked()