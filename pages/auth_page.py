from pages.base import WebPage
from pages.elements import WebElement,ManyWebElements
import os

class AuthPage(WebPage):

    def __init__(self, web_driver, url=''):
        if not url:
            url = os.getenv("MAIN_URL") or 'https://b2c.passport.rt.ru/'

        super().__init__(web_driver, url)

    #страница авторизации
    #Меню-авторизация по почте
    authorization_by_email = WebElement(id="t-btn-tab-mail")
    #Поле ввода email
    email = WebElement(id='username')
    #Поле ввода пароля
    password = WebElement(id='password')
    #Кнопка входа
    login_btn = WebElement(id="kc-login")
    #неверный логин или пароль
    error_field_auth = WebElement(id='form-error-message')
    #Ссылка на пользовательское соглашение
    user_agreement = WebElement(xpath='//a[@class="rt-link rt-link--orange" and @target="_blank"]')
    #Ссылка регистрации
    registration_link = WebElement(id='kc-register')

    #личный кабинет, поле фамилия
    last_name_lk=WebElement(css_selector='span.user-name__last-name')

    # страница регистрации
    # Поле воода имени
    first_name = WebElement(name="firstName")
    # Поле ввода фамилии
    last_name = WebElement(name='lastName')
    # Поле ввода региона
    region = WebElement(xpath='//input[@autocomplete="new-password" and @type="text"]')
    # Поле ввода email
    email_for_registration=WebElement(id="address")
    # Поле ввода пароля
    password_for_registration=WebElement(id='password')
    # Поле подтверждения пароля
    password_confirm = WebElement(id='password-confirm')
    # Кнопка регистрации
    registration_btn = WebElement(name='register')
    # список ошибок(подсказок)
    fields_errors=ManyWebElements(css_selector='span.rt-input-container__meta--error')

    #Логотип и слоган
    logo_and_title=WebElement(css_selector='div.what-is-container')

    # старница с подтверждением кода по email
    # Заголовок подтверждения
    confirmation_email_title=WebElement(xpath='//h1[contains(text(), "Подтверждение email")]')

    #форма о существующем учетной записи
    #Заголовок
    title_user_exist=WebElement(css_selector='h2.card-modal__title')
    #Кнопка входа
    login_btn_user_exist=WebElement(name = "gotoLogin")
    #Кнопка восстановления пароля
    recover_password=WebElement(id="reg-err-reset-pass")


