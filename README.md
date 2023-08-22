Introduction
------------

Объектом тестирования является веб-сайт "Ростелеком" (https://b2c.passport.rt.ru/)

По выше указанному веб-сайту был составлен набор тест-кейсов, авто-тестов и багов для тестирования функционала авторизации и регистрации нового пользователя.
Были использованы различные техники тест-дизайна. Для проверки длин вводимых строк в поля "Имя", "Фамилия", "Пароль" были использованы комбинированные техники граничных значений и классов эквивалентности. Также была использована техника предугадывания ошибок путем проверки ввода пустых значений. Эта техника также использовалась в тестах EXP-029 и EXP-031 - указание неверных паролей.

Ссылка на тест-кейсы и баги: [Google_doc](https://docs.google.com/spreadsheets/d/1Amw22s5HR_EPSnsA3P-oYNl8HWr-w8Up/edit#gid=287177797)

Ссылка на документацию: [Требования по проекту](https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Flms-cdn.skillfactory.ru%2Fassets%2Fcourseware%2Fv1%2F010c9924044551b87b76b5c3c624bd2a%2Fasset-v1%3ASkillFactory%2BQAP-D%2B2020%2Btype%40asset%2Bblock%2F%25D0%25A2%25D1%2580%25D0%25B5%25D0%25B1%25D0%25BE%25D0%25B2%25D0%25B0%25D0%25BD%25D0%25B8%25D1%258F_SSO_%25D0%25B4%25D0%25BB%25D1%258F_%25D1%2582%25D0%25B5%25D1%2581%25D1%2582%25D0%25B8%25D1%2580%25D0%25BE%25D0%25B2%25D0%25B0%25D0%25BD%25D0%25B8%25D1%258F_last.doc&wdOrigin=BROWSELINK)

Files
-----

[conftest.py](conftest.py) contains all the required code to catch failed test cases and make screenshot
of the page in case any test case will fail.

[pages/base.py](pages/base.py) contains PageObject pattern implementation for Python.

[pages/elements.py](pages/elements.py) contains helper class to define web elements on web pages.

[tests/test_auth_page.py](tests/test_auth_page.py) contains Web UI tests for authorization and registration on "Rostelecom" (https://b2c.passport.rt.ru/)

[pages/auth_page.py](pages/auth_page.py) contains initialization of URL and locators for main pages.

How To Run Tests
----------------

1) Install all requirements:

    ```bash
    pip3 install -r requirements
    ```
2) The correct Selenium WebDriver for Google Chrome v114 (Windows) has already located in project [driver/chromedriver.exe](driver/chromedriver.exe) 
 If this version isn't compatible with your browser or OS, you can load the new one in link https://chromedriver.chromium.org/downloads

3) Run tests:

    ```bash
    python3 -m pytest -v --driver Chrome --driver-path ~/chrome tests/*
    ```

4) Some of tests, which have the parametrised structure, were marked by "slow" and the others marked by "fast" in file [pytest.ini](pytest.ini)
   So the tests can run accordingly as parametrised or not by adding to run command marks below:

   ```bash
    -m slow
    ```
   or

   ```bash
   -m fast
    ```