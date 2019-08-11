import sqlite3
import pandas as pd
import datetime
from random import randrange
import matplotlib.pyplot as plt
import io
import base64
import config
import os

DB_NAME = config.DB_NAME
# DB_NAME = config.DB_NAME

# region Run SQL
# Выполнение SQL, без возврата значения, с сохранением
def __exec_sql(sql):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(sql)

    except Exception as e:
        print(f'Error during "exec_sql": {e}\n{sql}')
    else:
        conn.commit()
        conn.close()


# Выполнение SQL и получение результата
def __get_data(sql):

    try:
        conn = sqlite3.connect(DB_NAME)
        ca = pd.read_sql(sql, conn)
    except Exception as e:
        print(f'Error during "get_data": {e}\n{sql}')
    else:
        conn.close()
        return ca
    return None


# Вставка в таблицу table датафрейма df
def __insert_df(df: pd.DataFrame, table):
    try:
        conn = sqlite3.connect(DB_NAME)
        df.to_sql(name=table, con=conn, if_exists='append', index=False)
    except Exception as e:
        print(f'Error during "insert_df": {e}')
    else:
        conn.commit()
        conn.close()
# endregion


# region Creates
# Создание таблицы Компании
def create_table_company():
    data = '''
        CREATE TABLE IF NOT EXISTS company (
            id integer PRIMARY KEY,
            symbol text NOT NULL,
            name text NOT NULL,
            creation_date text
        );
    '''
    __exec_sql(data)


# Создание таблицы Информация (для хранения истории объёмов продаж акций и курс акций за разные дни)
def create_table_info():
    data = '''
        CREATE TABLE IF NOT EXISTS info (
            company_id integer,
            date text NOT NULL,
            volume integer NOT NULL,
            vwap float NOT NULL,
            FOREIGN KEY (company_id) REFERENCES company (id)
        );
    '''
    __exec_sql(data)
# endregion


# region Inserts
# Вставка строки в таблицу Компании
def insert_company(company):
    data = f'''
        INSERT INTO company(id, name, symbol, creation_date)
        VALUES ({int(company['iexId'])}, '{company['name']}', '{company['symbol']}', '{generate_random_date()}');
    '''
    __exec_sql(data)


# Вставка датафрейма в Информация
def insert_info(df):
    __insert_df(df, 'info')


# Вставка тестовой компании
def insert_handmade_company():
    company = {
        'iexId': '11',
        'name': 'Apple Inc.',
        'date': generate_random_date(),
        'symbol': 'AAPL'
    }
    insert_company(company)

    company = {
        'iexId': '4563',
        'name': 'Microsoft Corporation',
        'date': generate_random_date(),
        'symbol': 'MSFT'
    }
    insert_company(company)

# endregion


# region Selects
# Получение графика по данным запроса
def get_chart_by_dataframe(df):
    # plt.close('all')
    df.groupby(['date', 'company_name'])['inf_field'].sum().unstack().plot(figsize=(10, 6))
    plt.title(f'График изменения {"курса акций" if type == "vwap" else "объема продаж акций"} компаний по времени')
    plt.xlabel('Дата')
    plt.ylabel('Курс акций ($)' if type == "vwap" else 'Объем продаж акций ($)')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


# Получение информации по определённой компании
def get_company_info(company_id_list, date_from=config.start_date, date_to=config.finish_date, type='vwap'):
    company_id_list = ', '.join([str(i) for i in company_id_list])

    data = f'''
        SELECT 
            c.id company_id,
            c.name company_name,
            i.date date,
            i.{type} inf_field
        FROM company c
            JOIN info i
                ON i.company_id = c.id
        WHERE i.date BETWEEN "{date_from}" AND "{date_to}"  
            AND c.id IN ({company_id_list})             
    '''
    return __get_data(data)


# Получение списка кортежей (id компании, название компании)
def get_companies_list():
    data = f'''
                SELECT 
                    c.id id,
                    c.name name
                FROM company c        
            '''
    ca = __get_data(data)
    lst = []
    for row in ca.iterrows():
        lst.append((row[1]['id'], row[1]['name']))

    return lst


# Получение всех значений из таблицы Компании
def get_all_companies():
    data = f'''
            SELECT *
            FROM company        
        '''
    return __get_data(data)


# Получение всех данных по таблице Информация
def get_all_info():
    data = f'''
            SELECT *
            FROM info        
            '''
    return __get_data(data)
# endregion


# region Removes / Drops
# Генерация рандомной даты для поля Дата Создания Компании
def generate_random_date():
    year = randrange(1920, 2000)
    month = randrange(1, 12)
    day = randrange(1, 28)
    date = datetime.date(year=year, month=month, day=day)
    return str(date)


# Удаление данных из таблицы Company
def __company_data_clear(company=None):
    if not company:
        data = '''
            DELETE FROM company   
        '''
    else:
        data = f'''
                    DELETE FROM company
                    WHERE company.id = {company} 
                '''
    __exec_sql(data)


# Удаление данных из таблицы info
def __info_data_clear(company=None):
    if not company:
        data = '''
            DELETE FROM info
        '''
    else:
        data = f'''
            DELETE FROM info
            WHERE info.company_id = {company['iexId']} 
        '''
    __exec_sql(data)


# Удаление таблицы Company
def __remove_company_table():
    data = '''
        DROP TABLE IF EXISTS company
    '''
    __exec_sql(data)


# Удаление таблицы Info
def __remove_info_table():
    data = '''
        DROP TABLE IF EXISTS info
    '''
    __exec_sql(data)


# Получение списка компаний, не имеющих запись в info
def get_companies_without_info():
    cdata = '''
        SELECT id company
        FROM company
    '''
    cdf = __get_data(cdata)
    ids_from_company = set(cdf['company'].to_list())

    idata = '''
        SELECT company_id info
        FROM info
    '''
    idf = __get_data(idata)
    ids_from_info = set(idf['info'].to_list())

    return list(ids_from_company - ids_from_info)
# endregion


if __name__ == '__main__':

    # print(get_company_info([692]))
    # print(get_all_info())
    pass

