Feature: Login functionality - Rahul Shetty Academy

  As a registered user
  I want to log in to Rahul Shetty Academy practice site
  So that I can access the application successfully


  Background:
    Given I open the login page

  @smoke @positive @suite2
  Scenario: Successful login with valid credentials
    When I enter username "rahulshettyacademy"
    And I enter password "Learning@830$3mK2"
    And I click on the sign in button
    Then I should be logged in successfully
    And I should see the home page

#  @regression @negative
#  Scenario: Login failure with invalid password
#    When I enter username "rahulshettyacademy"
#    And I enter password "wrongPassword"
#    And I click on the sign in button
#    Then I should see an error message
#
#  @regression @negative
#  Scenario: Login failure with empty credentials
#    When I click on the sign in button
#    Then I should see an error message
