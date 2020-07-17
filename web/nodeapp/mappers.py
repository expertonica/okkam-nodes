from .entities import CompanyTop6Entity, PageTop6Entity

def map_get_nodes(json_data):
    companies = {}
    companies_json_data = json_data['companies']
    query = json_data['query']
    for c_data in companies_json_data:
        company_id = c_data['company_id']
        top6 = []
        for p_data in c_data['top_6']:
            top6.append(PageTop6Entity(p_data['url'], p_data['es_score'], p_data['query_in_title']))
        companies[company_id] = CompanyTop6Entity(company_id, top6)
    return query, companies