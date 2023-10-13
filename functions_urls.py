#! python3
# Dependencies - Requests, BeautifulSoup4

# functions_url.py - Contains functions relating to job vacancy URLs, for
# overall functionality of vacancy_checker.py

import functions_general as fg
import os, json

# Function to update the Civil Service Jobs website URL
def update_url_civil(urls):
    url_civil = input('Please input new URL for Civil Service Jobs vacancies: '
                      '(optional)\n')
    urls['civil_service'] = url_civil
    
    return urls

# Function to update website URL for DWP job vacancies
def update_url_dwp(urls):
    url_dwp = input('Please input new URL for DWP vacancies: (optional)\n')
    # Removes unnecessary URL query data from specified URL
    url_edit = url_dwp.split('&')
    for segment in url_edit:
        if segment.startswith('p=') or segment.startswith('pp='):
            url_edit.remove(segment)
    url_new = '&'.join(url_edit)
    urls['dwp'] = url_new

    return urls

# Function to write updated URLs to JSON file
def write_json_url(urls):
    with open('urls.json', 'w') as file:
        json_urls = json.dumps(urls)
        file.write(json_urls)
        file.close()

# Function to import or generate a JSON file with job vacancy website URLs
def import_urls():
    # If previously run, import contents of existing JSON file containing URLs
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as file:
            urls = json.load(file)
            file.close()
    # If not previously run, generate a JSON file containing specified URLs
    else:
        urls = {'civil_service': '',
                'dwp': ''}
        urls = update_url_civil(urls)
        urls = update_url_dwp(urls)
        write_json_url(urls)

    return urls

# Function to check the Civil Service Jobs URL
def check_url_civil(urls):
    # Initialise BS4 object for Civil Services Jobs vacancy page
    url_civil = urls['civil_service']
    soup_page = fg.create_bs4(url_civil)

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
        update_url_civil(urls)
        print('URL for the Civil Service Jobs website updated\n')
        write_json_url(urls)

    return urls

# Function to check the Civil Service Jobs URL
def check_url_dwp(urls):
    # Initialise BS4 object for DWP vacancy page
    url_dwp = urls['dwp']
    soup_page = fg.create_bs4(url_dwp)

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
        update_url_dwp(urls)
        print('URL for the DWP vacancies website updated\n')
        write_json_url(urls)

    return urls

# Function to check functionality of all job vacancy website URLs
def check_urls(urls: dict):
    for key, value in urls.items():
        if value:
            if key == 'civil_service':
                urls = check_url_civil(urls)
            if key == 'dwp':
                urls = check_url_dwp(urls)
        else:
            if key == 'civil_service':
                urls = update_url_civil(urls)
            if key == 'dwp':
                urls = update_url_dwp(urls)
    if not urls['civil_service'] and not urls['dwp']:
        print('No job vacancy URLs have been provided\n'
              'Please rerun program and provide URLs when prompted')