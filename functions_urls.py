#! python3
# Dependencies - Requests, BeautifulSoup4

# url_functions.py - Contains functions relating to job vacancy URLs, for
# overall functionality of vacancy_checker.py

import os, json, requests, bs4

# Function to write updated URLs to JSON file
def url_json_writer(urls):
    with open('urls.json', 'w') as file:
        json_urls = json.dumps(urls)
        file.write(json_urls)
        file.close()

# Function to update the Civil Service Jobs website URL
def url_civil_updater(urls):
    url_civil = input('Please input new URL for Civil Service Jobs vacancies:\n')
    urls['civil_service'] = url_civil
    return urls

# Function to check the Civil Service Jobs URL
def url_civil_checker(urls):
    # Initialise Requests module Response object and test for status code
    try:
        url_civil = urls['civil_service']
        civil_page = requests.get(url_civil)
        civil_page.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Error: %s' % str(err))
        quit()

    # Initialise bs4 object
    soup_page = bs4.BeautifulSoup(civil_page.text, 'html.parser')

    # Test for page content and update if required
    results_element = soup_page.find('div', 'csr-page-title').getText()
    total_results = results_element.split()[0]
    try:
        int(total_results) // 25
    except ValueError:
        url_civil_updater(urls)
        print('Civil Service Jobs URL updated')
        url_json_writer(urls)
    return urls

# Function to import or generate a JSON file with job vacancy website URLs
def url_importer():
    # If previously run, import contents of existing JSON file containing URLs
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as file:
            urls = json.load(file)
            file.close()
    # If not previously run, generate a JSON file containing specified URLs
    else:
        urls = {}
        urls = url_civil_updater(urls)
        url_json_writer(urls)
    return urls

# Function to check functionality of all job vacancy website URLs
def url_checker(urls: dict):
    for key, value in urls.items():
        if value:
            if key == 'civil_service':
                urls = url_civil_checker(urls)