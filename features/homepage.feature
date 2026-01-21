Feature: Rahul Shetty Academy Homepage

  @smoke @positive @suite1
  Scenario: Verify homepage title
    Given I open Rahul Shetty Academy homepage
    Then page title should contain "Rahul Shetty Academy"
