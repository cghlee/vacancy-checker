# vacancy-checker

An automated solution to filter through new job vacancies relevant to me,
without having to reparse all 50+ vacancies daily while trying to remember
those I had or had not seen. Originally designed for the UK Government's
Civil Service Jobs website.

## Dependencies

This Vacancy Checker requires the `Requests` and `BeautifulSoup4` modules to
function, with relevant documentation linked below:

[Requests module](https://pypi.org/project/requests/)
[BeautifulSoup4 module](https://pypi.org/project/beautifulsoup4/)

## How it works

Run `vacancy_checker.py`, which will call the `update_civil_service` function
within `updater.py`.

If a locally-stored `vacancies.json` file doesn't exist, it will be
automatically generated using current job listings.

If `vacancies.json` *does* exist locally, job vacancies will be updated and
compared against those active at the last time the Vacancy Checker was run.
New vacancies, if present, will be listed alongside a prompt for them to all
be opened within your default browser.