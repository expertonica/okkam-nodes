import operator
import datetime
import os
from xlsxwriter.workbook import Workbook

from .models import  UrlWc

MAX_WORDS = 1000



def load_db(companies):
    pages = []
    for cid in companies:
        for page in companies[cid].top6:
            pages.append(page.url)


    #q = UrlWc.objects.filter(url='bestbaby.kz/ru/article/chto-takoe-videonyanya-kak-ona-vyglyadit-zachem-nuzhna_3')
    #return q

    company_urls = {}

    urlWcs = UrlWc.objects.filter(url__in=pages)
    db_urls = {}
    for uwc in urlWcs:
        db_urls[uwc.url] = uwc
        company_urls[uwc.company_id] = uwc.company_url

    return db_urls, company_urls

def get_wc_for_company(company, db_urls):
    wc = {}
    for page in company.top6:
        #page_wc = {'привет': 1, 'как': 2, 'дела': 3}
        page_wc = {}
        urlWc = db_urls.get(page.url, None)
        if urlWc:
            page_wc = urlWc.word_counter
        for w in page_wc:
            wc[w] = wc.get(w, 0) + page_wc.get(w, 0)

    sorted_x = sorted(wc.items(), key=operator.itemgetter(1), reverse=True)
    sorted_x = sorted_x[:MAX_WORDS]
    words = [x[0] for x in sorted_x]

    new_wc = { w: wc[w]  for w in words}

    summ = sum(list(new_wc.values()))
    if summ==0:
        summ = 1
    for w in new_wc:
        new_wc[w] = new_wc[w] / summ

    return new_wc


def get_world_counters(companies, db_urls):
    word_counters = {}
    for cid in companies:
        wc = get_wc_for_company(companies[cid], db_urls)
        word_counters[cid] = wc
    return word_counters

def get_all_words(word_counters):

    all_words = set()

    for cid in word_counters:
        words = set(word_counters[cid].keys())
        all_words.update(words)

    return all_words

def calc_mask(node, word_counters, all_words):
    mask = {}
    node_words = set()
    for cid in node['common']:
        node_words.update(set(word_counters[cid].keys()))

    for word in node_words:
        A = 0
        B = 0
        for cid in word_counters:
            if word in word_counters[cid]:
                if cid in node['common']:
                    A+=1
                B+=1
        if A > 1:
            R = (A/len(node['common'])) - (B/len(word_counters))
            mask[word] = R

    return mask

def calc_all_masks(nodes, word_counters, all_words):
    all_masks = {}
    for nid in nodes:
        mask = calc_mask(nodes[nid], word_counters, all_words)
        all_masks[nid] = mask

    return all_masks


def calc_M(mask, word_counter, word_limit):

    ms = []
    for word in mask:
        m = mask.get(word, 0)*word_counter.get(word, 0)
        if m>0:
            ms.append(m)

    ms.sort(reverse=True)

    ms = ms[:word_limit]

    M = sum(ms)

    return M, len(ms)

def create_mask(query, nodes, companies):

    print('***********MASK*****************')

    db_urls, company_urls = load_db(companies)


    #key - cid, value - словарь слов с весами
    word_counters = get_world_counters(companies, db_urls)

    all_words = get_all_words(word_counters)

    now = datetime.datetime.now()
    fname = 'mask_'+query + '_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) + '_' + str(
        now.minute) + '_' + str(now.second) + '.xls'

    book = Workbook(os.path.join('media_root', fname))
    sheet = book.add_worksheet('test')
    sheet.write(0, 0, 'Q')
    sheet.write(0, 1, 'Q')
    sheet.write(0, 2, 'Q')
    sheet.write(0, 3, 'Q')
    sheet.write(0, 4, 'Q')
    sheet.write(0, 5, 'Q')
    NODE_START_COLUMN = 6

    col = NODE_START_COLUMN

    node_keys = list(nodes.keys())

    for nid in node_keys:
        node = nodes[nid]
        sheet.write(0, col, nid)
        sheet.write(1, col, node['L'])
        sheet.write(2, col, node['score'])
        col+=1

    all_masks = calc_all_masks(nodes, word_counters, all_words)



    row = 4

    WORD_LIMITS = [15, 30, 50, 100, 1000]

    for cid in companies:
        for i in range(len(WORD_LIMITS)):
            sheet.write(row, 1, i+1)
            sheet.write(row, 2, cid)
            sheet.write(row, 3, company_urls.get(cid, 'WWW'))
            sheet.write(row, 4, WORD_LIMITS[i])
            sheet.write(row, 5, 'TODO')

            col = NODE_START_COLUMN
            for nid in node_keys:
                M, real_words = calc_M(all_masks[nid], word_counters[cid], WORD_LIMITS[i])
                if M:
                    sheet.write(row, col, M)
                col+=1


            row+=1



    book.close()

    return all_words
    #return word_counters[37159]