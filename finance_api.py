import requests
import json
import pandas as pd
import os
from app.db import db_worker
import re
from app.db import db_worker
import config
from config import base_url, companies_url, company_url, company_info_per_year


# Получение данных по компании за год
def get_company_info(company):
    url = base_url + company_info_per_year.format(company_name=company['symbol'])
    print(url)
    responce = requests.get(url=url)
    return json.loads(responce.content)


# Скачивание и сохранение данных по списку компаний
def download_and_save_company_info(company_list):
    for company in company_list:
        company_info = get_company_info(company)
        try:
            json.dump(company_info, open(os.path.join(config.info_dir, f'({company["iexId"]}) {company["name"]}.json'), 'w'))
        except Exception as e:
            print(f'Error during "save_company_info": {e}')
        else:
            print(f'Сохранена инфа за год по компании "{company["name"]}"')


# Получение из списка всех компаний, компаний технических
def get_all_tech_companies():
    all_comps = json.loads(requests.get(base_url + companies_url).content)
    res = []
    for company in all_comps:
        company_info = get_company_info(company)
        if company_info['sector'] == 'Technology':
            try:
                with open(os.path.join(config.info_dir, company_info["companyName"]), 'w') as f:
                    json.dump(company_info, f)
            except Exception as e:
                print(f'Error: {e}')
            else:
                print('Saved')
            res.append(company)
    return res


# Преобразование инфрмации о компании из файла в df
def get_info_df(file_name):
    info = json.load(open(file_name))
    df = pd.DataFrame(info)[['date', 'volume', 'vwap']]
    return df


# Заполнение БД данными из файлов
def fill_info():
    def get_id(text):
        search = re.search(r'\((\d+)\)', text)
        if search:
            return int(search.group(1))
        return None

    for info in os.listdir(config.info_dir):
        info_df = get_info_df(os.path.join(config.info_dir, info))
        info_df['company_id'] = get_id(info)
        db_worker.insert_info(info_df)
        print(f'Company "{info.replace(".json", "")}" inserted.')


if __name__ == '__main__':

    # # Загрузка данных по техническим компаниям
    # comps = json.load(open(config.tech_companies_list_json))
    # print(len(comps))
    # save_company_info(comps)

    # # Заполнение БД данными
    # fill_info()

    # lst = db_worker.get_companies_list()
    # print(list(enumerate(lst, start=1)))

    pass


