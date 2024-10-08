#! python3
# Dependencies - Requests, BeautifulSoup4

# functions_general.py - Contains functions used across different sections of
# the Vacancy Checker program's overall functionality

from bs4 import BeautifulSoup
import requests

# Pulls a website URL and returns its BS4 soup object
def create_bs4(url):
    try:
        page = requests.get(url)
        page.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Error: %s' % str(err))
        quit()
    soup_object = BeautifulSoup(page.text, 'html.parser')
    
    return soup_object
