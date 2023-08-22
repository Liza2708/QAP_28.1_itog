import pytest
from pages.auth_page import AuthPage
import pickle
import random
import time

# регистрация меток
def pytest_configure(config):
    # регистрируется метка `@pytest.mark.fast`
    config.addinivalue_line("markers", "fast: маркер зарегистрирован программно.")
    # регистрируется метка `@pytest.mark.slow`
    config.addinivalue_line("markers", "slow: медленный тест.")

#Генерация случайных строк
def generate_random_string_english(length=6):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def generate_random_string_english_Upper(length=3):
    str_upper = generate_random_string_english(length)
    return str_upper.upper()


def generate_random_string_russin(length=6):
   letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
   rand_string = ''.join(random.choice(letters) for i in range(length))
   return rand_string

def generate_random_string_special_chars(length=6):
    letters = '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

# EXP-001
# Баг FB-001
@pytest.mark.fast
def test_click_registration_link(web_browser):
    """Переход по ссылке 'Зарегистрироваться'"""
    page = AuthPage(web_browser)
    #клик на сслыку регистрации
    page.registration_link.click()
    #проверка наличия элементов на странице согласно требованиям
    assert page.first_name.is_presented()
    assert page.last_name.is_presented()
    assert page.region.is_presented()
    assert page.email_for_registration.is_presented()
    assert page.password_for_registration.is_presented()
    assert page.password_confirm.is_presented()
    assert page.registration_btn.is_clickable()
    assert page.logo_and_title.is_presented()
    # проверка на наличие JS ошибок
    assert page.check_js_errors()

# EXP-002
# Баг FB-002
@pytest.mark.fast
def test_registration_new_user_with_valid_data(web_browser):
    """Регистрация нового пользователя"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    #ввод полей для заполнения (поле региона заполняется автоматически)
    page.first_name.send_keys("Алла")
    page.last_name.send_keys("Андреева")
    page.email_for_registration.send_keys(generate_random_string_english()+"@mail.ru")
    page.password_for_registration.send_keys("1234Qwerty")
    page.password_confirm.send_keys("1234Qwerty")
    #клик на кнопку регистрации
    page.registration_btn.click()

    #проверяем, что на странице отображается заголовок для подтверждение кода, и наличие JS ошибок
    assert page.confirmation_email_title.is_presented()
    assert page.check_js_errors()

# EXP-003
# Баг FB-003
@pytest.mark.fast
def test_registration_existing_user(web_browser):
    """Регистрация уже зарегистрированного пользователя"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.first_name.send_keys("Алла")
    page.last_name.send_keys("Андреева")
    page.email_for_registration.send_keys("ldarovskaya@yandex.ru")
    page.password_for_registration.send_keys("1234Qwerty")
    page.password_confirm.send_keys("1234Qwerty")
    # клик на кнопку регистрации
    page.registration_btn.click()

    # проверяем наличие всплывающей формы о существовании учетной записи
    assert page.title_user_exist.is_presented()
    assert page.login_btn_user_exist.is_presented()
    assert page.password_confirm.is_presented()


# EXP-004,EXP-005
@pytest.mark.slow
@pytest.mark.parametrize("name", ['', '0'], ids=['empty string', 'zero'])
@pytest.mark.parametrize("last_name", ['', '0'], ids=['empty string', 'zero'])
@pytest.mark.parametrize("email", ['', '0'], ids=['empty string', 'zero'])
@pytest.mark.parametrize("password", ['', '0'], ids=['empty string', 'zero'])
@pytest.mark.parametrize("password_conf", ['', '0'], ids=['empty string', 'zero'])
def test_registration_fields_by_zero_and_empty(web_browser, name, last_name, email, password, password_conf):
    """Заполнение полей регистрации пустыми значениями и нулями"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.first_name.send_keys(name)
    page.last_name.send_keys(last_name)
    page.email_for_registration.send_keys(email)
    page.password_for_registration.send_keys(password)
    page.password_confirm.send_keys(password_conf)
    # клик на кнопку регистрации
    page.registration_btn.click()

    # проверяем появление всплывающих подсказок к каждому полю (должно быть 5)
    assert page.fields_errors.is_presented()
    assert page.fields_errors.length() == 5


# EXP-007,EXP-008, EXP-009, EXP-010
@pytest.mark.slow
@pytest.mark.parametrize("name", [generate_random_string_russin(2), generate_random_string_russin(3), generate_random_string_russin(29), generate_random_string_russin(30)], ids =['length=2', 'length=3', 'length=29', 'length=30'])
def test_registration_field_name_positive(web_browser, name):
    """Проверка граничных значений поля "Имя", позитивные тесты"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.first_name.send_keys(name)
    # клик на кнопку регистрации
    page.registration_btn.click()
    # проверяем, что подсказок стало 4 (поле имя заполнено верно)
    assert page.fields_errors.length() == 4

