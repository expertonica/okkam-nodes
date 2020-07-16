import os
import pandas as pd

CAT_NUM = 10

def load_bookcases(raw_query, companies):
    bc_companies = {}

    bookcase_classic = {}
    bookcase_query = {}
    bookcase_classic_not_filtered = {}
    bookcase_query_not_filtered = {}
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

    return bc_companies, bookcase_classic, bookcase_query, bookcase_classic_not_filtered, bookcase_query_not_filtered
