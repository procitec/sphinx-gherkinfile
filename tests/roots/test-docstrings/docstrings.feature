Feature: Doc strings are rendered

  Scenario: Doc string without media type
    Given a doc string without media type
      """
      plain doc string content
      """

  Scenario: Doc string with media type
    Given a doc string with media type
      """text/plain
      typed doc string content
      """
