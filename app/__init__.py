from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)

Bootstrap(app)
app.config.from_object('config')

from app import views

