@requirements
Feature: File with repeated steps using wildcard notation

  The file includes repeated steps with wildcard notation for better visualisation

Background: Parameter state exists
  Given a first precondition
  * a second precondition
  * a third precondition

Scenario: Changing a known parameter
  When the user does login to the system
  * starts a chat
  * enters "hello world" in the chat

  Then the system repeats the text in the chat
  * the systems adds a new prompt
