Feature: Shopping Cart
  As a registered user, I want to manage my shopping cart.

  Scenario: Add an item to the cart
    Given a registered user is logged in
    When the user adds a "Laptop" to the shopping cart
    Then the shopping cart should contain 1 item of "Laptop"