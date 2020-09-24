from django.core.management.base import BaseCommand
from collections import defaultdict

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from nodeapp.models import UrlWc


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('MONGO TO POSTGRESS')

        self.transfer_all()
        #self.transfer_one_company(11496)

    def transfer_all(self):
        data = []
        with open('site_list.csv', 'r') as f:
            for line in f:
                line = line.strip()
                ss = line.split('|')
                cid = int(ss[0])
                company_url = ss[1]
                data.append((cid, company_url))


        i = 0
        for d in data:
            if i % 50 == 0:
                print(str(i)+'/'+str(len(data)))
            i+=1
            cid = d[0]
            company_url = d[1]
            try:
                self.transfer_one_company(cid, company_url)
            except Exception as ex:
                f = open('logs.txt', 'a')
                f.write('**************' + '\r\n')
                f.write(str(cid)+' '+company_url+'\r\n')
                f.write(str(ex)+'\r\n')
                f.write('**************' + '\r\n')
                f.close()
            break


    def transfer_one_company(self, cid, company_url):
        urls_db = UrlWc.objects.filter(company_id=cid)
        if urls_db:
            print('delete')
            urls_db.delete()

        print('MONGO')
        db = MongoDatabase()
        mongo_company = db.get_rd(int(cid))[2]
        for url in mongo_company:
            url_decoded = url.replace('%60', '.').replace('`', '.')
            url_wc = UrlWc(url=url_decoded, company_id=cid, company_url=company_url, word_counter=mongo_company[url])
            url_wc.save()


class MongoDatabase:

    def __init__(self):
        # MONGO_HOST = '94.130.204.53'
        MONGO_HOST = 'beta.okkam.io'
        MONGO_PORT = 27017
        self.mongo_client = MongoClient(MONGO_HOST, MONGO_PORT, connect=False,
                                        username='myUserAdmin', password='qwer1234',
        )
        self.mongo_db = self.mongo_client['elastic_db']
        self.cached_data_collection = self.mongo_db['cached_data']
        self.all_companies = self.mongo_db['all_companies']

    def insert_rd(self, company_id, each_page_links_list, first_url, word_counters, titles):
        # return self.cached_data_collection.insert_many([{'company_id': 1, 'str': 'asd'}, {'company_id': 1, 'str': 'asd'}])
        # print(each_page_links_list)

        if len(each_page_links_list) > 8000:
            i = 0
            portion = {}

            for word, counter in each_page_links_list.items():

                portion.update({
                    word: counter
                })
                i += 1
                if i == 8000:
                    self.cached_data_collection.insert_one(
                        {"company_id": company_id,
                         'each_page_links_list': portion,
                         }
                    )
                    i = 0
                    portion = {}

            if i > 0:
                self.cached_data_collection.insert_one(
                    {"company_id": company_id,
                     'each_page_links_list': portion,
                     }
                )
        else:
            self.cached_data_collection.insert_one(
                {"company_id": company_id,
                 'each_page_links_list': each_page_links_list,

                 }
            )
        i = 0
        portion = {}

        for word, counter in word_counters.items():

            portion.update({
                word: counter
            })
            i += 1
            if i == 300:
                self.cached_data_collection.insert_one(
                    {"company_id": company_id,
                     'word_counters': portion,
                     }
                )
                i = 0
                portion = {}

        if i > 0:
            self.cached_data_collection.insert_one(
                {"company_id": company_id,
                 'word_counters': portion,
                 }
            )

        self.cached_data_collection.insert_one(
            {"company_id": company_id,
             # 'each_page_links_list': each_page_links_list,
             'first_url': first_url,
             # 'word_counters': word_counters,
             'titles': titles
             }
        )

    def delete_all(self):
        self.cached_data_collection.delete_many({})

    def delete_company_id(self, company_id):
        return self.cached_data_collection.delete_many({'company_id': company_id})

    def create_index(self):
        return self.cached_data_collection.create_index('company_id')
    def list_indexes(self):
        return self.cached_data_collection.index_information()
    def get_rd(self, company_id):
        """

        :rtype: dict
        """
        # return [item for item in self.cached_data_collection.find({'company_id': 1})]

        result = defaultdict(dict)
        i = 1
        for document in self.cached_data_collection.find({'company_id': company_id}):
            # print('got reth doc', i)
            i += 1
            if 'word_counters' in document:
                result['word_counters'].update(
                    document['word_counters']
                )
            elif 'each_page_links_list' in document:
                result['each_page_links_list'].update(
                    document['each_page_links_list']
                )
            else:
                result.update(
                    document
                )

        return result['each_page_links_list'], result['first_url'], result['word_counters'], result['titles']







    def user_count_in_tlc7(self):
        return self.cached_data_collection.count_documents({})

    def set_as_cached(self, company_id):
        # return self.r.table('caching_data').index_create('id').run()

        return self.all_companies.update_one({'_id': company_id}, {"$set":{"is_parsed": True}})
        # return self.r.db("top6_db").table_create("caching_data").run()

    def import_ids(self, ids):
        return self.all_companies.insert_many([{'_id': company_id,
                                                     'is_parsed': False} for company_id in ids])

    def get_all_not_cached(self):
        # return self.r.table('caching_data').index_create('id').run()

        return [item['_id'] for item in self.all_companies.find({"is_parsed": False})]
        # return self.r.db("top6_db").table_create("caching_data").run()

    def write_companies_from_file(self):
        # return self.r.table('caching_data').index_create('id').run()
        with open('all_companies.txt', 'r') as f:
            self.all_companies.insert_many([
                {'_id': int(line), 'is_parsed': False} for line in f.readlines()
            ])


        return [item['_id'] for item in self.all_companies.find({"is_parsed": False})]
        # return self.r.db("top6_db").table_create("caching_data").run()

    def write_companies_from_file_second(self):
        # return self.r.table('caching_data').index_create('id').run()
        print(self.all_companies.count())
        # with open('comp_list.txt', 'r') as f:
        #     for line in f.readlines():
        #         try:
        #             self.all_companies.insert({'_id': int(line.split('|')[0]), 'is_parsed': False})
        #         except DuplicateKeyError:
        #             print('dub')



        return [item['_id'] for item in self.all_companies.find({"is_parsed": False})]
        # return self.r.db("top6_db").table_create("caching_data").run()

    def close(self):
        self.mongo_client.close()

    def index_show(self):
        return [index for index in self.cached_data_collection.list_indexes()]