# EXP-006,EXP-011, EXP-012
@pytest.mark.slow
@pytest.mark.parametrize("name", [generate_random_string_russin(1), generate_random_string_russin(31), generate_random_string_english(6),'123',generate_random_string_special_chars(6)], ids =['length<min', 'length>max', 'english_chars', 'digits', 'spesial_chars'])
def test_registration_field_name_negative(web_browser, name):
    """Проверка граничных значений поля "Имя" + заполнение недопустимыми символами, негативный тест"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.first_name.send_keys(name)
    # клик на кнопку регистрации
    page.registration_btn.click()
    #отображение всплывающей подсказки?
    assert page.fields_errors.length() == 1

# EXP-014,EXP-015, EXP-016, EXP-017
@pytest.mark.slow
@pytest.mark.parametrize("last_name", [generate_random_string_russin(2), generate_random_string_russin(3), generate_random_string_russin(29), generate_random_string_russin(30)], ids =['length=2', 'length=3', 'length=29', 'length=30'])
def test_registration_field_last_name_positive(web_browser, last_name):
    """Проверка граничных значений поля "Фамилия", позитивные тесты"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.last_name.send_keys(last_name)
    # клик на кнопку регистрации
    page.registration_btn.click()
    # проверяем, что подсказок стало 4 (поле фамилия заполнено верно)
    assert page.fields_errors.length() == 4

# EXP-013,EXP-018, EXP-019
@pytest.mark.slow
@pytest.mark.parametrize("last_name", [generate_random_string_russin(1), generate_random_string_russin(31), generate_random_string_english(6),'123',generate_random_string_special_chars(6)], ids =['length<min', 'length>max', 'english_chars', 'digits', 'spesial_chars'])
def test_registration_field_last_name_negative(web_browser, last_name):
    """Проверка граничных значений поля "Фамилия" + заполнение недопустимыми символами, негативный тест"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.last_name.send_keys(last_name)
    # клик на кнопку регистрации
    page.registration_btn.click()
    #отображение всплывающей подсказки?
    assert page.fields_errors.length() == 1

# EXP-022,EXP-023, EXP-024, EXP-025
@pytest.mark.slow
@pytest.mark.parametrize("passw", [generate_random_string_english_Upper(2)+generate_random_string_english(5)+'1', generate_random_string_english_Upper(2)+generate_random_string_english(5)+'12', generate_random_string_english_Upper(2)+generate_random_string_english(15)+'12', generate_random_string_english_Upper(2)+generate_random_string_english(15)+'123'], ids =['length=8', 'length=9', 'length=19', 'length=20'])
def test_registration_field_password_positive(web_browser, passw):
    """Проверка граничных значений поля "Пароль", позитивные тесты"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.password_for_registration.send_keys(passw)
    # клик на кнопку регистрации
    page.registration_btn.click()
    # проверяем, что подсказок стало 4 (поле пароль заполнено верно)
    assert page.fields_errors.length() == 4

# EXP-021,EXP-026, EXP-027, EXP-028
@pytest.mark.slow
@pytest.mark.parametrize("passw", [generate_random_string_english_Upper(2)+generate_random_string_english(4)+'1', generate_random_string_english_Upper(2)+generate_random_string_english(17)+'12', generate_random_string_russin(9), generate_random_string_english(8)+'1'], ids =['length<min', 'length>max', 'russian_chars', 'lower_english'])
def test_registration_field_password_negative(web_browser, passw):
    """Проверка граничных значений поля "Пароль" + заполнение недопустимыми символами, негативный тест"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод полей для заполнения (поле региона заполняется автоматически)
    page.password_for_registration.send_keys(passw)
    # клик на кнопку регистрации
    page.registration_btn.click()
    #отображение всплывающей подсказки?
    assert page.fields_errors.length() == 5 or page.fields_errors.length() == 1


# EXP-029
@pytest.mark.fast
def test_registration_passwords_dont_match(web_browser):
    """Ввод в поле "Подтверждение пароля" пароля отличного от поля "Пароль"""
    page = AuthPage(web_browser)
    page.registration_link.click()

    # ввод паролей
    page.password_for_registration.send_keys('1234Qwerty')
    page.password_confirm.send_keys('1234Qwertt')

    # клик на кнопку регистрации
    page.registration_btn.click()

    # подсказка отображается лишь для поля подтверждения пароля
    assert page.fields_errors.length() == 4


# EXP-030
# Баг FB-004
@pytest.mark.fast
def test_authorization_by_email_with_valid_data(web_browser):
    """Авторизация в личном кабинете по почте"""
    page = AuthPage(web_browser)

    #переход на вкладку авторизации по почте
    page.authorization_by_email.click()
    #ввод пароля и почты валидными данными
    page.email.send_keys('ldarovskaya@yandex.ru')
    page.password.send_keys('173AsD2708')
    # клик на кнопку входа
    page.login_btn.click()

    #проверка отображения фамилии пользователя в ЛК
    assert page.last_name_lk.is_presented()
    #проверка на JS ошибки
    assert page.check_js_errors()

# EXP-031
@pytest.mark.fast
def test_authorization_by_email_with_not_valid_password(web_browser):
    """Авторизация в личном кабинете по почте с неверно указанным паролем"""
    page = AuthPage(web_browser)

    # переход на вкладку авторизации по почте
    page.authorization_by_email.click()
    # ввод пароля и почты валидными данными
    page.email.send_keys('ldarovskaya@yandex.ru')
    page.password.send_keys('1234Qwerty')
    # клик на кнопку входа
    page.login_btn.click()
    time.sleep(5)
    assert page.error_field_auth.is_presented()
