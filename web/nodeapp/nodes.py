from .bookcases import load_bookcases


def get_average_es(companies, common):
    if len(common) == 0:
        return 0
    s = 0
    n = 0
    for cid in common:
        for p_data in companies[cid].top6:
            s += p_data.es_score
            n += 1
    if n == 0:
        return 0
    return s / n

def get_node( bookcase_classic, bookcase_classic_not_filtered, bookcase_query, companies, bc_classic,
             bc_query):
    node = {}
    bcid_classic = bookcase_classic[bc_classic]
    bcid_classic_not_filtered = bookcase_classic_not_filtered[bc_classic]
    bcid_query = bookcase_query[bc_query]


    aver_titles = 0
    common_not_filtered = set(bcid_classic).intersection(set(bcid_query))
    common = set()
    for cid in common_not_filtered:
        if companies[cid].titles_with_query > 0:
            common.add(cid)
            aver_titles += companies[cid].titles_with_query

    if len(common) > 0:
        aver_titles = aver_titles / len(common)

    if len(common) == 0:
        return None

    node['bc_classic'] = bc_classic
    node['bc_query'] = bc_query
    node['common'] = common
    node['L'] = len(common)
    node['R'] = len(common) / len(bcid_classic_not_filtered)
    node['aver_es'] = get_average_es(companies, common)
    node['score'] = node['R'] * node['L'] * node['aver_es']
    node['aver_titles'] = aver_titles

    return node

def calculate_nodes(query, companies):
    bc_companies, bookcase_classic, bookcase_query, bookcase_classic_not_filtered, bookcase_query_not_filtered \
        = load_bookcases(query, companies)

    nodes = {}
    n = 0
    for bc_classic in bookcase_classic:
        for bc_query in bookcase_query:
            node = get_node(bookcase_classic, bookcase_classic_not_filtered, bookcase_query, companies,
                                 bc_classic, bc_query)
            if node:
                node['node_id'] = n
                nodes[n] = node
                n += 1

    return nodes



