

class CompanyTop6Entity:
    def __init__(self, company_id, top6):
        self.company_id = company_id
        self.top6 = top6
        self.aver_es = self.calc_aver_es(self.top6)
        self.title_score = self.calc_title_score(self.top6)
        self.titles_with_query = self.count_titles_with_query(self.top6)

    def calc_aver_es(self, top6):
        ss = 0
        for p_data in top6:
            ss+=p_data.es_score
        if len(top6)>0:
            ss = ss / len(top6)
        return ss

    def calc_title_score(self, top6):
        title_score = 0
        n = 0

        for p_data in top6:
            if p_data.query_in_title > 0:
                title_score+=p_data.query_in_title
                n+=1

        if n>0:
            title_score = title_score / n

        return title_score

    def count_titles_with_query(self, top6):
        titles_with_query = 0
        for p_data in top6:
            if p_data.query_in_title > 0:
                titles_with_query += 1
        return titles_with_query

    def get_link(self):
        if len(self.top6) == 0:
            return ''
        return self.top6[0].url

class PageTop6Entity:
    def __init__(self, url, es_score, query_in_title):
        self.url = url
        self.es_score = es_score
        self.query_in_title = query_in_title