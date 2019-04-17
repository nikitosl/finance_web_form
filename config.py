import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

DB_NAME = os.path.join(CURRENT_DIR, 'app', 'db', 'finance.db')

