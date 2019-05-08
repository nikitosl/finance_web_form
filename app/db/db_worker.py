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

    if os.path.exists(DB_NAME):
        print('file exist!')

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


# Создание таблицы Объёмы (для хранения истории объёмов продаж акций за разные дни)
def create_table_volume():
    data = '''
        CREATE TABLE IF NOT EXISTS volume (
            company_id integer,
            date text NOT NULL,
            volume integer NOT NULL,
            vwap float NOT NULL,
            FOREIGN KEY (company_id) REFERENCES company (id)
        );
    '''
    __exec_sql(data)


# Вставка строки в таблицу Компании
def insert_company(company):
    data = f'''
        INSERT INTO company(id, name, symbol, creation_date)
        VALUES ({int(company['iexId'])}, '{company['name']}', '{company['symbol']}', '{generate_random_date()}');
    '''
    __exec_sql(data)


# Вставка строки в таблицу Объёмы
def insert_volume(company, volume):
    data = f'''
            INSERT INTO volume(name, symbol, creation_date)
            VALUES ({int(company['iexId'])}, '{volume['date']}', {volume['volume']});
        '''
    __exec_sql(data)


# Вставка датафрейма с объёмами
def insert_volumes(df):
    __insert_df(df, 'volume')


# Получение всех объёмов по определённой компании
def get_chart_of_company_volume(company_id_list, date_from, date_to, type='vwap'):
    company_id_list = ', '.join([str(i) for i in company_id_list])

    if type == 'vwap':
        data = f'''
            SELECT 
                c.id company_id,
                c.name company_name,
                v.date date,
                v.vwap volume
            FROM company c
                JOIN volume v
                    ON v.company_id = c.id
            WHERE v.date BETWEEN "{date_from}" AND "{date_to}"  
                AND c.id IN ({company_id_list})             
                '''
    else:
        data = f'''
            SELECT 
                c.id company_id,
                c.name company_name,
                v.date date,
                v.volume volume
            FROM company c
                JOIN volume v
                    ON v.company_id = c.id
            WHERE v.date BETWEEN "{date_from}" AND "{date_to}"  
                AND c.id IN ({company_id_list})             
        '''
    df = __get_data(data)
    # plt.close('all')
    df.groupby(['date', 'company_name'])['volume'].sum().unstack().plot(figsize=(10, 6))

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


# Получение всех значений из таблицы Компании
def get_all_companies():
    data = f'''
            SELECT *
            FROM company        
        '''
    return __get_data(data)


def get_all_volumes():
    data = f'''
            SELECT *
            FROM volume        
            '''
    return __get_data(data)


# Генерация рандомной даты для поля Дата Создания Компании
def generate_random_date():
    year = randrange(1920, 2000)
    month = randrange(1, 12)
    day = randrange(1, 28)
    date = datetime.date(year=year, month=month, day=day)
    return str(date)

# Удаление данных из таблицы Company
def __company_clear(company=None):
    if not company:
        data = '''
            DELETE FROM company   
        '''
    else:
        data = f'''
                    DELETE FROM company
                    WHERE company.id = {company['iexId']} 
                '''
    __exec_sql(data)


# Удаление данных из таблицы Volume
def __volume_clear(company=None):
    if not company:
        data = '''
            DELETE FROM volume
        '''
    else:
        data = f'''
            DELETE FROM volume
            WHERE volume.company_id = {company['iexId']} 
        '''
    __exec_sql(data)


# Удаление таблицы Company
def __remove_company_table():
    data = '''
        DROP TABLE IF EXISTS company
    '''
    __exec_sql(data)


# Удаление таблицы Volume
def __remove_volume_table():
    data = '''
        DROP TABLE IF EXISTS volume
    '''
    __exec_sql(data)


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

if __name__ == '__main__':

    # __remove_volume_table()

    print(get_all_volumes())

    # insert_handmade_company()
    # df = get_all_companies()
    # print(df)

