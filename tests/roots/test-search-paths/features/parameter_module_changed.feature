@requirements
Feature: Parameter module changed
  The documentation includes a feature file that already exists on disk.

  Background: Parameter state exists
    Given a module parameter file

  Rule: Known modules are tracked

    @wip
    Scenario: Changing a known parameter
      Given a module parameter file
        | module_name | state |
        | RX          | old   |
      When the parameter is changed
      Then the change is visible in documentation
