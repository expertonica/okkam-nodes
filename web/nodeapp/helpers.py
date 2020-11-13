import datetime
import os
import json
from xlsxwriter.workbook import Workbook




def log_json_data(query, json_data):
    now = datetime.datetime.now()

    fname_json = 'dump_' + query + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(
        now.hour) + '_' + str(
        now.minute) + '_' + str(now.second) + '.json'

    with open(os.path.join('media_root', fname_json), 'w') as f:
        json.dump(json_data, f)


    fname = 'data_'+query + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '_' + str(
        now.minute) + '_' + str(now.second) + '.xls'

    book = Workbook(os.path.join('media_root', fname))
    sheet = book.add_worksheet('test')
    sheet.write(0, 0, 'company_id')
    sheet.write(0, 1, 'url')
    sheet.write(0, 2, 'es_score')
    sheet.write(0, 3, 'query_in_title')
    sheet.write(0, 4, 'title')

    companies_json_data = json_data['companies']
    query = json_data['query']
    row = 1
    for c_data in companies_json_data:
        company_id = c_data['company_id']
        for p_data in c_data['top_6']:
            title = p_data['title']
            url = p_data['url']
            es_score = p_data['es_score']
            query_in_title = p_data['query_in_title']

            sheet.write(row, 0, company_id)
            sheet.write(row, 1, url)
            sheet.write(row, 2, es_score)
            sheet.write(row, 3, query_in_title)
            sheet.write(row, 4, title)

            row+=1



    book.close()