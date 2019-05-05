from app import app
import flask
from flask import request, render_template, flash, redirect, url_for
from app.forms import *
import json
import datetime
from datetime import datetime
from app.db import db_worker
import os


def generate_plot(form):
    comps = form.company_lst.data
    if None in comps:
        return 0
    start_date = str(form.start_date_dt_tx.data)
    finish_date = str(form.finish_date_dt_tx.data)
    return db_worker.get_chart_of_company_volume(comps, start_date, finish_date)


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

    return render_template(
        'form.html',
        # 'form_without_date.html',
        form=form
    )


