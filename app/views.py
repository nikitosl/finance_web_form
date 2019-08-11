from app import app
import flask
from flask import request, render_template, flash, redirect, url_for, send_file
from app.forms import *
import json
import datetime
from datetime import datetime
from app.db import db_worker


# Получение DataFrame по данным формы
def get_dataframe_by_form(form):
    comps = form.company_lst.data
    if None in comps:
        return 0
    start_date = str(form.start_date_dt_tx.data)
    finish_date = str(form.finish_date_dt_tx.data)
    chart_type = form.chart_type_rbtn.data
    return db_worker.get_company_info(comps, start_date, finish_date, chart_type)


# Подготовка данных для вывода
def df_preparation_for_html(df):
    df = df.rename(columns={'date': 'Дата'})\
        .pivot(index='Дата', columns='company_name', values='inf_field')\
        .reset_index()
    return df

# Построение графика по данным формы
def generate_plot(form):
    df = get_dataframe_by_form(form)
    return db_worker.get_chart_by_dataframe(df)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FinanceForm()
    if request.method == 'POST':                        # Кнопки
        if form.add_company_btn.data:   # Добавление компании
            form.add_company()

        elif form.del_company_btn.data: # Удаление компании
            form.remove_company()

        elif form.clear_btn.data:   # Очистка списка компаний
            form.data_clear()

        if form.print_btn.data and form.validate_on_submit():  # Отрисовка графика
            if len(form.company_lst.data) == 0:
                flash('Необходимо добавить хотябы одну компанию')
            else:
                file_url = generate_plot(form)
                return render_template(
                    'graph.html',
                    chart_filename=file_url
                )

        if form.show_data_btn.data and form.validate_on_submit():  # Скачивание данных
            if len(form.company_lst.data) == 0:
                flash('Необходимо добавить хотябы одну компанию')
            else:
                df = get_dataframe_by_form(form)

                # Обработка df для красивого вывода
                df = df_preparation_for_html(df)
                df.columns = [col[:18] + '..' * (len(col) > 20) for col in df.columns]
                title = 'Курс акций компаний по времени ($)' if form.chart_type_rbtn.data == 'vwap' \
                    else 'Объем продаж акций компаний по времени ($)'

                return render_template(
                    'load_data.html',
                    table=df.to_html(index_names=False, index=False,
                                     border=2, justify='center',
                                     col_space=100,  max_cols=7, max_rows=30),
                    title=title
                )

        if form.load_data_btn.data and form.validate_on_submit():  # Скачивание данных
            if len(form.company_lst.data) == 0:
                flash('Необходимо добавить хотябы одну компанию')
            else:
                df = get_dataframe_by_form(form)

                # Обработка df для красивого вывода
                df = df_preparation_for_html(df)
                filename = '/Users/nikita/PycharmProjects/finance_web_form/app/static/company_info.xlsx'
                df.to_excel(filename, index=False)
                try:
                    return send_file(filename, as_attachment=True, attachment_filename='company_info.xlsx')
                except Exception as e:
                    return e

    return render_template(
        'form.html',
        form=form
    )

