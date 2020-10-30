import datetime
import os
from xlsxwriter.workbook import Workbook
from django.conf import settings
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

def log_nodes(query, companies, nodes):
    now = datetime.datetime.now()
    fname = query+'_'+str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '_' + str(
        now.minute) + '_' + str(now.second)+'.xls'

    book = Workbook( os.path.join('media_root', fname))
    sheet = book.add_worksheet('test')
    sheet.write(0, 0, 'cid')
    sheet.write(0, 1, 'node')
    sheet.write(0, 2, 'score')
    sheet.write(0, 3, 'link')
    sheet.write(0, 4, 'bookcase_static')
    sheet.write(0, 5, 'bookcase_dynamic')
    sheet.write(0, 6, 'L')
    sheet.write(0, 7, 'R')
    sheet.write(0, 8, 'aver_es')
    sheet.write(0, 9, 'aver_es_company')
    sheet.write(0, 10, 'title_score')
    sheet.write(0, 11, 'titles')

    row = 1

    written_cids = []
    for nid in range(len(nodes)):
        node = nodes[nid]
        for cid in node['common']:
            written_cids.append(cid)
            sheet.write(row, 0, cid)
            sheet.write(row, 1, nid)
            sheet.write(row, 2, node['score'])
            sheet.write(row, 3, companies[cid].get_link())
            sheet.write(row, 4, node['bc_classic'])
            sheet.write(row, 5, node['bc_query'])
            sheet.write(row, 6, node['L'])
            sheet.write(row, 7, node['R'])
            sheet.write(row, 8, node['aver_es'])
            sheet.write(row, 9, companies[cid].aver_es)
            sheet.write(row, 10, companies[cid].title_score)
            sheet.write(row, 11, companies[cid].all_titles)

            row+=1

    for cid in companies:
        if not (cid in written_cids):
            sheet.write(row, 0, cid)
            sheet.write(row, 1, -1)
            sheet.write(row, 2, -1)
            sheet.write(row, 3, companies[cid].get_link())
            sheet.write(row, 4, -1)
            sheet.write(row, 5, -1)
            sheet.write(row, 6, -1)
            sheet.write(row, 7, -1)
            sheet.write(row, 8, -1)
            sheet.write(row, 9, companies[cid].aver_es)
            sheet.write(row, 10, companies[cid].title_score)
            sheet.write(row, 11, companies[cid].all_titles)
            row+=1

    book.close()

    pass

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
        if cid==37494:
            print('FOUND CID 37494')
            print(companies[cid].titles_with_query)
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

    if settings.SHOULD_LOG_RESULTS:
        log_nodes(query, companies, nodes)

    return nodes



