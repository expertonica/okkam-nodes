import os
import pandas as pd
from .dynamic_bookcases import make_dynamic_bookcase

CAT_NUM = 10

def load_bookcases(raw_query, companies):
    bc_companies = {}

    bookcase_classic = {}
    bookcase_query = {}
    bookcase_classic_not_filtered = {}
    bookcase_query_not_filtered = {}

    id_translation = {}

    with open('static_bookcases/companies.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                ss = line.split(',')
                id_translation[int(ss[0])] = int(ss[1])

    data = pd.read_csv("static_bookcases/shelves.csv", delimiter=";")
    for i in range(data.shape[0]):
        bc = int(data.iloc[i, 0])
        #print('bccc')
        dccc = data.iloc[i, 4]
        dcc = dccc.split(' ')
        for c in dcc:
            if '(2)' in c:
                ncid = int(c.split('(')[0])
                cid = id_translation[ncid]

                #print(str(ncid)+':'+str(cid))
                if cid in companies:
                    cc = bookcase_classic.get(bc, [])
                    cc.append(cid)
                    bookcase_classic[bc] = cc

                cc = bookcase_classic_not_filtered.get(bc, [])
                cc.append(cid)
                bookcase_classic_not_filtered[bc] = cc



    '''
    fname_classic = os.path.join('support', 'node', 'shelve_classic.xlsx')
    excel_data_df = pd.read_excel(fname_classic, sheet_name=0)
    for i in range(excel_data_df.shape[0]):
        company = {}
        cid = excel_data_df.iloc[i, 3]
        bc = excel_data_df.iloc[i, 0]
        company['bookcase'] = excel_data_df.iloc[i, 0]
        company['shelve'] = excel_data_df.iloc[i, 1]
        company['appeared'] = excel_data_df.iloc[i, 2]
        company['cid'] = cid
        #company['titles_with_query'] = self.get_titles(cid, raw_query)
        company['company_name'] = excel_data_df.iloc[i, 4]
        company['url'] = excel_data_df.iloc[i, 5]
        company['positioning'] = excel_data_df.iloc[i, 6]
        for j in range(1, CAT_NUM):
            company['cat' + str(j)] = excel_data_df.iloc[i, 6 + j]

        if cid in companies:
            bc_companies[cid] = company
            cc = bookcase_classic.get(bc, [])
            cc.append(cid)
            bookcase_classic[bc] = cc

        cc = bookcase_classic_not_filtered.get(bc, [])
        cc.append(cid)
        bookcase_classic_not_filtered[bc] = cc
    '''
    elastic_ids = set()
    for cid in companies:
        elastic_ids.add(cid)
    dynamic_bookcases = make_dynamic_bookcase( elastic_ids=elastic_ids)
    print('dynamic')
    for db in dynamic_bookcases:
        if db['percentage']==0.15:
            print('YES')
            #print(db)

            db_bookcases = db['bookcases']
            for bid in db_bookcases:
                shelf = db_bookcases[bid]
                #print('shelf'+ str(shelf))
                for cid in shelf:
                    if cid in companies:
                        #bc_companies[cid]['bookcase_query'] = excel_data_df.iloc[i, 0]

                        cc = bookcase_query.get(bid, [])
                        cc.append(cid)
                        bookcase_query[bid] = cc

                    cc = bookcase_query_not_filtered.get(bid, [])
                    cc.append(cid)
                    bookcase_query_not_filtered[bid] = cc
            break
    print('QQ')
    #print(elastic_ids)
    #print(bookcase_query_not_filtered)
    #print(from .dynamic_bookcases import make_dynamic_bookcase)



    '''
    fname_query = os.path.join('support', 'node', 'node_' + str(raw_query), '0.15',
                               'shelve for each company extended.csv')
    excel_data_df = pd.read_csv(fname_query, delimiter=';')
    for i in range(excel_data_df.shape[0]):
        cid = excel_data_df.iloc[i, 1]
        bc = excel_data_df.iloc[i, 0]

        if cid in companies:
            bc_companies[cid]['bookcase_query'] = excel_data_df.iloc[i, 0]
            # companies[cid]['shelve_query'] = excel_data_df.iloc[i, 1]
            # companies[cid]['appeared_query'] = excel_data_df.iloc[i, 2]

            cc = bookcase_query.get(bc, [])
            cc.append(cid)
            bookcase_query[bc] = cc

        cc = bookcase_query_not_filtered.get(bc, [])
        cc.append(cid)
        bookcase_query_not_filtered[bc] = cc
    '''
    return bc_companies, bookcase_classic, bookcase_query, bookcase_classic_not_filtered, bookcase_query_not_filtered
