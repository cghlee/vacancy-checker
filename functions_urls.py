#! python3
# Dependencies - Requests, BeautifulSoup4

# url_functions.py - Contains functions relating to job vacancy URLs, for
# overall functionality of vacancy_checker.py

from functions_general import create_bs4_object
import os, json, requests, bs4

# Function to update the Civil Service Jobs website URL
def url_civil_updater(urls):
    url_civil = input('Please input new URL for Civil Service Jobs vacancies: '
                      '(optional)\n')
    urls['civil_service'] = url_civil
    return urls

# Function to update the Civil Service Jobs website URL
def url_dwp_updater(urls):
    url_dwp = input('Please input new URL for DWP vacancies: (optional)\n')
    urls['dwp'] = url_dwp
    return urls

# Function to write updated URLs to JSON file
def url_json_writer(urls):
    with open('urls.json', 'w') as file:
        json_urls = json.dumps(urls)
        file.write(json_urls)
        file.close()

# Function to import or generate a JSON file with job vacancy website URLs
def url_importer():
    # If previously run, import contents of existing JSON file containing URLs
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as file:
            urls = json.load(file)
            file.close()
    # If not previously run, generate a JSON file containing specified URLs
    else:
        urls = {'civil_service': '',
                'dwp': ''}
        urls = url_civil_updater(urls)
        urls = url_dwp_updater(urls)
        url_json_writer(urls)
    return urls

# Function to check the Civil Service Jobs URL
def url_civil_checker(urls):
    # Initialise BS4 object for Civil Services Jobs vacancy page
    url_civil = urls['civil_service']
    soup_page = create_bs4_object(url_civil)

    # Test for page content and update if required
    results_element = soup_page.find('div', 'csr-page-title').getText()
    str_results = results_element.split()[0]

    try:
        if ',' in str_results:
            total_results = int(str_results.replace(',', ''))
        else:
            total_results = int(str_results)
        total_results // 25
    except ValueError:
        url_civil_updater(urls)
        print('URL for the Civil Service Jobs website updated')
        url_json_writer(urls)
    return urls

# Function to check the Civil Service Jobs URL
def url_dwp_checker(urls):
    # Initialise BS4 object for DWP vacancy page
    url_dwp = urls['dwp']
    soup_page = create_bs4_object(url_dwp)

    # Test for page content and update if required
    results_element = soup_page.find(class_='govuk-heading-l').getText()
    str_results = results_element.split()[0]

    try:
        if ',' in str_results:
            total_results = int(str_results.replace(',', ''))
        else:
            total_results = int(str_results)
        total_results // 25
    except ValueError:
        url_dwp_updater(urls)
        print('URL for the DWP vacancies website updated')
        url_json_writer(urls)
    return urls

# Function to check functionality of all job vacancy website URLs
def url_checker(urls: dict):
    for key, value in urls.items():
        if value:
            if key == 'civil_service':
                urls = url_civil_checker(urls)
            if key == 'dwp':
                urls = url_dwp_checker(urls)
        else:
            if key == 'civil_service':
                urls = url_civil_updater(urls)
            if key == 'dwp':
                urls = url_dwp_updater(urls)
    if not urls['civil_service'] and not urls['dwp']:
        print('No job vacancy URLs have been provided\nPlease rerun program'
              'and provide URLs when prompted')