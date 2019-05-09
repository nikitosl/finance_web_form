import os
import datetime

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

DB_NAME = os.path.join(CURRENT_DIR, 'app', 'db', 'finance.db')

# Путь к директории info
info_dir = os.path.join(CURRENT_DIR, 'app', 'db', 'tech_companies', 'info')

# Путь к файлу tech_companies.json
tech_companies_list_json = os.path.join(CURRENT_DIR, 'app', 'db', 'tech_companies', 'tech_companies.json')

# URLы апишки
base_url = 'https://api.iextrading.com/1.0'
company_url = '/stock/{company_name}/company'
companies_url = '/ref-data/symbols'
company_info_per_year = '/stock/{company_name}/chart/1y'

# Начальная и конечные даты для графиков
start_date = datetime.date(2018, 5, 9)
finish_date = datetime.date(2019, 5, 8)