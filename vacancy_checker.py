#! python3
# Dependencies - Requests, BeautifulSoup4

# vacancy_checker.py - Checks existing vacancies, updates and compares against
# new vacancies, then provides option to open new vacancies within a browser

import functions_vacancies as fv
import functions_urls as fu
import os, json

# Import or generate job vacancy URLs via url_importer function
urls = fu.import_urls()

# Check job vacancy URLs are functioning correctly
fu.check_urls(urls)

if urls['civil_service']:
    # If previously run, import contents of existing JSON file containing vacancies
    if os.path.exists('vacancies_civil.json'):
        with open('vacancies_civil.json', 'r') as file:
            old_civil = json.load(file)
            file.close()
        created_json_civil = False
    # If not previously run, generate a JSON file containing current vacancies
    else:
        print('\nJSON file of job vacancies not found')
        print('Generating new JSON file containing current job vacancies')
        fv.update_vacancies_civil(urls)
        print('Generated new JSON file\nPlease run again for updates to vacancies\n')
        created_json_civil = True

    if not created_json_civil:
        # Update vacancies and create dictionary to store updated vacancy information
        fv.update_vacancies_civil(urls)
        with open('vacancies_civil.json', 'r') as file:
            updated_civil = json.load(file)
            file.close()

        # Print information about and prompt to open new vacancies in a web browser
        fv.print_new_vacancies(updated_civil, old_civil)

if urls['dwp']:
    if os.path.exists('vacancies_dwp.json'):
        with open('vacancies_dwp.json', 'r') as file:
            old_dwp = json.load(file)
            file.close()
        created_json_dwp = False
    # If not previously run, generate a JSON file containing current vacancies
    else:
        print('\nJSON file of job vacancies not found')
        print('Generating new JSON file containing current job vacancies')
        fv.update_vacancies_dwp(urls)
        print('Generated new JSON file\nPlease run again for updates to vacancies\n')
        created_json_dwp = True

    if not created_json_dwp:
        # Update vacancies and create dictionary to store updated vacancy information
        fv.update_vacancies_dwp(urls)
        with open('vacancies_dwp.json', 'r') as file:
            updated_dwp = json.load(file)
            file.close()

        # Print information about and prompt to open new vacancies in a web browser
        fv.print_new_vacancies(updated_dwp, old_dwp)