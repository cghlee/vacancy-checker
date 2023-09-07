#! python3
# Dependencies - Requests, BeautifulSoup4

# functions_general.py - Contains functions used across different sections of
# the Vacancy Checker program's overall functionality

import requests, bs4

# Pulls a website URL and returns its BS4 soup object
def create_bs4_object(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Error: %s' % str(err))
        quit()
    soup_object = bs4.BeautifulSoup(page.text, 'html.parser')
    return soup_object