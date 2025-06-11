from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Scenarios
scenarios('../features/login.feature')

# Fixtures are in conftest.py

# Given Steps
@given('the user is on the login page')
def go_to_login_page(browser):
    browser.get("http://127.0.0.1:5000/login")
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "username")))

# When Steps
@when('the user enters valid credentials')
def enter_valid_credentials(browser):
    browser.find_element(By.ID, "username").send_keys("testuser")
    browser.find_element(By.ID, "password").send_keys("password123")

@when(parsers.parse('the user enters a valid username and an invalid password'))
def enter_invalid_password(browser):
    browser.find_element(By.ID, "username").send_keys("testuser")
    browser.find_element(By.ID, "password").send_keys("wrongpassword")

@when('clicks the login button')
def click_login(browser):
    browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

# Then Steps
@then('the user should be redirected to the products page')
def check_products_page_redirect(browser):
    WebDriverWait(browser, 5).until(EC.url_contains('/products'))
    assert '/products' in browser.current_url

@then('a welcome message should be visible')
def check_welcome_message(browser):
    # For this simple app, being on the product page implies a successful login
    assert "Products" in browser.page_source

@then(parsers.parse('an "{error_message}" error message should be displayed'))
def check_error_message(browser, error_message):
    error_element = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "error"))
    )
    assert error_message in error_element.text