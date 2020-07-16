

class CompanyTop6Entity:
    def __init__(self, company_id, top6):
        self.company_id = company_id
        self.top6 = top6
        self.titles_with_query = self.count_titles_with_query(self.top6)

    def count_titles_with_query(self, top6):
        titles_with_query = 0
        for p_data in top6:
            if p_data.query_in_title > 0:
                titles_with_query += 1
        return titles_with_query

class PageTop6Entity:
    def __init__(self, url, es_score, query_in_title):
        self.url = url
        self.es_score = es_score
        self.query_in_title = query_in_title