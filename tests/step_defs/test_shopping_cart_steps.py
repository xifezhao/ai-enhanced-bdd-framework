from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Scenarios
scenarios('../features/shopping_cart.feature')

# Given Steps
@given('a registered user is logged in')
def logged_in_user(browser):
    browser.get("http://127.0.0.1:5000/login")
    browser.find_element(By.ID, "username").send_keys("testuser")
    browser.find_element(By.ID, "password").send_keys("password123")
    browser.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
    WebDriverWait(browser, 5).until(EC.url_contains('/products'))

@given(parsers.parse('a product "{product_name}" is available'))
def product_is_available(browser, product_name):
    # In this PoC, we assume the product is always available if the page loads.
    assert product_name in browser.page_source

# When Steps
@when(parsers.parse('the user adds the "{product_name}" to the shopping cart'))
def add_item_to_cart(browser, product_name):
    # Find the button next to the product name
    product_list_items = browser.find_elements(By.TAG_NAME, 'li')
    for item in product_list_items:
        if product_name in item.text:
            item.find_element(By.TAG_NAME, 'button').click()
            break
    # Add a small wait for the async operation
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element((By.ID, 'cart-items'), product_name)
    )

# Then Steps
@then(parsers.parse('the shopping cart should contain {quantity:d} item of "{product_name}"'))
def check_cart_contents(browser, quantity, product_name):
    cart_items_element = browser.find_element(By.ID, 'cart-items')
    expected_text = f"{product_name} x {quantity}"
    assert expected_text in cart_items_element.text