Feature: User Login
  As a user, I want to log in to the application to access my account.

  Scenario: Successful Login
    Given the user is on the login page
    When the user enters valid credentials
    And clicks the login button
    Then the user should be redirected to the products page
    And a welcome message should be visible

  Scenario: Failed Login with wrong password
    Given the user is on the login page
    When the user enters a valid username and an invalid password
    And clicks the login button
    Then an "Invalid credentials" error message should be displayed