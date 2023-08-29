#! python3
# Dependencies - Requests, BeautifulSoup4

# updater.py - Contains functions to check and update job vacancies, and
# stores vacancies in a JSON file for use within vacancy_checker.py

import requests, bs4, json

def update_civil_service():
    # Pulls a Civil Service jobs URL and converts into a BS4 object
    URL_CIVIL_SERVICE = 'https://www.civilservicejobs.service.gov.uk/csr/'\
                        'index.cgi?SID=cGFnZWFjdGlvbj1zZWFyY2hjb250ZXh0Jn'\
                        'BhZ2VjbGFzcz1TZWFyY2gmcGFnZT0xJm93bmVyPTUwNzAwMD'\
                        'Amb3duZXJ0eXBlPWZhaXImY29udGV4dGlkPTQ3ODYzMTIyJn'\
                        'JlcXNpZz0xNjkzMzAyMjYzLWQ3N2FkMjU5Zjc0YTBiN2Q5MT'\
                        'g1NDBiZjBkMzliMTM4MzM4OGFjNjM%3D&sort=sallow&req'\
                        'sig=1693302263-d77ad259f74a0b7d918540bf0d39b1383388ac63'
    try:
        initial_page = requests.get(URL_CIVIL_SERVICE)
        initial_page.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print('Error: %s' % str(err))
        quit()

    initial_soup = bs4.BeautifulSoup(initial_page.text, 'html.parser')
    print('Updating Civil Service job vacancies')

    # Assign variable with total results
    results_element = initial_soup.find('div', 'csr-page-title').getText()
    total_results = results_element.split()[0]
    # Calculate expected number of pages of results (25 per page)
    # If URL is invalid, raised ValueError will terminate the program
    try:
        expected_pages = int(total_results) // 25
    except ValueError:
        print('Invalid or expired URL\nPlease update the URL')
        quit()

    # Grab HTML elements for the paging menu
    paging_element = initial_soup.select('div[class="search-results-paging-menu"]')
    page_elements = paging_element[0].find_all('a')

    # Add results pages into a list for processing of individual vacancies
    pages = []
    pages.append(URL_CIVIL_SERVICE)
    for i in range(expected_pages):
        pages.append(page_elements[i].get('href'))

    # Set up counters and initialise dictionary to store current job vacancies
    vacancies = {}
    page_number = 1
    vacancy_number = 1

    # Find all job vacancies on each page
    for page in pages:
        print('Processing page %s of %s' % (page_number, expected_pages + 1))
        try:
            response_page = requests.get(page)
            response_page.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print('Error: %s' % str(err))
            quit()
        response_soup = bs4.BeautifulSoup(response_page.text, 'html.parser')
        page_results = response_soup.find_all('li', 'search-results-job-box')
        # Create nested dictionaries containing details about each job vacancy
        for result in page_results:
            print('Processing vacancy %s of %s' % (vacancy_number, total_results))
            vacancy = {}
            vacancy['title'] = result.find('a').getText()
            vacancy['dept'] = result.find('div', 'search-results-job-box-department').getText()
            vacancy['url'] = result.find('a').get('href')
            ref_raw = result.find('div', 'search-results-job-box-refcode').getText()
            ref = ref_raw.split()[-1]
            vacancies[ref] = vacancy
            vacancy_number += 1
        page_number += 1
    print('Processing complete')

    # Write all vacancy information to a local JSON file
    print('Writing job vacancies to vacancies.json')
    with open('vacancies.json', 'w') as file:
        file.write(json.dumps(vacancies))
        file.close()
    print('Writing complete')