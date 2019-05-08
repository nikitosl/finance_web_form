from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, Label, TextField, FieldList, FormField, FileField, IntegerField, DateField, SelectField, validators
from wtforms.validators import InputRequired, Email, Length, AnyOf
from app.db import db_worker
import datetime


def not_empty_validator(form, field):
    if not field.data:
        raise ValueError('Поле не заполнено!')


def is_date_validator(form, field):
    if not isinstance(field.data, datetime.date):
        print('Не смог распознать дату.')
        raise ValueError('Не смог распознать дату.')
    return True


def start_date_validator(form, field):
    if is_date_validator(form, field):
        if field.data < datetime.date(year=2018, month=4, day=5):
            raise ValueError('Слишком рано для начальной даты. Есть данные, начиная с 05.04.2018')


def finish_date_validator(form, field):
    if is_date_validator(form, field):
        if field.data < datetime.date(year=2018, month=4, day=5):
            raise ValueError('Слишком поздно для конечной даты. Есть данные до 11.04.2019')





class FinanceForm(Form):
    company_tuple_list = sorted(db_worker.get_companies_list(), key=lambda x: x[1])

    # ________________________________________________________ COMPANIES
    add_company_btn = SubmitField(label='Добавить')
    del_company_btn = SubmitField(label='Удалить')
    company_lst = FieldList(SelectField(label='Название компании:', choices=company_tuple_list, coerce=int))

    # ________________________________________________________ START DATE
    start_date_dt_tx = DateField(label='Начальная дата:', format='%d.%m.%Y',
                                    validators=[start_date_validator], default=datetime.date(2018, 4, 5))
    finish_date_dt_tx = DateField(label='Конечная дата:', format='%d.%m.%Y',
                                    validators=[finish_date_validator], default=datetime.date(2019, 4, 11))
    # _________________________________________________________ CHART TYPE
    chart_type_rbtn = RadioField('Критерий сравнения',
                                choices=[('volume', 'Объем продаж акций'), ('vwap', 'Курс акций')])
    # _________________________________________________________ BUTTONS
    print_btn = SubmitField(label='Нарисовать')
    clear_btn = SubmitField(label='Очистить')

    def data_clear(self):
        while len(self.company_lst.data) > 0:
            self.company_lst.pop_entry()

    def add_company(self):
        self.company_lst.append_entry()

    def remove_company(self):
        if len(self.company_lst.data) > 0:
            self.company_lst.pop_entry()

