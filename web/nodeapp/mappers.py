import re
from pymystem3 import Mystem

from .entities import CompanyTop6Entity, PageTop6Entity


def query_in_title(m, title, raw_query):

    query = set(m.lemmatize(raw_query))

    n = 0
    # TODO убрать лишние слова и прочее из загловка
    title = re.sub('\W+', ' ', title).strip().lower()
    lemmas = set(m.lemmatize(title))

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
            qit = query_in_title(m, p_data['title'], query)
            top6.append(PageTop6Entity(p_data['url'], p_data['es_score'], qit))
        companies[company_id] = CompanyTop6Entity(company_id, top6)
    return query, companies