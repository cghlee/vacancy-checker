#! python3
# Dependencies - Requests, BeautifulSoup4

# vacancy_checker.py - Checks existing vacancies, updates and compares against
# new vacancies, then provides option to open new vacancies within a browser

from functions_vacancies import update_civil_service
from functions_urls import url_importer, url_checker
import os, json, webbrowser

# Import or generate job vacancy URLs via url_importer function
urls = url_importer()

# Check job vacancy URLs are functioning correctly
url_checker(urls)

# If previously run, import contents of existing JSON file containing vacancies
if os.path.exists('vacancies.json'):
    with open('vacancies.json', 'r') as file:
        old_vacancies = json.load(file)
        file.close()
# If not previously run, generate a JSON file containing current vacancies
else:
    print('JSON file of job vacancies not found')
    print('Generating new JSON file containing current job vacancies')
    update_civil_service(urls)
    print('Generated new JSON file\nPlease run again for updates to vacancies')
    quit()

# Update vacancies and create dictionary to store updated vacancy information
update_civil_service(urls)
with open('vacancies.json', 'r') as file:
    updated_vacancies = json.load(file)
    file.close()

# Identify and store new vacancies within a list
new_vacancies = []
for key in updated_vacancies:
    if key not in old_vacancies:
        new_vacancies.append(key)

# Feedback and break out of file if no new vacancies have been identified
if not new_vacancies:
    print('There have been no new vacancies since last time')
    quit()

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
    for url in new_urls:
        webbrowser.open(url)