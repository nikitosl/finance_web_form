from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, Label, TextField, FieldList, FormField, FileField, IntegerField, DateField, SelectField, validators
from wtforms.validators import InputRequired, Email, Length, AnyOf
from app.db import db_worker
import datetime
import config


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
        if field.data < config.start_date:
            raise ValueError(f'Слишком рано для начальной даты. Есть данные, начиная с {config.start_date}')


def finish_date_validator(form, field):
    if is_date_validator(form, field):
        if field.data > config.finish_date:
            raise ValueError(f'Слишком поздно для конечной даты. Есть данные до {config.finish_date}')





class FinanceForm(Form):
    company_tuple_list = sorted(db_worker.get_companies_list(), key=lambda x: x[1])

    # ________________________________________________________ COMPANIES
    add_company_btn = SubmitField(label='Добавить')
    del_company_btn = SubmitField(label='Удалить')
    company_lst = FieldList(SelectField(label='Название компании:', choices=company_tuple_list, coerce=int))

    # ________________________________________________________ START DATE
    start_date_dt_tx = DateField(label='Начальная дата:', format='%d.%m.%Y',
                                    validators=[start_date_validator], default=config.start_date)
    finish_date_dt_tx = DateField(label='Конечная дата:', format='%d.%m.%Y',
                                    validators=[finish_date_validator], default=config.finish_date)
    # _________________________________________________________ CHART TYPE
    chart_type_rbtn = RadioField('Критерий сравнения',
                                 choices=[('volume', 'Объем продаж акций'), ('vwap', 'Курс акций')],
                                 default='vwap')
    # _________________________________________________________ BUTTONS
    print_btn = SubmitField(label='Нарисовать')
    show_data_btn = SubmitField(label='Посмотреть')
    load_data_btn = SubmitField(label='Скачать')
    clear_btn = SubmitField(label='Очистить')

    def data_clear(self):
        while len(self.company_lst.data) > 0:
            self.company_lst.pop_entry()

    def add_company(self):
        self.company_lst.append_entry()

    def remove_company(self):
        if len(self.company_lst.data) > 0:
            self.company_lst.pop_entry()

