# Bank Project

Basic practice project for:

- UI automation with Selenium and Pytest
- API testing with Requests and Pytest
- DB validation with SQLite
- POM structure for UI tests

This scaffold intentionally includes only:

- project folders
- empty placeholder packages
- HTML template placeholders
- SQLite schema and seed data

You will implement the application code, page objects, and tests on top of it.


In order to run all or part of them, rum from terminal inside bank_project:

for all - pytest -v
for ui only - pytest -m ui
for API only - pytest -m api
for DB only - pytest -m db
for integration - pytest -m integration
for api+db - pytest -m "api or db"
