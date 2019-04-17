import requests
import json
import pandas as pd
import os
from app.db import db_worker
import re
from app.db import db_worker

base_url = 'https://api.iextrading.com/1.0'
company_url = '/stock/{company_name}/company'
companies_url = '/ref-data/symbols'
company_info_per_year = '/stock/{company_name}/chart/1y'

crypto_list_url = '/stock/market/crypto'

nice_companies = ['AAPL', 'MSFT', 'YNDX']


def get_company_info(company):
    url = base_url + company_info_per_year.format(company_name=company['symbol'])
    print(url)
    responce = requests.get(url=url)
    return json.loads(responce.content)


def save_company_info(company_list):
    for company in company_list:
        company_info = get_company_info(company)
        try:
            json.dump(company_info, open(f'tech_companies/info/({company["iexId"]}) {company["name"]}.json', 'w'))
        except Exception as e:
            print(f'Error during "save_company_info": {e}')
        else:
            print(f'Сохранена инфа за год по компании "{company["name"]}"')



def save_all_companies():
    all_comps = json.loads(requests.get(base_url + companies_url).content)
    json.dump(all_comps, open('all_companies.json', 'w'))


def get_all_tech_companies():
    all_comps = json.loads(requests.get(base_url + companies_url).content)
    res = []
    for company in all_comps:
        company_info = get_company_info(company)
        if company_info['sector'] == 'Technology':
            try:
                with open(f'tech_companies\info\{company_info["companyName"]}', 'w') as f:
                    json.dump(company_info, f)
            except Exception as e:
                print(f'Error: {e}')
            else:
                print('Saved')
            res.append(company)
    return res


def save_random_companies():
    all_comps = json.loads(requests.get(base_url + companies_url).content)
    json.dump(all_comps, open('all_companies.json', 'w'))


def get_info_df(file_name):
    info = json.load(open(file_name))
    df = pd.DataFrame(info)[['date', 'volume']]
    return df


def fill_volumes():

    def get_id(text):
        search = re.search(r'\((\d+)\)', text)
        if search:
            return int(search.group(1))
        return None


    info_dir = r'C:\Users\altuhov.n.a\PycharmProjects\free_project\finance_api\tech_companies\info'
    for info in os.listdir(info_dir):
        info_df = get_info_df(os.path.join(info_dir, info))
        info_df['company_id'] = get_id(info)
        db_worker.insert_volumes(info_df)
        print(f'Company "{info.replace(".json", "")}" inserted.')


if __name__ == '__main__':

    # comps = json.load(open('tech_companies/tech_companies.json'))
    # print(len(comps))
    # save_company_info(comps)

    # fill_volumes()
    lst = db_worker.get_companies_list()
    print(list(enumerate(lst, start=1)))


