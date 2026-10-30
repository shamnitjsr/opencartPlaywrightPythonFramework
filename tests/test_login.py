"""
Test Case: User Login Functionality

===========================================
Test Steps
===========================================

Test Case 1: Verify Login with Invalid Credentials
--------------------------------------------------
1. Open the application in the browser.
2. Navigate to the "My Account" menu on the Home page.
3. Click on the "Login" link.
4. Enter an invalid email address and password.
5. Click on the "Login" button.
6. Verify that an error message appears indicating invalid credentials.

Expected Result:
----------------
An error message should be displayed, and the user should not be logged in.


Test Case 2: Verify Login with Valid Credentials
------------------------------------------------
1. Open the application in the browser.
2. Navigate to the "My Account" menu on the Home page.
3. Click on the "Login" link.
4. Enter a valid email address and password.
5. Click on the "Login" button.
6. Verify that the "My Account" page is displayed after successful login.

Expected Result:
----------------
The "My Account" page should appear, confirming a successful login.
"""
import re
import time
import allure

import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from playwright.sync_api import expect
from config import Config    # Configuration file holding credentials



@allure.epic("OpenCart Web Shop")
@allure.feature("Login")
@allure.story("PROJ-101: Valid user login")
@allure.issue("PROJ-101", "User story: Valid user login")
@allure.testcase("PROJ-101", "TC001_LoginValidUser")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("TC001_LoginValidUser")
@allure.description("Verify a registered user can log in with valid credentials")
@pytest.mark.sanity
def test_valid_user_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)
    my_account_page = MyAccountPage(page)

    with allure.step("Open the login page"):
        home_page.click_my_account()
        home_page.click_login()

    with allure.step("Log in with valid credentials"):
        login_page.set_email(Config.email)
        login_page.set_password(Config.password)
        login_page.click_login()

    with allure.step("Verify the My Account page is displayed"):
        expect(my_account_page.get_my_account_page_heading()).to_be_visible(timeout=6000)


@allure.epic("OpenCart Web Shop")
@allure.feature("Login")
@allure.story("PROJ-101: Invalid user login")
@allure.issue("PROJ-101", "User story: InValid user login")
@allure.testcase("PROJ-101", "TC002_LoginBothInvalidEmailPassword")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("TC002_LoginBothInvalidEmailPassword")
@allure.description("Verify a login fail if Invalid Email and Password both valid credentials")
@pytest.mark.regression
def test_invalid_user_both_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(Config.invalid_email)
    login_page.set_password(Config.invalid_password)
    login_page.click_login()

    time.sleep(3)

    expect(login_page.get_login_error()).to_be_visible(timeout=3000)


@allure.epic("OpenCart Web Shop")
@allure.feature("Login")
@allure.story("PROJ-101: Invalid user login")
@allure.issue("PROJ-101", "User story: InValid user login")
@allure.testcase("PROJ-101", "TC003_LoginInvalidEmailValidPassword")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("TC003_LoginInvalidEmailValidPassword")
@allure.description("Verify a login fail if Invalid Email and Valid Password")
@pytest.mark.regression
@pytest.mark.sanity
def test_invalid_email_and_Valid_password_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(Config.invalid_email)
    login_page.set_password(Config.password)
    login_page.click_login()

    time.sleep(3)

    expect(login_page.get_login_error()).to_be_visible(timeout=3000)


@allure.epic("OpenCart Web Shop")
@allure.feature("Login")
@allure.story("PROJ-101: Invalid user login")
@allure.issue("PROJ-101", "User story: InValid user login")
@allure.testcase("PROJ-101", "TC004_LoginValidEmailInvalidPassword")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("TC004_LoginValidEmailInvalidPassword")
@allure.description("Verify a login fail if Valid Email and Invalid Password")
@pytest.mark.regression
def test_valid_email_and_invalid_password_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    home_page.click_my_account()
    home_page.click_login()

    login_page.set_email(Config.email)
    login_page.set_password(Config.invalid_password)
    login_page.click_login()

    time.sleep(3)

    expect(login_page.get_login_error()).to_be_visible(timeout=3000)

@allure.epic("OpenCart Web Shop")
@allure.feature("Login")
@allure.story("PROJ-101: Invalid user login")
@allure.issue("PROJ-101", "User story: Invalid user login")
@allure.testcase("PROJ-101", "TC005_EmptyEmailAndPasswordClickLoginButton")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC005_EmptyEmailAndPasswordClickLoginButton")
@allure.description("Verify login fails when both Email and Password are empty")
@pytest.mark.regression
def test_empty_email_and_password_login(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    with allure.step("Open the login page"):
        home_page.click_my_account()
        home_page.click_login()

    with allure.step("Leave Email and Password empty and click Login"):
        login_page.set_email("")
        login_page.set_password("")
        login_page.click_login()

    with allure.step("Verify the login error is shown and the user stays on the login page"):
        expect(login_page.get_login_error()).to_be_visible(timeout=5000)
        expect(page).to_have_url(re.compile(r"route=account/login"))



@allure.epic("OpenCart Web Shop")
@allure.feature("Login")
@allure.story("PROJ-101: Forgotten_Password_Link_Present")
@allure.issue("PROJ-101", "User story: Forgotten_Password_Link_Present")
@allure.testcase("PROJ-101", "TC006_Forgotten_Password_Link_Present")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC006_Forgotten_Password_Link_Present")
@allure.description("Verify Forgotten Password Link Present")
@pytest.mark.regression
def test_Forgotten_Password_Link_Present(page):
    home_page = HomePage(page)
    login_page = LoginPage(page)

    with allure.step("Open the login page"):
        home_page.click_my_account()
        home_page.click_login()

    with allure.step("Forgotten Password Link Present"):
        assert login_page.forgot_password_link_present() is True, "Forgotten password link is not visible"













