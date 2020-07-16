from .entities import CompanyTop6Entity, PageTop6Entity

def map_get_nodes(json_data):
    companies = {}
    for c_data in json_data:
        company_id = c_data['company_id']
        top6 = []
        for p_data in c_data['top_6']:
            top6.append(PageTop6Entity(p_data['url'], p_data['es_score'], p_data['query_in_title']))
        companies[company_id] = CompanyTop6Entity(company_id, top6)
    return companies