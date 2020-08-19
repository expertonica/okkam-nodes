import re
from pymystem3 import Mystem

from .entities import CompanyTop6Entity, PageTop6Entity

def lemmatize_str(m, str):
    str = str.lower().strip()
    str = re.sub('\W+', ' ', str)
    lemmas = set(m.lemmatize(str))
    good_lemmas = []
    for l in lemmas:
        l = l.strip()
        if len(l) >= 2:
            good_lemmas.append(l)
    return good_lemmas

def query_in_title(m, title, raw_query):

    query = lemmatize_str(m, raw_query)

    n = 0
    # TODO убрать лишние слова и прочее из загловка
    #title = re.sub('\W+', ' ', title).strip().lower()
    #lemmas = set(m.lemmatize(title))
    lemmas = lemmatize_str(m, title)

    for q in query:
        if q in lemmas:
            n += 1

    return n

def map_get_nodes(json_data):
    m = Mystem()
    companies = {}
    companies_json_data = json_data['companies']
    query = json_data['query']
    for c_data in companies_json_data:
        company_id = c_data['company_id']
        top6 = []
        for p_data in c_data['top_6']:
            title = p_data['title']
            if not title:
                title = ''
            qit = query_in_title(m, title, query)
            top6.append(PageTop6Entity(p_data['url'], p_data['es_score'], qit))
        companies[company_id] = CompanyTop6Entity(company_id, top6)
        '''
        if company_id==28294:
            print('CHECK!!!!')
            print(vars(companies[company_id]))
            for page in companies[company_id].top6:
                print(vars(page))
        '''
    return query, companies