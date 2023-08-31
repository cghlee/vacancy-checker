# Vacancy Checker

An automated solution to filter through new job vacancies relevant to me,
without having to reparse all 50+ vacancies daily while trying to remember
those I had or had not seen. Originally designed for the UK Government's
Civil Service Jobs website.

## Dependencies

Vacancy Checker requires the `Requests` and `BeautifulSoup4` modules, with
relevant documentation linked below:

- [Requests module](https://pypi.org/project/requests/)
- [BeautifulSoup4 module](https://pypi.org/project/beautifulsoup4/)

## How to Use

Run `vacancy_checker.py`, which will call the `update_civil_service` function
within `updater.py`.

If locally-stored `vacancies.json` or `urls.json` files do not exist, they
will be automatically generated using current vacancy listings, or user-
defined job vacancy website URLs, respectively.

If `vacancies.json` *does* exist locally, job vacancies will be updated and
compared against those active at the last time the Vacancy Checker was run.
New vacancies, if present, will be listed alongside a prompt for them to all
be opened within your default browser.

If a job vacancy website URL is identified as invalid or expired, you will be
prompted to update the URL; after which you must rerun `vacancy_checker.py`.