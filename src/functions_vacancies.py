#! python3
# Dependencies - Requests, BeautifulSoup4

# functions_vacancies.py - Contains functions to check and update job vacancies,
# and stores vacancies in a JSON file for use within vacancy_checker.py

from . import functions_general as fg
import json, webbrowser, time

# Updates Civil Service Jobs vacancy listings
def update_vacancies_civil(urls: dict):
    # Pulls Civil Service Jobs URL from "urls.json" and creates BS4 object
    url_civil = urls['civil_service']
    soup_object = fg.create_bs4(url_civil)
    print('Updating Civil Service job vacancies...')

    # Assign variable with total results
    results_element = soup_object.find('div', 'csr-page-title').getText()
    total_results = int(results_element.split()[0])

    # Calculate expected number of pages for all job vacancies
    if total_results % 25 == 0:
        expected_pages = total_results // 25
    else:
        expected_pages = ((total_results) // 25) + 1

    # Grab HTML elements for the paging menu
    paging_element = soup_object.select('div[class="search-results-paging-menu"]')
    page_elements = paging_element[0].find_all('a')

    # Add results pages into a list for processing of individual vacancies
    pages = []
    pages.append(url_civil)
    for i in range(expected_pages - 1):
        pages.append(page_elements[i].get('href'))

    # Set up counters and initialise dictionary to store current job vacancies
    vacancies = {}
    page_number = 1
    vacancy_number = 1

    # Find all job vacancies on each page
    for page in pages:
        print('Processing page %s of %s...' % (page_number, expected_pages))
        response_soup = fg.create_bs4(page)
        page_results = response_soup.find_all('li', 'search-results-job-box')
        # Create nested dictionaries containing details about each job vacancy
        for result in page_results:
            print('Processing vacancy %s of %s...' % (vacancy_number, total_results))
            vacancy = {}
            vacancy['title'] = result.find('a').getText()
            vacancy['dept'] = result.find('div', 'search-results-job-box-department').getText()
            vacancy['url'] = result.find('a').get('href')
            ref_raw = result.find('div', 'search-results-job-box-refcode').getText()
            ref = ref_raw.split()[-1]
            vacancies[ref] = vacancy
            vacancy_number += 1
        page_number += 1
    print('Completed processing of Civil Service vacancies')

    # Write all vacancy information to a local JSON file
    print('\nWriting job vacancies to "vacancies_civil.json"...')
    with open('vacancies_civil.json', 'w') as file:
        file.write(json.dumps(vacancies))
        file.close()
    print('Writing complete')

# Updates DWP vacancy listings
def update_vacancies_dwp(urls: dict):
    # Pulls DWP URL from "urls.json" and creates BS4 object
    url_dwp = urls['dwp']
    soup_object = fg.create_bs4(url_dwp)
    print('\nUpdating DWP job vacancies...')

    # Assign variable with total results
    results_element = soup_object.find(class_='govuk-heading-l').getText()
    str_results = results_element.split()[0]
    if ',' in str_results:
        total_results = int(str_results.replace(',', ''))
    else:
        total_results = int(str_results)

    # Calculate expected number of pages for all job vacancies
    if total_results % 50 == 0:
        expected_pages = total_results // 50
    else:
        expected_pages = ((total_results) // 50) + 1

    # Add results pages into a list for processing of individual vacancies
    pages = []
    for i in range(expected_pages):
        pages = []
        for i in range(expected_pages):
            page_url = url_dwp + f"&pp=50&p={i+1}"
            pages.append(page_url)

    # Set up counters and initialise dictionary to store current job vacancies
    vacancies = {}
    page_number = 1
    vacancy_number = 1

    # Find all job vacancies on each page
    for page in pages:
        print('Processing page %s of %s...' % (page_number, expected_pages))
        response_soup = fg.create_bs4(page)
        page_results = response_soup.find_all('div', class_='search-result')
        # Create nested dictionaries containing details about each job vacancy
        for result in page_results:
            print('Processing vacancy %s of %s...' % (vacancy_number, total_results))
            vacancy = {}
            vacancy['title'] = str(result.find('a', class_='govuk-link').getText()).strip()
            list_data = result.find_all('li')
            vacancy['dept'] = str(list_data[1].getText().strip())
            vacancy['url'] = result.find('a', class_='govuk-link').get('href')
            ref = result.get('data-aid')
            vacancies[ref] = vacancy
            vacancy_number += 1
        page_number += 1
    print('Completed processing of DWP vacancies')

    # Write all vacancy information to a local JSON file
    print('\nWriting job vacancies to "vacancies_dwp.json"...')
    with open('vacancies_dwp.json', 'w') as file:
        file.write(json.dumps(vacancies))
        file.close()
    print('Completed writing of DWP vacancies to JSON file')

# Prints information about and prompts to open new vacancies in a web browser
def print_new_vacancies(updated_vacancies: dict, old_vacancies: dict):
    # Identify and store new vacancies within a list
    print('\nChecking for new vacancies...')
    new_vacancies = []
    for key in updated_vacancies:
        if key not in old_vacancies:
            new_vacancies.append(key)

    # Feedback and break out of file if no new vacancies have been identified
    if not new_vacancies:
        print('There have been no new vacancies since last time')
    else:
        # Print data and store URLs relating to new vacancies
        new_urls = []
        print('New vacancies found:')
        for vacancy in new_vacancies:
            print(' - %s, at %s' % (updated_vacancies[vacancy]['title'],\
                                    updated_vacancies[vacancy]['dept']))
            new_urls.append(updated_vacancies[vacancy]['url'])

        # Open new vacancies in browser if desired
        is_to_open = input('Open new vacancies in browser? (y/n)\n').lower()
        if is_to_open == 'y':
            counter_open = 0
            for url in new_urls:
                webbrowser.open(url)
                counter_open += 1
                # Pause for one second for every ten vacancy URLs opened
                if counter_open % 10 == 0:
                    time.sleep(1)
