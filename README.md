# Vacancy Checker

An automated solution to filter through new job vacancies relevant to me,
without having to reparse all 50+ vacancies daily while trying to remember
those I had or had not seen. Originally designed for the UK Government's
Civil Service Jobs website.

## Dependencies

Vacancy Checker requires the `Requests` and `BeautifulSoup4` modules, with
relevant documentation linked below:

- [Requests](https://pypi.org/project/requests/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## How to Use

Run `vacancy_checker.py`, which will operate according to functions defined
within `functions_urls.py`, `functions_vacancies.py`, and
`functions_general.py`.

If locally-stored `<website>_vacancies.json` or `urls.json` files do not exist,
these will be automatically generated using current vacancy listings, or user-
defined job vacancy website URLs, respectively.

If `<website>_vacancies.json` *does* exist locally, job vacancies will be
updated and then compared against those active during the last time the Vacancy
Checker was run. New vacancies, if present, will be listed alongside a prompt
for them to opened in separate tabs within your default browser.

If a job vacancy website URL is missing, or identified as invalid or expired,
you will be prompted to update the URL.